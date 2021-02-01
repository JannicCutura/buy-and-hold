import pandas as pd

funds = pd.DataFrame(data={"WKN":["A1C9DP","A0YAN6",  "A1C9CZ", "A1JJAF","A1C9C2", "LYX0LQ","A111X9", "LYX0YD"],
                          "ISIN":["IE00B2PC0609", "IE00B1W6CW87",  "IE00B0HCGS80","IE00B67WB637","IE0030982288", "LU0317841665","IE00BKM4GZ66","LU1781541179"],
                          "currency":["USD","EUR","USD","EUR","","","USD","USD"]
                          "Name":["Dimensional Global Targeted Value Fund Fonds",
                                  "Dimensional European Value Fund",
                                  "Dimensional Emerg.Markets Value F",
                                  "Dimensional Global Small Companies Fund Fonds",
                                  "Dimensional European Small Companies Fund Fonds",
                                  "Lyxor Core STOXX Europe 600 (DR) - ETF",
                                  "iShares Core MSCI Emerging Markets",
                                  "Lyxor Core MSCI World UCITS ETF acc"]})

isins = list(funds.ISIN.unique())

data = dict()
for isin in isins:
    data[isin] = pd.read_excel(f"https://buy-and-hold-strategy.s3.eu-central-1.amazonaws.com/{isin}.xlsx",
                                 header=0,
                                 engine='openpyxl',
                                 skiprows=7).assign(ISIN = isin)

fund_returns = (pd.concat(data.values(), ignore_index=True)
                .filter(["ISIN", "Date","NAV"]))














