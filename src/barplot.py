import matplotlib.pylab as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
import statistics
from scipy.stats import ttest_ind, levene, shapiro, mannwhitneyu

def read_files(basedir:str, names: list[str]) -> list[pd.DataFrame]:
    """read files containing in names from basedir. Files are tabular
    without a header with extension "*.txt"

    Args:
        basedir (str): root directory
        names (list[str]): list of file names, extension is appended

    Returns:
        list[pd.DataFrame]: a list containing `pd.DataFrame`
    """
    print("reading files...")
    basedir = Path(basedir)
    frames = []
    for name in names:
        filename = name + ".txt"
        df = diff_time(pd.read_csv(basedir / filename, sep="\t", header=None))
        df["name"] = name
        frames.append(df)
    return frames

def process(dataframes: list[pd.DataFrame]):
    return []

def diff_time(df: pd.DataFrame) -> pd.DataFrame:
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

def CPM(g: list):
    """generate the variable calls per minute (CPM), dividing the total amount of calls per the duration of the recording (5 min)

    Args:
        g (list): a list of 'pd.DataFrame'

    Returns:
        float: a decimal number
    """
    return len(g)/5.

def aggregate(frames:pd.DataFrame, op:str):
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
        operation = CPM
    for i in range(lenframes):
        means.append(operation(frames[i]["length_USV"]))
    return(means)

class Summary():
    def __init__(self, root, names) -> None:
        self.root = root
        self.filenames = names

    def generate_summary(self) -> pd.DataFrame:
        dir_names = read_files(self.root, self.filenames)
        summary_df = pd.DataFrame({
        "average.length.usv": aggregate(dir_names, "mean"),
        "stdev.length.usv": aggregate(dir_names, "stdev"),
        "total.calls": aggregate(dir_names, "nrow"),
        "calls.per.minute": aggregate(dir_names, "CPM")
        })

        return summary_df

def perform_statistics(sample1, sample2):
    """Perform a test of normality (Spahiro-Wilk test), and then a t-test (standard or Welch's, according to Levene's test), or a Mann-Whitney U test

    Args:
        sample1 (pd.series): first group/sample to compare with the t-test
        sample2 (pd.series): second group/sample to compare with the t-test
    """
    # Test for normality
    shapiro_sample1 = shapiro(sample1)
    shapiro_sample2 = shapiro(sample2)
    alpha = 0.05 # Significance level
    if shapiro_sample1.pvalue < alpha or shapiro_sample2.pvalue < alpha:
        # If either group is not normally distributed, perform Mann-Whitney U test
        result = mannwhitneyu(sample1, sample2)
        t_stat = result.statistic
        p_value = result.pvalue
        test_type = "Mann-Whitney U test"
    else:
        # If both groups are normally distributed, use T-test or Welch's test
        # Test for equality of variances
        stat, p_value_var = levene(sample1, sample2)
        # If p-value is less than significance level, assume unequal variances
        if p_value_var < 0.05:
            t_stat, p_value = ttest_ind(sample1, sample2, equal_var=False) # Welch's t-test
            test_type = "Welch's t-test"
        else:
            t_stat, p_value = ttest_ind(sample1, sample2, equal_var=True) # Standard t-test
            test_type = "Standard t-test"
    return(t_stat, p_value, test_type)

def plot_barplot(data, x_axis, y_axis, sem_values, x_axis_2, individual_points, save_path, y_label):
    """Create a barplot with error bars and individual points, and save it as a file

    Args:
        data (pd.DataFrame): data frame of the data for the graph
        x_axis (pd.Series): groups for the x axis for the bars
        y_axis (pd.Series): length of the y axis (mean)
        sem_values (pd.Series): sem of the y axis for error bars
        x_axis_2 (pd.Series): groups of the x axis for the individual points
        individual_points (pd.Series): individual values
        save_path (str): path directory (where to save the graphs)
        y_label (str): name for the y axis
    """
    fig, ax = plt.subplots()
    ax = sns.barplot(x = x_axis, y = y_axis, data = data, palette = "Blues", errorbar = None)
    # Manually adding error bars:
    for i, sem in enumerate(sem_values):
        ax.errorbar(i, y_axis.iloc[i], yerr = sem, fmt = "none", capsize = 5, color = "black")
    # Add indiviual data points
    for i, category in enumerate(x_axis.unique()): # Assuming x_axis is a column in data with unique categories
        y_values = individual_points[x_axis_2 == category]
        x_values = [i]*len(y_values) # x-axis position repeated for all individual points
        ax.scatter(x_values, y_values, color = "black")
    # Show the plot in its original size
    original_size = fig.get_size_inches()
    plt.draw()
    plt.pause(0.001) # Pause for a moment to allow the draw to take place
    input("Press any key to continue...")
    # Setting figure size and font sizes
    fig.set_size_inches(20,12)
    ax.tick_params(axis = 'x', labelsize = 14)  # Increase x-axis tick labels size
    ax.tick_params(axis = 'y', labelsize = 14)  # Increase y-axis tick labels size
    ax.set_xlabel(x_axis.name, fontsize = 16)  # Increase x-axis label size
    ax.set_ylabel(y_axis.name, fontsize = 16, labelpad = 20)  # Increase y-axis label size
    # Set title and x and y axis labels
    ax.set_xlabel("Genotype")
    ax.set_ylabel(y_label)
    # Save the plot
    fig.savefig(save_path)
    # Reset to original size
    fig.set_size_inches(original_size)
    
if __name__ == "__main__":
    print("testing")
    root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
    kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
    kos = read_files(root, kosnames)

    group = pd.concat(kos).groupby("name")
    CPM = group.apply(CPM)
    print(CPM)