# Regression to the Mean in Ski Jumping

A small data analysis project exploring regression to the mean in ski jumping using FIS World Cup data from the 2025/26 season.

## Inspiration

The idea for this project was inspired by Daniel Kahneman's book *Thinking, Fast and Slow*, particularly Chapter 17, *Regression to the Mean*.

Kahneman describes an example from the Israeli Air Force, where flight instructors noticed that exceptionally good performances were often followed by worse performances, while unusually poor performances were often followed by better ones. The instructors interpreted this as an effect of praise and punishment. Kahneman used the example to explain that this pattern can instead arise naturally from regression to the mean and random variation in performance.

This made me curious whether a similar pattern could be observed in ski jumping: when a jumper performs unusually well or poorly in the first round, does their performance tend to move closer to their usual level in the second round?

## Research question

Do ski jumpers who perform unusually well or poorly in the first round tend to move closer to their usual level in the second round?

## Data

The dataset contains results from the 2025/26 FIS Ski Jumping World Cup season. Each row represents one ski jumper in one competition.

The dataset has the following columns:

| Column     | Description                  |
| ---------- | ---------------------------- |
| `date`     | Competition date             |
| `location` | Competition location         |
| `codex`    | FIS competition code         |
| `rank`     | Rank in the competition      |
| `bib`      | Bib number                   |
| `name`     | Ski jumper's name            |
| `nation`   | Ski jumper's country         |
| `series1`  | Score in the first round     |
| `series2`  | Score in the second round    |
| `total`    | Total score from both rounds |

The data was collected from the FIS website.

## Method

For each competition, a jumper's average score was calculated using all of their other rounds in the dataset, excluding both rounds from the current competition.

Missing second-round results were not treated as zero. Competitions where a jumper did not have a second-round result were excluded from the regression analysis.

The following variables were then calculated:

* `dif1` = first-round score − jumper's average
* `dif2` = second-round score − jumper's average

A linear regression was used to examine the relationship between `dif1` and `dif2`.

The regression line was compared with the diagonal `y = x`, which represents the case where the deviation stays exactly the same between the two rounds.

## Results

| Measure               |       Result |
| --------------------- | -----------: |
| Correlation (r)       |        0.713 |
| Slope (β)             |        0.653 |
| Intercept             |        0.419 |
| R²                    |        0.509 |
| p-value for slope ≠ 0 | 7.43 × 10⁻⁸¹ |
| p-value for slope < 1 | 1.16 × 10⁻³⁰ |

The regression slope was between 0 and 1, which is consistent with a regression-to-the-mean pattern: deviations from a jumper's usual level tended to be smaller in the second round than in the first.
## Findings

The analysis shows a clear positive relationship between how far a jumper's first-round score is from their usual level and how far their second-round score is from that level.

The correlation between the two deviations is **r = 0.713**, indicating that jumpers who perform above their usual level in the first round tend to remain above it in the second round, while jumpers who perform below their usual level tend to remain below it. However, the relationship is not one-to-one.

The estimated regression slope is **β = 0.653**. This means that, on average, a 1-point deviation from a jumper's usual level in the first round is associated with a deviation of about **0.65 points in the same direction** in the second round. The regression line is therefore substantially flatter than the `y = x` line, which represents an unchanged deviation.

For example, a hypothetical jumper who scores 10 points above their usual level in the first round would be predicted to score about 6.9 points above their usual level in the second round, according to the regression model:

$$
dif2 = 0.653 \cdot dif1 + 0.419
$$

Similarly, a large negative deviation in the first round is expected to be less negative in the second round.

The **R² of 0.509** means that around 51% of the variation in second-round deviation is explained by the linear relationship with first-round deviation in this dataset.

The p-value for the regression slope being different from zero is extremely small (**p < 0.001**), indicating that the observed relationship is unlikely to be explained by random sampling variation alone under the assumptions of the test.

The one-sided test of whether the slope is smaller than 1 also gives a very small p-value (**p < 0.001**). Together with the estimated slope of 0.653, this indicates that the second-round deviations are, on average, smaller than the first-round deviations.

Overall, the results are **consistent with regression to the mean**: unusually high or low first-round performances tend to be followed by performances that are closer to the jumper's usual level in the second round. The analysis does not, however, show that regression to the mean is the only reason for this pattern.

## Limitations

This project is intended as a small exploratory analysis rather than a definitive statistical study.

First, the jumper's average is calculated using all of their other rounds in the dataset, including competitions that happened after the current one. This makes the average useful for measuring deviation from an overall season level, but it should not be interpreted as information that would have been available before each competition.

Second, the analysis only includes jumpers who completed both rounds. Jumpers who did not qualify for the second round are therefore excluded from the regression, which means the results do not describe all first-round performances.

The same jumpers also appear in multiple competitions, so individual observations are not completely independent. The analysis does not account for this repeated-measures structure.

The dataset covers only the 2025/26 season, so the findings may not generalize to other seasons. In addition, ski-jumping scores are affected by factors such as wind conditions, gate changes and other competition conditions, which are not separately modeled here.

Finally, the analysis shows a statistical pattern consistent with regression to the mean, but it does not establish a causal explanation for why performance changes between rounds.

## Files

* `season_2025_26.csv` — dataset (Raw data omitted; sourced from official FIS results.)
* `regression.py` — data preparation, regression analysis and visualization
* `index.html` — interactive version of the plot

### Visualization

The [interactive graph]() shows the relationship between first-round and second-round deviations from a jumper's average. The regression line is shown together with the diagonal `y = x` for comparison.

## Technologies

* Python
* Pandas
* NumPy
* SciPy
* Matplotlib
* Plotly
* GitHub Pages

## References

Kahneman, D. (2011). *Thinking, Fast and Slow*. Chapter 17: "Regression to the Mean".
