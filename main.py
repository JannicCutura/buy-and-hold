import pandas as pd, numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MonthLocator


funds = pd.DataFrame(data={"WKN":["A1C9DP","A0YAN6",  "A1C9CZ", "A1JJAF","A1C9C2", "LYX0LQ","A111X9", "LYX0YD"],
                          "ISIN":["IE00B2PC0609", "IE00B1W6CW87",  "IE00B0HCGS80","IE00B67WB637","IE0030982288", "LU0317841665","IE00BKM4GZ66","LU1781541179"],
                          "wghts":[6.89, 11.05, 6.90, 7.20, 11.84, 36.41, 7.38, 61.00],
                          "Name":["Dimensional Global Targeted Value Fund Fonds",
                                  "Dimensional European Value Fund",
                                  "Dimensional Emerg.Markets Value F",
                                  "Dimensional Global Small Companies Fund Fonds",
                                  "Dimensional European Small Companies Fund Fonds",
                                  "Lyxor Core STOXX Europe 600 (DR) - ETF",
                                  "iShares Core MSCI Emerging Markets",
                                  "Lyxor Core MSCI World UCITS ETF acc"]})

funds["wghts"] = funds["wghts"]/funds.wghts.sum()

fund_returns = pd.read_excel("https://buy-and-hold-strategy.s3.eu-central-1.amazonaws.com/buy_and_hold.xlsm",
                     header=0,
                     sheet_name="data",
                     engine='openpyxl',
                     skiprows=4)

fund_returns = (fund_returns.drop(columns="Unnamed: 0")
                            .rename(columns={"ISIN":"date"})
                            .query("date != 'CURRENCY'"))



fund_returns_wide = fund_returns  # store a copy of the wide layout
fund_returns_wide = fund_returns_wide.convert_dtypes()
fund_returns_wide["date"] = fund_returns_wide["date"].dt.date

ref_period = fund_returns_wide.query("date ==@datetime.date(2020,3,12)")

for column in ['IE00B0HCGS80', 'IE00B1W6CW87', 'IE00B2PC0609', 'IE00B67WB637',
       'IE00BKM4GZ66', 'IE0030982288', 'LU0317841665', 'LU1781541179']:
    fund_returns_wide[column] = fund_returns_wide[column]/ref_period[column].iloc[0]*100

fund_returns_wide = fund_returns_wide.filter(['date','IE00B0HCGS80', 'IE00B1W6CW87', 'IE00B2PC0609', 'IE00B67WB637',
       'IE00BKM4GZ66', 'IE0030982288', 'LU0317841665', 'LU1781541179'])

fund_returns_wide = fund_returns_wide.set_index("date")


fund_returns = (fund_returns.set_index("date")
                            .unstack()
                            .reset_index()
                            .rename(columns={"level_0":"ISIN", 0:"Return"}))

fund_returns["date"] = fund_returns["date"].dt.date

df = fund_returns.merge(funds, on="ISIN").convert_dtypes()


ref_period = (df.query("date ==@datetime.date(2020,3,12)")
                .filter(["ISIN","Return"]))

df = df.merge(ref_period, on="ISIN", suffixes=("","_refperiod"))
df["Return_wghts"] = df["Return"]/df["Return_refperiod"]*df["wghts"] *100

df = (df.groupby("date")
        .sum()
        .reset_index()
        .sort_values("date"))

df["buy-and-hold"] = df.Return_wghts
df["panic-sale"] = df.Return_wghts
df["panic-sale"] = np.where(df.date >=datetime.date(2020,3,12), 100,df.Return_wghts)
df["panic-sale"] = np.where(df.date >=datetime.date(2020,6,12), np.NaN, df["panic-sale"])
df = df.query("@datetime.date(2020,7,9)>date >@datetime.date(2019,9,30)")
df = df.set_index("date")


df = df.merge(fund_returns_wide, left_index=True, right_index=True)







## plot
fig, ax = plt.subplots(1,figsize=(8,6))
bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
etfcolor = (24/255,93/255,169/255)
df["buy-and-hold"].plot.line(label="weighted return of ETFs \nin the fairr portfolio", alpha = 1,linewidth=2, color=(24/255,93/255,169/255))
df['IE00B0HCGS80'].plot.line(label="individual returns of ETFs \nin the fairr portfolio", alpha = 0.25,linewidth=2, color=etfcolor)
for etfs in ['IE00B0HCGS80', 'IE00B1W6CW87', 'IE00B2PC0609', 'IE00B67WB637',
       'IE00BKM4GZ66', 'IE0030982288', 'LU0317841665', 'LU1781541179']:
    df[etfs].plot.line( label='_Hidden', alpha = 0.25,linewidth=2, color=etfcolor)

df["panic-sale"].plot.line(label="fairr portfolio",  linewidth=2, color=(182/255,12/255,75/255))

ax.set_xlabel('Date')
ax.set_ylabel('Total Return (12th March 2020 = 100)')

ax.set_ylim((85,165))
ax.set_xlim((datetime.date(2020,1,1),datetime.date(2020,7,7)))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.annotate('fairr and Sutorbank \nsold the portfolio \nentirely on March 12th',
            ha="center", va="center",
            xy=("2020-03-12", 100),
            xytext=("2020-02-04", 116),
            arrowprops=dict(facecolor='black', arrowstyle="->", connectionstyle="arc3"),
            bbox=bbox_props)

ax.annotate('The weighted returns of \nETFs in the fair portfolio\n reach their lowest point \non 18th March, six days \nafter  the panic sale',
            ha="center", va="center",
            xy=("2020-03-23", df["buy-and-hold"].min()),
            xytext=("2020-02-01", 97),
            arrowprops=dict(facecolor='black', arrowstyle="->", connectionstyle="arc3"),
            bbox=bbox_props)

ax.annotate("", xy=("2020-06-12", 119.3),
            xytext=("2020-06-12", 100),
            arrowprops=dict(arrowstyle="<->", connectionstyle="arc3"))

ax.text("2020-06-12", 110, "Fairr reinvests June \n12th after the market \nregained 20% points",
        ha="center", va="center", rotation=0, bbox=bbox_props)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(MonthLocator())
#plt.gcf().autofmt_xdate()
#fig.tight_layout()
plt.legend(loc="upper right", title="Strategy", frameon=True)

plt.suptitle("Fairr riester portfolio: Buy-and-hold vs panic-sale ", fontsize=16)
ax.set_title('The fairr Riester portfolio consisted of eight ETFs (light blue lines). The dark blue line and the dark '
             '\nred line visualize the returns of fairr portfolio for a buy-and-hold and panic-sale stragey respectively', fontsize = 8)


plt.show()
plt.xticks(rotation = 0)
fig.savefig("C:\\Users\\janni\\Dropbox\\university\\13 Semester bis zum Lebensende\\2021_02 buy-and-hold\\codes\\docs\\buy_and_hold.png")

