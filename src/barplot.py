import matplotlib.pylab as plt
import pandas as pd
from pathlib import Path

def read_files(basedir:str, names: list[str]) -> list[pd.DataFrame]:
    print("reading files...")
    basedir = Path(basedir)
    frames = []
    for name in names:
        filename = name + ".txt"
        df = pd.read_csv(basedir / filename, sep="\t")
        frames.append(df)
    return frames

def process(dataframes: list[pd.DataFrame]):
    return []

def plot_barplot():
    raise NotImplementedError("The function is under construction")

if __name__ == "__main__":
    print("testing")
    plot_barplot()

