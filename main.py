from datetime import datetime

from os import path, getenv

import backtrader
import pyfolio

from strategies.sma_cross import SmaCross
from strategies.landry import Landry

strategy_mapping = dict(
    sma_cross=SmaCross,
    landry=Landry
)

def get_yahoo_data(dataname):
    return path.join(path.dirname(__file__), 'data', 'yahoo', dataname)

class FixedCommission(backtrader.CommInfoBase):
  def getoperationcost(self, _size, _price):
      return 4.99

cerebro = backtrader.Cerebro()

cerebro.broker.addcommissioninfo(FixedCommission, name='Fixed Commission')

# cerebro.addanalyzer(backtrader.analyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(backtrader.analyzers.PyFolio, _name='pyfolio')
cerebro.addstrategy(strategy_mapping.get(getenv('STRATEGY')))

data0 = backtrader.feeds.YahooFinanceCSVData(
            dataname=get_yahoo_data('BBAS3.SA.weekly.csv'),
            fromdate=datetime(2015, 1, 1),
            todate=datetime(2020, 3, 20),
        )
data0.plotinfo.plotlog = True
data0.plotinfo.plotylimited = True

cerebro.adddata(data0)

strats = cerebro.run()
strat = strats[0]

if getenv('NOSTATS') != 'true':
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    pyfolio.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions)


if getenv('NOPLOT') != 'true':
    cerebro.plot(
            grid=False,
            style='candle',
            # Default color for the 'line on close' plot
            loc='black',
            # Default color for a bullish bar/candle (0.75 -> intensity of gray)
            barup='blue',
            # Default color for a bearish bar/candle
            bardown='red',
            volume=False)
