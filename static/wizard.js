/**
 * AI Statistical Wizard - Logic and Data Matrix
 * Optimised for caching, fast rendering, and modular maintainability.
 */

const messages = [
    "Consulting the statistical oracle...",
    "Negotiating with the Null Hypothesis...",
    "Polishing the bell curve...",
    "Checking p-values for cosmic significance...",
    "Ensuring our data is organic and locally sourced...",
    "Avoiding Type II errors in the quantum realm...",
    "Asking the Normal Distribution for its expert opinion...",
    "Searching for hidden correlations in the static...",
    "Applying Laplace transforms to your curiosity..."
];

const WIZARD_MATRIX = {
  "compare_means": {
    "continuous": {
      "1": {
        test: "One-Sample t-test",
        desc: "Compares your single sample's mean against a known or hypothesized population mean to see if there is a statistically significant difference."
      },
      "2": {
        test: "Independent Samples t-test / Paired t-test",
        desc: "Compares the means of two groups. Use Independent t-test if groups are distinct (e.g., Treatment vs Control), or Paired t-test if matching the same subjects before and after."
      },
      "3+": {
        test: "One-Way ANOVA / Kruskal-Wallis Test",
        desc: "Compares means across three or more groups. Use ANOVA if your data satisfies normality assumptions, otherwise utilize Kruskal-Wallis as a robust non-parametric fallback."
      }
    },
    "categorical": {
      "1": {
        test: "Chi-Square Goodness-of-Fit Test",
        desc: "Compares observed category frequencies in a single variable against an expected theoretical distribution."
      },
      "2": {
        test: "Chi-Square Test of Independence",
        desc: "Compares frequency counts across two categorical groups to see if an association or correlation exists between them."
      },
      "3+": {
        test: "Chi-Square Test of Independence (Multi-way)",
        desc: "Analyzes the frequency distribution and associations across three or more categorical dimensions or groups."
      }
    },
    "binary": {
      "1": {
        test: "One-Sample Z-Test for Proportions / Binomial Test",
        desc: "Compares the proportion of successes in a single binary sample to a hypothesized constant (such as testing if a coin is fair, p=0.5)."
      },
      "2": {
        test: "Two-Sample Z-Test for Proportions",
        desc: "Compares the success rates or proportions between two independent binary groups (e.g., conversion rate in group A vs. group B)."
      },
      "3+": {
        test: "Chi-Square Test of Independence (R x C)",
        desc: "Compares binary proportions across three or more groups to determine if the probability of success is uniform."
      }
    }
  },
  "find_relationship": {
    "continuous": {
      "1": {
        test: "Descriptive Trend Analysis",
        desc: "Analyzing relationships requires at least two variables. With one continuous variable, analyze descriptive metrics like variance and trend lines over time."
      },
      "2": {
        test: "Pearson / Spearman Correlation",
        desc: "Measures the strength and direction of the relationship between two continuous variables (Pearson for linear data, Spearman for non-linear or skewed data)."
      },
      "3+": {
        test: "Partial Correlation / Correlation Matrix",
        desc: "Computes a matrix of correlation coefficients between multiple continuous variables, optionally controlling for the influence of other variables."
      }
    },
    "categorical": {
      "1": {
        test: "Descriptive Frequency Profiling",
        desc: "Relationships require at least two variables. With one categorical variable, describe the frequency counts and percentage distribution of categories."
      },
      "2": {
        test: "Chi-Square Test of Independence",
        desc: "Evaluates whether there is a statistically significant association or dependence between two separate categorical variables."
      },
      "3+": {
        test: "Log-Linear Analysis",
        desc: "Examines the relationship between three or more categorical variables, testing for multi-way interactions and joint dependencies."
      }
    },
    "binary": {
      "1": {
        test: "Binary Proportion Profiling",
        desc: "Relationships require at least two variables. With one binary variable, profile the baseline probability and success/failure ratios."
      },
      "2": {
        test: "Phi Coefficient / Fisher's Exact Test",
        desc: "Measures the strength of association between two binary variables, using Fisher's Exact Test if sample frequencies are low (< 5)."
      },
      "3+": {
        test: "Cochran's Q Test / Log-Linear Analysis",
        desc: "Tests for differences or associations among three or more related binary variables or matched groups."
      }
    }
  },
  "predict_outcome": {
    "continuous": {
      "1": {
        test: "Simple Linear Regression",
        desc: "Predicts the value of a continuous dependent outcome variable based on a single continuous or binary predictor variable."
      },
      "2": {
        test: "Multiple Linear Regression (2 Predictors)",
        desc: "Models and predicts a continuous outcome using two independent predictor variables to assess their individual and joint impacts."
      },
      "3+": {
        test: "Multiple Linear Regression (3+ Predictors)",
        desc: "Predicts a continuous outcome from three or more predictor variables, checking for multicollinearity and model fit (R²)."
      }
    },
    "categorical": {
      "1": {
        test: "Simple Multinomial Logistic Regression",
        desc: "Predicts a nominal multi-class categorical outcome based on a single predictor variable."
      },
      "2": {
        test: "Multinomial Logistic Regression (2 Predictors)",
        desc: "Models and predicts a multi-class categorical outcome based on two separate predictor variables."
      },
      "3+": {
        test: "Multinomial Logistic Regression (3+ Predictors)",
        desc: "Predicts a multi-class categorical outcome using three or more predictor variables to determine classification odds ratios."
      }
    },
    "binary": {
      "1": {
        test: "Simple Logistic Regression",
        desc: "Predicts the probability of a binary outcome (e.g., yes/no, success/failure) based on a single predictor variable."
      },
      "2": {
        test: "Multiple Logistic Regression (2 Predictors)",
        desc: "Predicts the probability of a binary outcome using two independent predictor variables to evaluate their joint odds ratios."
      },
      "3+": {
        test: "Multiple Logistic Regression (3+ Predictors)",
        desc: "Predicts the probability of a binary outcome from three or more predictors, adjusting for potential confounding variables."
      }
    }
  },
  "describe_data": {
    "continuous": {
      "1": {
        test: "Univariate Descriptive Statistics",
        desc: "Calculates the central tendency (Mean, Median, Mode) and dispersion (Standard Deviation, Variance, Range, IQR) for a single continuous variable."
      },
      "2": {
        test: "Bivariate Descriptive Statistics",
        desc: "Summarizes two continuous variables side-by-side, calculating independent means, standard deviations, and basic covariance."
      },
      "3+": {
        test: "Multivariate Data Profiling",
        desc: "Creates a summary table of means, standard deviations, and distributions across multiple continuous variables simultaneously."
      }
    },
    "categorical": {
      "1": {
        test: "Frequency Distribution",
        desc: "Summarizes a single categorical variable by presenting the absolute count and percentage frequency distribution for each unique category."
      },
      "2": {
        test: "Cross-tabulation (2-Way Contingency Table)",
        desc: "Summarizes the joint frequency distribution of two categorical variables, illustrating how categories overlap."
      },
      "3+": {
        test: "Multi-Way Cross-tabulation Table",
        desc: "Generates multi-dimensional contingency tables to summarize counts and frequencies across three or more categorical variables."
      }
    },
    "binary": {
      "1": {
        test: "Binary Proportion Summary",
        desc: "Summarizes a single binary variable, calculating counts, baseline rates, percentages (e.g., % Yes vs. % No), and error bounds."
      },
      "2": {
        test: "2x2 Contingency Table",
        desc: "Summarizes joint frequencies for two binary variables, commonly displaying rates in a standard 2x2 grid layout."
      },
      "3+": {
        test: "Multi-way Contingency Table / Joint Probabilities",
        desc: "Summarizes the frequencies and ratios across three or more binary variables to analyze conditional success rates."
      }
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('wizard-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const loading = document.getElementById('loading-state');
            const result = document.getElementById('result-container');
            const msgEl = document.getElementById('loading-msg');
            
            form.style.display = 'none';
            loading.style.display = 'block';
            
            // Choose a random whimsical message for this run
            const randomIndex = Math.floor(Math.random() * messages.length);
            msgEl.innerText = messages[randomIndex];
            
            // Inputs
            const goal = document.getElementById('goal').value;
            const data_type = document.getElementById('data_type').value;
            const groupsVal = parseInt(document.getElementById('groups').value, 10) || 1;
            
            // Group classification mapping (1, 2, or 3+)
            let groupKey = "3+";
            if (groupsVal === 1) {
                groupKey = "1";
            } else if (groupsVal === 2) {
                groupKey = "2";
            }
            
            // Retrieve recommendation instantly from our local matrix
            let recommendationHtml = "";
            try {
                const match = WIZARD_MATRIX[goal][data_type][groupKey];
                recommendationHtml = `<h4><strong>Recommended Test:</strong> <span style="color: var(--accent);">${match.test}</span></h4><p class="mt-3" style="font-size: 1.1rem; line-height: 1.6;">${match.desc}</p>`;
            } catch (err) {
                recommendationHtml = `<h4><strong>Recommended Test:</strong> <span style="color: var(--accent);">Standard Statistical Analysis</span></h4><p class="mt-3">Please review general statistical guidance for your variables.</p>`;
            }
            
            // Snappy micro-loading experience (1500ms) to enjoy the beautiful pulse animation without frustration
            setTimeout(() => {
                loading.style.display = 'none';
                result.style.display = 'block';
                document.getElementById('recommendation-text').innerHTML = recommendationHtml;
            }, 1500);
        });
    }
});

function resetWizard() {
    document.getElementById('result-container').style.display = 'none';
    document.getElementById('loading-state').style.display = 'none';
    document.getElementById('wizard-form').style.display = 'block';
}
