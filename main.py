from stats_logic.descriptive import get_full_analysis
from stats_logic.hypothesis_testing import two_sample_t_test
from stats_logic.linear_regression import linear_regression
from stats_logic.anova import anova
from stats_logic.confidence_intervals import two_pop_CI, dep_data, two_samp_prop
from datasets import descriptive_set, linear_set, anova_set, two_pops, dep_data_set, two_samp_prop_set

def main():
    print("Welcome to the Statistics Application!")
    # Here you can initialize data and call various statistical functions as needed.
    
    # Example usage of descriptive statistics
    for data in descriptive_set:
        print("Descriptive Analysis:")
        print(get_full_analysis(data))
        print('------------------------')

    # Example usage of hypothesis testing
    before = [56, 69, 48, 74, 65, 71, 60]
    after = [62, 73, 44, 85, 71, 70, 73]
    print("Hypothesis Testing (two-sample t-test):")
    print(two_sample_t_test(before, after))
    print('------------------------')

    # Example usage of regression
    for data in linear_set:
        print("Linear Regression Analysis:")
        print(linear_regression(data[0], data[1]))
        print('------------------------')

    # Example usage of ANOVA
    for data in anova_set:
        print("ANOVA Analysis:")
        print(anova(data))
        print('------------------------')

    # Example usage of confidence intervals
    for data in two_pops:
        print("Two Population Confidence Interval:")
        print(two_pop_CI(data))
        print('------------------------')

    for data in dep_data_set:
        print("Dependent Data Analysis:")
        print(dep_data(data))
        print('------------------------')

    for data in two_samp_prop_set:
        print("Two Sample Proportion Analysis:")
        print(two_samp_prop(data))
        print('------------------------')

if __name__ == "__main__":
    main()