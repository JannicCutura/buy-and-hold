import pandas as pd
import yfinance as yf

from tools.funds import funds_df

tsla_df = yf.download('IE00B2PC0609',
                      start='2019-01-01',
                      end='2019-12-31',
                      progress=False)
tsla_df.head()


df = investpy.get_fund_recent_data(fund='Dimensional Global Targeted Value Fund Fonds', country="germany")
print(df.head())

funds_dict = pd.DataFrame(investpy.get_funds_dict(country=None)).query("isin == 'IE00B2PC0609'")











