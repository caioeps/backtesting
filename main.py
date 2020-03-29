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

cerebro = backtrader.Cerebro()

# cerebro.addanalyzer(backtrader.analyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(backtrader.analyzers.PyFolio, _name='pyfolio')
cerebro.addstrategy(strategy_mapping.get(getenv('STRATEGY')))

data0 = backtrader.feeds.YahooFinanceCSVData(
            dataname=get_yahoo_data('B3SA3.SA.csv'),
            fromdate=datetime(2015, 1, 1),
            todate=datetime(2020, 3, 20)
        )

cerebro.adddata(data0)

strats = cerebro.run()

if getenv('NOSTATS') != 'true':
    pyfoliozer = strats.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    pyfolio.create_full_tear_sheet(
            returns,
            positions=positions,
            transactions=transactions,
            gross_lev=gross_lev,
            live_start_date='2005-05-01',  # This date is sample specific
            round_trips=True)


if getenv('NOPLOT') != 'true':
    cerebro.plot()
