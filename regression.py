import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import linregress
from scipy.stats import t as t_dist


df = pd.read_csv("season_2025_26.csv")


# Povprečje vseh serij istega skakalca brez trenutne tekme
group_sum = (
    df.groupby("name")[["series1", "series2"]]
    .transform("sum")
    .sum(axis=1)
)

group_count = (
    df.groupby("name")[["series1", "series2"]]
    .transform("count")
    .sum(axis=1)
)

current_sum = (
    df[["series1", "series2"]]
    .sum(axis=1, skipna=True)
)

current_count = (
    df[["series1", "series2"]]
    .count(axis=1)
)

other_sum = group_sum - current_sum
other_count = group_count - current_count

df["avg"] = other_sum / other_count


df["dif1"] = df["series1"] - df["avg"]
df["dif2"] = df["series2"] - df["avg"]


reg = df[
    ["date", "location", "name",
     "series1", "series2", "avg",
     "dif1", "dif2"]
].dropna(subset=["dif1", "dif2"])


x = reg["dif1"]
y = reg["dif2"]

rezultat = linregress(x, y)


print("REZULTATI REGRESIJE")
print("--------------------")
print(f"Korelacija (r): {rezultat.rvalue:.6f}")
print(f"Naklon: {rezultat.slope:.6f}")
print(f"Intercept: {rezultat.intercept:.6f}")
print(f"R²: {rezultat.rvalue ** 2:.6f}")
print(f"p-vrednost za naklon ≠ 0: {rezultat.pvalue:.6e}")


n = len(x)
df_stopinje = n - 2

t_stat = (
    (rezultat.slope - 1)
    / rezultat.stderr
)

p_manj_kot_1 = t_dist.cdf(
    t_stat,
    df=df_stopinje
)

print()
print("TEST NAKLONA < 1")
print("----------------")
print(f"t-statistika: {t_stat:.6f}")
print(
    f"p-vrednost za naklon < 1: "
    f"{p_manj_kot_1:.6e}"
)


min_val = min(x.min(), y.min())
max_val = max(x.max(), y.max())

margin = (max_val - min_val) * 0.05

x_min = min_val - margin
x_max = max_val + margin

# Točke za regresijsko premico
x_line = np.linspace(x_min, x_max, 100)
y_line = (
    rezultat.slope * x_line
    + rezultat.intercept
)


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="markers",
        name="Skoki",
        marker=dict(
            size=7,
            opacity=0.35
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=x_line,
        y=y_line,
        mode="lines",
        name=f"Regresija (β = {rezultat.slope:.2f})"
    )
)

fig.add_trace(
    go.Scatter(
        x=[x_min, x_max],
        y=[x_min, x_max],
        mode="lines",
        name="y = x",
        line=dict(
            dash="dash"
        )
    )
)

fig.add_hline(
    y=0,
    line_dash="dash",
    opacity=0.5
)

fig.add_vline(
    x=0,
    line_dash="dash",
    opacity=0.5
)

fig.update_layout(
    title="Regresija k srednji vrednosti: 1. vs. 2. serija (FIS 2025/26)",
    xaxis_title="Odstopanje 1. serije od skakalčevega povprečja",
    yaxis_title="Odstopanje 2. serije od skakalčevega povprečja",
    width=1000,
    height=650,
    template="plotly_white"
)

fig.show()
