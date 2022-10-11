# %%
import camelot
import pandas as pd
import numpy as np

url = "https://cpsa.ca/MedicalDirectory/Alphabetical%20Listing.pdf"
tables = camelot.read_pdf(url, pages="all", flavor="stream")

total = int(tables[-1].df.loc[4, 1])


# %%
def process(tdf):
    indices = [i for i, value in enumerate(tdf.iloc[0].tolist()) if value == "NAME"]
    dfs = []
    for ind in indices:
        _df = tdf[range(ind, ind + 4)]
        header = _df.iloc[0]
        _df = _df[1:]
        _df.columns = header

        dfs.append(_df)
    df = pd.concat(
        dfs,
        ignore_index=True,
    )
    df = df.replace("", np.nan)
    df = df[~df.apply(lambda row: row.isna().sum() == 4, axis=1)]
    df = df.reset_index(drop=True)
    for ind in df[df.apply(lambda row: row.isna().sum() == 3, axis=1)].index:

        if df.loc[ind]["CITY"] is not np.nan:

            df.loc[ind - 1]["CITY"] += f' {df.loc[ind]["CITY"]}'

        if df.loc[ind]["NAME"] is not np.nan:

            df.loc[ind - 1]["NAME"] += f' {df.loc[ind]["NAME"]}'
    df = df[~df.apply(lambda row: row.isna().sum() == 3, axis=1)]
    return df


df = pd.concat([process(t.df) for t in tables[:-1]], ignore_index=True)
df


# %%
assert df.shape[0] == total


# %%
df.to_csv("physicians.csv", index=False)


# %%
