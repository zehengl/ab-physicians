# %%
from stats_can import StatsCan

sc = StatsCan()
df = sc.table_to_df("98-10-0002-01")
df.to_csv("population.csv", index=False)


# %%
