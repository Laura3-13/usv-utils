import matplotlib.pylab as plt
import pandas as pd
from pathlib import Path

def read_files(basedir:str, names: list[str]) -> list[pd.DataFrame]:
    print("reading files...")
    basedir = Path(basedir)
    frames = []
    for name in names:
        filename = name + ".txt"
        df = diff_time(pd.read_csv(basedir / filename, sep="\t"))
        df["name"] = name
        frames.append(df)
    return frames

def process(dataframes: list[pd.DataFrame]):
    return []

def diff_time(df: pd.DataFrame) -> pd.DataFrame:
      df.drop(df.columns[[2]], axis=1, inplace=True)
      df.columns = ["start_time", "end_time"]
      df["length_USV"] = (df.end_time - df.start_time)
      return df

def plot_barplot():
    raise NotImplementedError("The function is under construction")

def cpm(g):
    return len(g)/5.

if __name__ == "__main__":
    print("testing")
    root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
    kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
    kos = read_files(root, kosnames)

    group = pd.concat(kos).groupby("name")
    cpm = group.apply(cpm)
    print(cpm)


