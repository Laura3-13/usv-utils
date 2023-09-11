import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from pathlib import Path
import statistics
from scipy.stats import ttest_ind, levene, shapiro, mannwhitneyu

class Summary():
    def __init__(self, root, names) -> None:
        self.root = root
        self.filenames = names
        self.path = os.path.join(self.root, "Python_files")
        os.makedirs(self.path, exist_ok = True)
    
    def __read_files(self, basedir:str, names: list[str]) -> list[pd.DataFrame]:
        """read files containing in names from basedir. Files are tabular without a header with extension "*.txt"
        
        Args:
            basedir (str): root directory
            names (list[str]): list of file names, extension is appended

        Returns:
            list[pd.DataFrame]: a list containing `pd.DataFrame`
        """
        print("reading files...")
        print()
        basedir = Path(basedir)
        frames = []
        for name in names:
            filename = name + ".txt"
            df = self.__diff_time(pd.read_csv(basedir / filename, sep="\t", header=None))
            df["name"] = name
            frames.append(df)
        return frames

    def __diff_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """change the index to "start_time" and "end_time" of the USV, and calculate the USV lenght using these two values

        Args:
            df (pd.DataFrame): the 'pd.DataFrame' of the original files

        Returns:
            pd.DataFrame: with a corrected index and the addition of the USV length variable
        """
        df.drop(df.columns[[2]], axis=1, inplace=True)
        df.columns = ["start_time", "end_time"]
        df["length_USV"] = (df.end_time - df.start_time)
        return df

    @staticmethod
    def CPM(g: list):
        """generate the variable calls per minute (CPM), dividing the total amount of calls per the duration of the recording (5 min)

        Args:
            g (list): a list of 'pd.DataFrame'

        Returns:
            float: a decimal number
        """
        return len(g)/5.

    def __aggregate(self, frames:pd.DataFrame, op:str):
        """perform the following operations to the pd.DataFrame: mean, standard deviation,
        number of rows, CPM (calls per minute), and the mean of "length_USV"

        Args:
            frames (pd.DataFrame): pd.DataFrame that contains the values for the operations
            op (str): different operations
        """
        means = list()
        lenframes = len(frames)
        if op == "mean":
            operation = statistics.mean
        elif op == "stdev":
            operation = statistics.stdev
        elif op == "nrow":
            operation = lambda df: df.shape[0]
        elif op == "CPM":
            operation = Summary.CPM
        for i in range(lenframes):
            means.append(operation(frames[i]["length_USV"]))
        return(means)


    def create(self) -> pd.DataFrame:
        """Generate a summary of the data sets with 4 columns (average lenght USV, stdev length USV, total calls, and CPM)

        Returns:
            pd.DataFrame: DataFrame with the columns average lenght USV, stdev length USV, total calls, and CPM
        """
        dir_names = self.__read_files(self.root, self.filenames)
        summary_df = pd.DataFrame({
        "average.length.usv": self.__aggregate(dir_names, "mean"),
        "stdev.length.usv": self.__aggregate(dir_names, "stdev"),
        "total.calls": self.__aggregate(dir_names, "nrow"),
        "calls.per.minute": self.__aggregate(dir_names, "CPM")
        })

        return summary_df
    
    @staticmethod
    def print(dataframe:pd.DataFrame, name:str):
        print(f"\033[1;4m{name}\033[0m\n", dataframe)
        print()
        print(f"\033[1;4m{name} group avg\033[0m = {dataframe['average.length.usv'].astype(float).mean():.6f}")
        print()
    
