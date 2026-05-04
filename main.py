from stats_logic.descriptive import result as desc_result
# from stats_logic.hypothesis_testing import t_test, z_test
from stats_logic.linear_regression import result as linear_result
from stats_logic.anova import anova
from stats_logic.confidence_intervals import two_pop_CI, dep_data, two_samp_prop
from datasets import descriptive_set, linear_set, anova_set, two_pops, dep_data_set, two_samp_prop_set

def main():
    print("Welcome to the Statistics Application!")
    # Here you can initialize data and call various statistical functions as needed.
    
    # Example usage of descriptive statistics
    for data in descriptive_set:
        desc_result(data)

    # # Example usage of hypothesis testing
    # before = [56, 69, 48, 74, 65, 71, 60]
    # after = [62, 73, 44, 85, 71, 70, 73]
    # print("Hypothesis Testing (t-test):")
    # print(t_test(before, after))

    # Example usage of regression
    for data in linear_set:
        linear_result(data)

    # Example usage of ANOVA
    for data in anova_set:
        print(anova(data))
        print('------------------------')

    # Example usage of confidence intervals
    for data in two_pops:
        print(two_pop_CI(data))
        print('------------------------')

    for data in dep_data_set:
        print(dep_data(data))
        print('------------------------')

    for data in two_samp_prop_set:
        print(two_samp_prop(data))
        print('------------------------')

if __name__ == "__main__":
    main()