# Statistical Assumptions and Parametric Audits

This document defines the core assumptions of parametric statistical tests and outlines how to handle assumption violations.

## 1. Assumption of Normality
Most parametric tests (such as the t-test and ANOVA) assume that the data in each group is normally distributed.
*   **How to Test**: Use the **Shapiro-Wilk test**. A p-value greater than .05 indicates that the data is not significantly different from a normal distribution (Assumption PASSED).
*   **Handling Violations**:
    *   **Small Samples (N < 30)**: If normality is violated, transition to a non-parametric alternative:
        *   Alternative to Independent t-test: **Mann-Whitney U test**.
        *   Alternative to Dependent t-test: **Wilcoxon Signed-Rank test**.
        *   Alternative to One-Way ANOVA: **Kruskal-Wallis test**.
    *   **Large Samples (N >= 30)**: Due to the Central Limit Theorem (CLT), parametric tests are robust to normality violations if the sample size is large enough.

## 2. Assumption of Homogeneity of Variance
Parametric tests comparing groups assume that the groups have approximately equal variances (homoscedasticity).
*   **How to Test**: Use **Levene's test**. A p-value greater than .05 indicates that group variances are equal (Assumption PASSED).
*   **Handling Violations**:
    *   For **t-tests**: Use **Welch's t-test** (set equal_var = False in scipy), which adjusts the degrees of freedom and standard error to account for unequal variances.
    *   For **ANOVA**: Use **Welch's ANOVA** paired with **Games-Howell post-hoc tests** instead of standard Tukey HSD.

## 3. Assumption of Independence
Observations must be independent of one another (the value of one observation does not influence another).
*   **How to Test**: Review study design. For time-series or sequential data, use the **Durbin-Watson statistic** to check for autocorrelation (ideal values are between 1.5 and 2.5).
*   **Handling Violations**: Use repeated-measures designs, mixed-effects models, or generalized estimating equations (GEE).
