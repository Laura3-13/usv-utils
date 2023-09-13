import pandas as pd
import os
from scipy.stats import ttest_ind, levene, shapiro, mannwhitneyu

class Statistics():
    def __init__(self, root:str) -> None:
        self.root = root
        self.path = os.path.join(self.root, "Phyton_files")
        os.makedirs(self.path, exist_ok = True)
        self.t_stat = None
        self.p_value = None
        self.test_type = None
    
    def calculate(self, variable_measured:str, sample1: pd.Series, sample2: pd.Series):
        """Perform a test of normality (Spahiro-Wilk test), and then a t-test (standard or Welch's, according to Levene's test), or a Mann-Whitney U test

        Args:
            sample1 (pd.Series): first group/sample to compare with the t-test
            sample2 (pd.Series): second group/sample to compare with the t-test
        """
        print("\033[1;4mSTATISTICS\033[0m")
        # Test for normality
        shapiro_sample1 = shapiro(sample1)
        shapiro_sample2 = shapiro(sample2)
        alpha = 0.05 # Significance level
        if shapiro_sample1.pvalue < alpha or shapiro_sample2.pvalue < alpha:
            # If either group is not normally distributed, perform Mann-Whitney U test
            result = mannwhitneyu(sample1, sample2)
            self.t_stat = result.statistic
            self.p_value = result.pvalue
            self.test_type = "Mann-Whitney U test"
        else:
            # If both groups are normally distributed, use T-test or Welch's test
            # Test for equality of variances
            _, p_value_var = levene(sample1, sample2)
            # If p-value is less than significance level, assume unequal variances
            if p_value_var < 0.05:
                self.t_stat, self.p_value = ttest_ind(sample1, sample2, equal_var=False) # Welch's t-test
                self.test_type = "Welch's t-test"
            else:
                self.t_stat, self.p_value = ttest_ind(sample1, sample2, equal_var=True) # Standard t-test
                self.test_type = "Standard t-test"
        print(variable_measured)
        print("Test used:", self.test_type)
        print("t-statistic:", self.t_stat)
        print("p-value:", self.p_value)
        print()

    def save(self, file_name:str, variable_measured:str):
        """Save the statistics into a text file

        Args:
            file_name (str): Name of the file you want to save
            variable_measured (str): Name of the variable for which the statistics were done
        """
        print("saving statistics...")
        print()
        statistics_path = os.path.join(self.path, f"{file_name}.txt")
        with open(statistics_path, "w") as f:
            f.write(f"{variable_measured}\n")
            f.write(f"Test used: {self.test_type}\n")
            f.write(f"t-statistic: {self.t_stat}\n")
            f.write(f"p-value: {self.p_value}\n")