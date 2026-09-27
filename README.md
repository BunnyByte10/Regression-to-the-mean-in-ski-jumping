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

## Limitations

This project is intended as a small exploratory analysis rather than a definitive statistical study.

First, the jumper's average is calculated using all of their other rounds in the dataset, including competitions that happened after the current one. This makes the average useful for measuring deviation from an overall season level, but it should not be interpreted as information that would have been available before each competition.

Second, the analysis only includes jumpers who completed both rounds. Jumpers who did not qualify for the second round are therefore excluded from the regression, which means the results do not describe all first-round performances.

The same jumpers also appear in multiple competitions, so individual observations are not completely independent. The analysis does not account for this repeated-measures structure.

The dataset covers only the 2025/26 season, so the findings may not generalize to other seasons. In addition, ski-jumping scores are affected by factors such as wind conditions, gate changes and other competition conditions, which are not separately modeled here.

Finally, the analysis shows a statistical pattern consistent with regression to the mean, but it does not establish a causal explanation for why performance changes between rounds.

## Files

* `season_2025_26.csv` — dataset
* `regression.py` — data preparation, regression analysis and visualization
* `index.html` — interactive version of the plot

## Visualization

The interactive graph shows the relationship between first-round and second-round deviations from a jumper's average.

The regression line is shown together with the diagonal `y = x` for comparison.

## References

Kahneman, D. (2011). *Thinking, Fast and Slow*. Chapter 17: "Regression to the Mean".