class Join_summary():
    def group_data(self, group1:pd.DataFrame, group2:pd.DataFrame, name1:str, name2:str)-> pd.DataFrame:
        """Join data of both groups together

        Args:
            group1 (pd.DataFrame): pd.DataFrame of group1
            group2 (pd.DataFrame): pd.DataFrame of group2
            name1 (str): name of group 1
            name2 (str): name of group2

        Returns:
            pd.DataFrame: pd.DataFrame of both groups together
        """
        df = pd.DataFrame({
        "Genotype": [name1]*len(group1["average.length.usv"]) + [name2]*len(group2["average.length.usv"]),
        "usv_length_mean": group1["average.length.usv"].astype(float).tolist() + group2["average.length.usv"].astype(float).tolist(),
        "usv_length_sem": group1["stdev.length.usv"].astype(float).tolist() + group2["stdev.length.usv"].astype(float).tolist(),
        "CPM_mean": group1["calls.per.minute"].astype(float).tolist() + group2["calls.per.minute"].astype(float).tolist()
        })
        print("\033[1;4mWTSvsKO\033[0m\n", df)
        print()
        return df
    
    def calculate_mean_by_group(self, group1:pd.DataFrame, group2:pd.DataFrame, name1:str, name2:str) -> pd.DataFrame:
        """Average and standard error of the mean of each group

        Args:
            group1 (pd.DataFrame): pd.DataFrame of group1
            group2 (pd.DataFrame): pd.DataFrame of group2
            name1 (str): name of group 1
            name2 (str): name of group2

        Returns:
            pd.DataFrame: pd.DataFrame with the average and standard error of the mean of each group
        """
        df = pd.DataFrame({
            "Genotype": [name1, name2],
            "usv_length_mean": [group1['average.length.usv'].astype(float).mean(), group2['average.length.usv'].astype(float).mean()],
            "usv_length_sem": [group1['average.length.usv'].astype(float).sem(), group2['average.length.usv'].astype(float).sem()],
            "CPM_mean": [group1['calls.per.minute'].astype(float).mean(), group2['calls.per.minute'].astype(float).mean()],
            "CPM_sem": [group1['calls.per.minute'].astype(float).sem(), group2['calls.per.minute'].astype(float).sem()]
            })
        print("\033[1;4mWTSvsKO summary\033[0m\n", df)
        print()
        return df
    
    def save_group_data(self, dataframe:pd.DataFrame, name:str):
        """ Save comparison DataFrame in an excel file
        """
        self_path = os.path.join(root, "Python_files", f"{name}.xlsx")
        print(f"saving {name} data...")
        print()
        dataframe.to_excel(self_path, index = False)

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

def plot_barplot(data: pd.DataFrame, x_axis: pd.Series, y_axis: pd.Series, sem_values: pd.Series, x_axis_2: pd.Series, individual_points: pd.Series, y_label: str, save_path:str):
    """Create a barplot with error bars and individual points, and save it as a file

    Args:
        data (pd.DataFrame): data frame of the data for the graph
        x_axis (pd.Series): groups for the x axis for the bars
        y_axis (pd.Series): length of the y axis (mean)
        sem_values (pd.Series): sem of the y axis for error bars
        x_axis_2 (pd.Series): groups of the x axis for the individual points
        individual_points (pd.Series): individual values
        y_label (str): name for the y axis
        save_path (str): path to the directory to save the files
    """    
    fig, ax = plt.subplots()
    ax = sns.barplot(x = x_axis, y = y_axis, data = data, palette = "Blues", errorbar = None)
    # Manually adding error bars:
    for i, sem in enumerate(sem_values):
        ax.errorbar(i, y_axis.iloc[i], yerr = sem, fmt = "none", capsize = 5, color = "black")
    # Add indiviual data points
    for i, category in enumerate(x_axis.unique()): # Assuming x_axis is a column in data with unique categories
        y_values = individual_points[x_axis_2 == category]
        x_values = np.random.normal(loc = i, scale = 0.1, size = (len(y_values))) # random jitter (0.1) for all individual points (not spread on a straight line)
        ax.scatter(x_values, y_values, color = "black")
    # Set title and x and y axis labels
    ax.set_xlabel("Genotype")
    ax.set_ylabel(y_label)
    # Show and save the plot
    plt.show()
    print("saving graph...")
    fig.savefig(save_path, dpi=300)
    
if __name__ == "__main__":
    print("testing")
    root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
    kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
    kos = Summary.read_files(root, kosnames)

    group = pd.concat(kos).groupby("name")
    CPM = group.apply(Summary.CPM)
    print(CPM)