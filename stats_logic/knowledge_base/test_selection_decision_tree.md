# Statistical Test Selection Matrix and Decision Tree

Use this decision matrix to determine the most appropriate statistical test based on the research objective, data types, and group counts.

## 1. Comparing Group Means (Inference)
Use these rules to select comparison tests:
*   **Two Independent Groups (Interval/Ratio Data)**:
    *   Assumptions met: **Independent Samples t-test** (parametric).
    *   Assumptions violated or ordinal data: **Mann-Whitney U test** (non-parametric).
*   **Two Dependent/Paired Groups (Interval/Ratio Data)**:
    *   Assumptions met: **Dependent/Paired Samples t-test** (parametric).
    *   Assumptions violated or ordinal data: **Wilcoxon Signed-Rank test** (non-parametric).
*   **Three or More Independent Groups (Interval/Ratio Data)**:
    *   Assumptions met: **One-Way ANOVA** (parametric).
    *   Assumptions violated or ordinal data: **Kruskal-Wallis test** (non-parametric).

## 2. Analyzing Relationships and Associations
Use these rules for association testing:
*   **Two Continuous/Interval Variables**:
    *   Linear relationship expected: **Pearson Correlation ($r$)**.
    *   Non-linear relationship or ordinal/skewed data: **Spearman Rank Correlation ($\rho$)**.
*   **Two Categorical/Nominal Variables**:
    *   Checking for independence/association: **Chi-Square Test of Independence ($\chi^2$)** (or Fisher's Exact Test for small sample frequencies < 5).

## 3. Predictive Modeling and Forecasting
Use these rules for predictive analytical models:
*   **Predicting a Continuous outcome from one or more predictors**:
    *   Use **Linear Regression** (checks coefficients, residuals, and overall $R^2$ model fit).
*   **Predicting a Binary/Categorical outcome from one or more predictors**:
    *   Use **Logistic Regression** (predicts probabilities of classification classes, outputs odds ratios).
*   **Predicting a multi-class outcome**:
    *   Use **Multinomial Logistic Regression** or Multi-Class Classifier.
