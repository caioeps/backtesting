import math

from backtrader import Strategy, indicators, Order

class Landry(Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        p1=21,  # period for the fast moving average
        risk_factor=2
    )

    def __init__(self):
        self.sma1 = indicators.SimpleMovingAverage(period=self.p.p1)

    def next(self):
        is_average_pointing_up = self.sma1[0] > self.sma1[-1]

        print("sma1: %s" % self.sma1[0])
        if is_average_pointing_up:
            print("average is pointing up")
            self.handle_buyer_position()

    def handle_buyer_position(self):
        is_close_below = self.data.close[0] < self.data[-1] and self.data.close[0] < self.data[-2]

        if is_close_below:
            self.place_buyer_position()

    def place_buyer_position(self):
        risk = (self.data.high - self.data.low)

        enter_at = self.data.high + 0.01
        stop_loss = self.data.low - 0.01
        stop_gain = self.data.high + risk * self.p.risk_factor

        size = 200

        print("Placing buyer order at $ %.2f" % enter_at)

        mainside = self.buy(price=enter_at,
                            exectype=Order.Limit,
                            size=size,
                            transmit=False)
        lowside  = self.sell(price=stop_loss,
                             size=mainside.size,
                             exectype=Order.Stop,
                             transmit=False,
                             parent=mainside)
        highside = self.sell(price=stop_gain,
                             size=mainside.size,
                             exectype=Order.Limit,
                             transmit=True,
                             parent=mainside)

