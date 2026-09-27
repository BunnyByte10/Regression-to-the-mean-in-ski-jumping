import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.stats import t as t_dist


df = pd.read_csv("season_2025_26.csv")


# Average of all other rounds by the same jumper
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


print("REGRESSION RESULTS")
print("------------------")
print(f"Correlation (r): {rezultat.rvalue:.6f}")
print(f"Slope: {rezultat.slope:.6f}")
print(f"Intercept: {rezultat.intercept:.6f}")
print(f"R²: {rezultat.rvalue ** 2:.6f}")
print(f"p-value for slope ≠ 0: {rezultat.pvalue:.6e}")


n = len(x)
df_degrees = n - 2

t_stat = (
    (rezultat.slope - 1)
    / rezultat.stderr
)

p_less_than_1 = t_dist.cdf(
    t_stat,
    df=df_degrees
)

print()
print("TEST OF SLOPE < 1")
print("-----------------")
print(f"t-statistic: {t_stat:.6f}")
print(f"p-value for slope < 1: {p_less_than_1:.6e}")


min_val = min(x.min(), y.min())
max_val = max(x.max(), y.max())

margin = (max_val - min_val) * 0.05

x_min = min_val - margin
x_max = max_val + margin


# Points for the regression line
x_line = np.linspace(x_min, x_max, 100)
y_line = (
    rezultat.slope * x_line
    + rezultat.intercept
)


plt.figure(figsize=(10, 6))

plt.scatter(
    x,
    y,
    alpha=0.3,
    s=20,
    color="blue"
)

plt.plot(
    x_line,
    y_line,
    color="red",
    label=f"Regression (β = {rezultat.slope:.2f})"
)

plt.plot(
    [x_min, x_max],
    [x_min, x_max],
    color="green",
    linestyle="--",
    alpha=0.7,
    label="y = x"
)

plt.axhline(
    0,
    color="black",
    linestyle="--",
    alpha=0.5
)

plt.axvline(
    0,
    color="black",
    linestyle="--",
    alpha=0.5
)

plt.title(
    "Regression to the Mean: 1st vs. 2nd Round (FIS 2025/26)"
)

plt.xlabel(
    "1st-round deviation from jumper's average"
)

plt.ylabel(
    "2nd-round deviation from jumper's average"
)

plt.legend()
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.show()
