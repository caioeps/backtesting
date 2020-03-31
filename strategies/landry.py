import datetime

from backtrader import Strategy, indicators, Order

def dump(obj, name):
  for attr in dir(obj):
    print("%s.%s = %r" % (name, attr, getattr(obj, attr)))

# @see https://www.youtube.com/watch?v=ztP0f6TVtTw&list=PLxQOwM1DuBkSuzl927Om4VI3-9RuaqF7e&index=13&t=0s
class Landry(Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        p1=20,  # period for the fast moving average
        risk_factor=2,
        size=200,
        allow_buyer=True,
        allow_seller=True,
        expiration_days=7*3
    )

    def __init__(self):
        self.sma1 = indicators.SimpleMovingAverage(period=self.p.p1)

    def next(self):
        is_average_pointing_up = self.sma1[0] > self.sma1[-1]

        if self.p.allow_buyer and is_average_pointing_up:
            self.handle_buyer_position()
        elif self.p.allow_seller and not is_average_pointing_up:
            self.handle_seller_position()

    def handle_buyer_position(self):
        is_close_below = self.data.low[0] < self.data.low[-1] and self.data.low[0] < self.data.low[-2]

        if any(self.get_open_main_orders()) and is_close_below:
            for order in self.get_open_main_orders():
                self.cancel(order)
                self.place_buyer_position()
        if is_close_below and not self.position:
            self.place_buyer_position()

    def handle_seller_position(self):
        is_close_above = self.data.high[0] > self.data.high[-1] and self.data.high[0] > self.data.high[-2]

        if any(self.get_open_main_orders()) and is_close_above:
            for order in self.get_open_main_orders():
                self.cancel(order)
                self.place_buyer_position()
        if is_close_above and not self.position:
            self.place_seller_position()

    def place_buyer_position(self):
        risk = (self.data.high - self.data.low)

        enter_at = self.data.high + 0.01
        stop_loss = self.data.low - 0.01
        stop_gain = self.data.high + (risk * self.p.risk_factor)

        breakpoint()
        self.buy_bracket(
                exectype=Order.StopLimit,
                limitprice=stop_gain,
                price=enter_at,
                stopprice=stop_loss,
                size=self.p.size)

    def place_seller_position(self):
        if len(self.get_open_main_orders()) > 0:
            return

        risk = (self.data.high - self.data.low)

        enter_at = self.data.low - 0.01
        stop_loss = self.data.high + 0.01
        stop_gain = self.data.low - (risk * self.p.risk_factor)

        self.sell_bracket(
                exectype=Order.StopLimit,
                limitprice=stop_gain,
                price=enter_at,
                stopprice=stop_loss,
                plimit=self.data.low,
                size=self.p.size,
                valid=self.data.datetime.date(0) + \
                        datetime.timedelta(days=self.p.expiration_days))

    def get_open_main_orders(self):
        return [order for order in self.broker.get_orders_open() if not order.parent];

class _LandryBuyer():
    def __init__(strategy):
        self.strategy = strategy
