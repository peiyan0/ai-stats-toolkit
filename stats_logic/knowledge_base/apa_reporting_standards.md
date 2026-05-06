# APA 7th Edition Reporting Standards

This document outlines the formal APA 7th Edition guidelines for reporting key statistical results. Use these templates to ground AI generation in professional research standards.

## 1. Independent Samples t-Test
When reporting an independent t-test, include the degrees of freedom (df), the t-statistic, the p-value, and the effect size (Cohen's d).
*   **Template**: "An independent-samples t-test was conducted to compare [Variable] in [Group 1] and [Group 2]. There was a significant difference in the scores for [Group 1] (M = [Mean1], SD = [SD1]) and [Group 2] (M = [Mean2], SD = [SD2]); t(df) = [t_stat], p = [p_value], d = [cohens_d]."
*   **Significance Guidelines**: 
    *   If p < .05: Report as "p = .XXX" or "p < .001".
    *   If p > .05: Report as "p = .XXX" and describe as not statistically significant.

## 2. One-Way ANOVA (Analysis of Variance)
Include the between-groups and within-groups degrees of freedom, the F-statistic, the p-value, and the effect size (Eta-squared $\eta^2$).
*   **Template**: "A one-way ANOVA was conducted to compare the effect of [Factor] on [Dependent Variable]. There was a significant effect of [Factor] on [Dependent Variable] for the [Number of groups] groups; F(df_between, df_within) = [F_test], p = [p_value], eta_squared = [eta_sq]."
*   **Post-Hoc Example**: "Tukey's HSD post-hoc test revealed that [Group 1] was significantly different from [Group 2] (p < .05)."

## 3. Simple & Multiple Linear Regression
Include the overall model fit ($R^2$, adjusted $R^2$, $F$-test), and individual coefficients ($\beta$ weights, $t$-values, and $p$-values).
*   **Overall Model Template**: "A simple linear regression was calculated to predict [Dependent Variable] based on [Independent Variable]. A significant regression equation was found (F(df_model, df_residual) = [F_val], p = [p_val]), with an R² of [r_sq]."
*   **Predictor Template**: "[Predictor] was a significant predictor of [Dependent Variable], beta = [coefficient], t(df) = [t_stat], p = [p_val]."

## 4. Logistic Regression
Include the Wald chi-square test, the odds ratio (OR) or Exp(B), and the confidence intervals for the OR.
*   **Template**: "A logistic regression was performed to analyze the relationship between [Predictors] and the probability of [Outcome]. The overall model was statistically significant, chi-square(df) = [chi_val], p = [p_val]. The odds of [Outcome] increased by [OR] for every unit increase in [Predictor] (OR = [OR], 95% CI [[lower], [upper]], p = [p_val])."

## 5. Descriptive Statistics
Always report the sample size ($N$), the mean ($M$), and the standard deviation ($SD$).
*   **Template**: "[Variable Name] had a mean score of [M] (SD = [SD], N = [N])."
