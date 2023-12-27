# %%
import json
import pickle
import time

import pandas as pd
from seleniumbase import SB
from tqdm import tqdm

df = pd.read_csv("physicians.csv")


# %%
def get_name(name, safe=True, first_name_only=False):
    parts = list(reversed(name.split(", ")))
    if first_name_only:
        parts[0] = parts[0].split()[0]
    n = " ".join(parts)
    if safe:
        n = n.replace(" ", "+")
    return n


names = [get_name(name) for name in df["NAME"].tolist()]


# %%
template = "https://www.ratemds.com/api/doctor_search/?country=ca&text="

resps = []
with SB() as sb:
    for name in tqdm(names):
        url = f"{template}{name}"
        sb.open(url)
        text = sb.get_element("pre").text
        resp = json.loads(text)
        resps.append(resp)
        time.sleep(0.5)

with open("ratemds.pkl", "wb") as f:
    pickle.dump(resps, f)


# %%
with open("ratemds.pkl", "rb") as f:
    resps = pickle.load(f)
count = 0
ratings = []
for resp, name in zip(resps, df["NAME"].tolist()):
    match, idx = 0, []
    for i, result in enumerate(resp["results"]):
        if get_name(name, safe=False, first_name_only=True) in result["full_name"]:
            match += 1
            idx.append(i)

    if match == 1:
        ratings.append(resp["results"][idx[0]]["rating"])
        count += 1
    else:
        ratings.append(
            {
                "bestRating": None,
                "average": None,
                "count": None,
                "helpfulness": None,
                "staff": None,
                "punctuality": None,
                "knowledge": None,
            }
        )

print(f"Found {count} matches")


# %%
pd.DataFrame(ratings).to_csv("ratings.csv", index=False)


# %%
