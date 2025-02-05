import pandas as pd
import os
from pathlib import Path
import statistics
import math
import scipy.stats

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
            pd.DataFrame: with a corrected index and the addition of the USV duration variable
        """
        df.drop(df.columns[[2]], axis=1, inplace=True)
        df.columns = ["start_time", "end_time"]
        df["duration_USV"] = (df.end_time - df.start_time)
        return df

    @staticmethod
    def CPM(g: list):
        """generate the variable calls per minute (CPM), dividing the total amount of calls per the duration of the recording (5 min)

        Args:
            g (list): a list of 'pd.DataFrame'

        Returns:
            float: a decimal number
        """
        if len(g) == 0:
            return 0.0
        return len(g)/5.
    
    @staticmethod
    def filter_nan_and_calculate_sem(data):
        filtered_data = [x for x in data if not math.isnan(x)]
        return scipy.stats.sem(filtered_data)

    def __aggregate(self, frames:pd.DataFrame, op:str):
        """perform the following operations to the pd.DataFrame: mean, standard deviation,
        number of rows, CPM (calls per minute), and the mean of "duration_USV"

        Args:
            frames (pd.DataFrame): pd.DataFrame that contains the values for the operations
            op (str): different operations
        """
        results = []
        lenframes = len(frames)
        for i in range(lenframes):
            duration_data = frames[i]["duration_USV"]
            if duration_data.empty or duration_data.isna().all():
                # If the duration data is empty or all values are NaN, set the result to 0
                results.append(0)
            elif len(duration_data) <2:
                if op == "sem":
                    results.append(float("NaN")) # Handle sem with insufficient data by returning NaN
                elif op == "mean" or "CPM":
                    # Handle the case with only one value or no value, return that value for "mean" or 0 for "CPM"
                    results.append(duration_data.iloc[0] if len(duration_data) == 1 else 0)
                else:
                    results.append(float("NaN")) # Handle cases with insufficient data for other operations by returning NaN
            else:
                if op == "mean":
                    results.append(statistics.mean(duration_data))
                elif op == "sem":
                    results.append(Summary.filter_nan_and_calculate_sem(duration_data)) # Use the filter_nan_and_calculate_sem static method
                elif op == "CPM":
                    results.append(Summary.CPM(duration_data))
        return(results)


    def create(self) -> pd.DataFrame:
        """Generate a summary of the data sets with 4 columns (average lenght USV, sem duration USV, total calls, and CPM)

        Returns:
            pd.DataFrame: DataFrame with the columns average lenght USV, sem duration USV, total calls, and CPM
        """
        dir_names = self.__read_files(self.root, self.filenames)
        summary_df = pd.DataFrame({
        "average.duration.usv": self.__aggregate(dir_names, "mean"),
        "sem.duration.usv": self.__aggregate(dir_names, "sem"),
        "calls.per.minute": self.__aggregate(dir_names, "CPM")
        })

        return summary_df
    
    @staticmethod
    def print(dataframe:pd.DataFrame, name:str):
        print(f"\033[1;4m{name}\033[0m\n", dataframe)
        print()
        print(f"\033[1;4m{name} group avg\033[0m = {dataframe['average.duration.usv'].astype(float).mean():.6f}")
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
        "Genotype": [name1]*len(group1["average.duration.usv"]) + [name2]*len(group2["average.duration.usv"]),
        "usv_duration_mean": group1["average.duration.usv"].astype(float).tolist() + group2["average.duration.usv"].astype(float).tolist(),
        "usv_duration_sem": group1["sem.duration.usv"].astype(float).tolist() + group2["sem.duration.usv"].astype(float).tolist(),
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
            "usv_duration_mean": [group1['average.duration.usv'].astype(float).mean(), group2['average.duration.usv'].astype(float).mean()],
            "usv_duration_sem": [group1['average.duration.usv'].astype(float).sem(), group2['average.duration.usv'].astype(float).sem()],
            "CPM_mean": [group1['calls.per.minute'].astype(float).mean(), group2['calls.per.minute'].astype(float).mean()],
            "CPM_sem": [group1['calls.per.minute'].astype(float).sem(), group2['calls.per.minute'].astype(float).sem()]
            })
        print("\033[1;4mWTSvsKO summary\033[0m\n", df)
        print()
        return df
    
    def save_group_data(self, dataframe:pd.DataFrame, name:str):
        """ Save comparison DataFrame in an excel file
        """
        self_path = os.path.join(self.root, "Python_files", f"{name}.xlsx")
        print(f"saving {name} data...")
        print()
        dataframe.to_excel(self_path, index = False)