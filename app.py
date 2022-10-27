from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="ab-physicians", page_icon=":mask:")
_, center, _ = st.columns([2, 1, 2])
with center:
    st.image(
        "https://cdn3.iconfinder.com/data/icons/covid-19-coronavirus-protection-or-prevention-fill/64/HospitalCovid-19-512.png",
        use_column_width=True,
    )
st.title("AB Physicians")


@st.cache
def load_df():
    df_physicians = pd.read_csv("physicians.csv")
    df_population = pd.read_csv("population.csv")
    df_ratings = pd.read_csv("ratings.csv")

    df_physicians["NUM_SPECIALTIES"] = df_physicians["SPECIALTY"].apply(
        lambda s: len([x for x in s.split() if x != "-"])
    )
    df_physicians = pd.merge(
        df_physicians, df_ratings, left_index=True, right_index=True
    )

    return df_physicians, df_population


df_physicians, df_population = load_df()
st.subheader("DataFrame")
st.dataframe(df_physicians)

st.subheader("Top 10 Cities regarding Number of Physicians")
most_physicians = df_physicians["CITY"].value_counts().reset_index()
most_physicians.columns = ["city", "count"]
fig = px.bar(
    most_physicians.head(10),
    x="city",
    y="count",
    color="city",
)
fig

ratio = pd.merge(
    most_physicians,
    df_population[["GEO", "Population and dwelling counts (13): Population, 2021 [1]"]],
    how="left",
    left_on="city",
    right_on="GEO",
)
ratio["ratio"] = (
    ratio["count"] / ratio["Population and dwelling counts (13): Population, 2021 [1]"]
)
fig = px.bar(
    ratio.head(10),
    x="city",
    y="ratio",
    color="city",
)
st.latex(r"ratio = \dfrac{\# of Physicians}{\# of Population}")
fig

st.subheader("Specialties")
specialties = Counter()
for specialty in df_physicians["SPECIALTY"]:
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
fig.update_layout(showlegend=False)
fig

fig = px.histogram(
    df_physicians,
    x="NUM_SPECIALTIES",
    color="NUM_SPECIALTIES",
)
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    )
)
fig

st.subheader("Ratings")
fig = px.box(
    df_physicians[
        df_physicians["CITY"].isin(most_physicians.head(10)["city"])
        & (df_physicians["average"])
    ].dropna(),
    y="average",
    x="CITY",
    category_orders={"CITY": most_physicians.head(10)["city"]},
    color="CITY",
)
fig
