from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="ab-physicians", page_icon="random")
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://cdn3.iconfinder.com/data/icons/covid-19-coronavirus-protection-or-prevention-fill/64/HospitalCovid-19-512.png",
        use_column_width=True,
    )
st.title("AB Physicians")


@st.cache
def load_df():
    df = pd.read_csv("physicians.csv")
    return df


df = load_df()
st.subheader("DataFrame")
st.dataframe(df)

st.subheader("Top 10 Cities regarding Number of Physicians")
most_physicians = df["CITY"].value_counts().reset_index()
most_physicians.columns = ["city", "count"]
fig = px.bar(
    most_physicians.head(10),
    x="city",
    y="count",
    color="city",
)
fig

st.subheader("Specialties")
specialties = Counter()
for specialty in df["SPECIALTY"]:
    for s in specialty.split():
        if s == "-":
            continue
        specialties[s] += 1
specialties = pd.DataFrame(
    dict(specialty=specialties.keys(), count=specialties.values())
).sort_values("count", ascending=False)
fig = px.bar(
    specialties,
    x="specialty",
    y="count",
    color="specialty",
)
fig
