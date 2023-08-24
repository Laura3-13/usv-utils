import matplotlib.pylab as plt
import pandas as pd
from pathlib import Path
import statistics
from scipy.stats import ttest_ind, levene

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

def perform_ttest(sample1, sample2):
    """Perform a t-test, standard or Welch's according to Levene's test

    Args:
        sample1 (pd.series): first group/sample to compare with the t-test
        sample2 (pd.series): second group/sample to compare with the t-test
    """
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

def plot_barplot():
    raise NotImplementedError("The function is under construction")

if __name__ == "__main__":
    print("testing")
    root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
    kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
    kos = read_files(root, kosnames)

    group = pd.concat(kos).groupby("name")
    CPM = group.apply(CPM)
    print(CPM)