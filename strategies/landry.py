import math

from backtrader import Strategy, indicators, Order

class Landry(Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        p1=21,  # period for the fast moving average
        risk_factor=2,
        size=200,
        allow_buyer=True,
        allow_seller=False,
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

        if is_close_below:
            self.place_buyer_position()

    def handle_seller_position(self):
        is_close_above = self.data.high[0] > self.data.high[-1] and self.data.high[0] > self.data.high[-2]

        if is_close_above:
            self.place_seller_position()

    def place_buyer_position(self):
        if self.position:
            return

        risk = (self.data.high - self.data.low)

        enter_at = self.data.high + 0.01
        stop_loss = self.data.low - 0.01
        stop_gain = self.data.high + (risk * self.p.risk_factor)

        print("---")
        print(self.data.datetime.date())
        print("Low: %.2f" % self.data.low[0])
        print("Low[-1]: %.2f" % self.data.low[-1])
        print("Low[-2]: %.2f" % self.data.low[-2])

        self.buy_bracket(
                exectype=Order.StopLimit,
                limitprice=stop_gain,
                price=enter_at,
                stopprice=stop_loss,
                plimit=self.data.high,
                size=self.p.size)

    def place_seller_position(self):
        if self.position:
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
                size=self.p.size)
