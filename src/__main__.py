import barplot
import pandas as pd
import os

root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
wtsnames = ["WT1", "WT2", "WT3", "WT4", "WT5", "WT6", "WT7","WT8","WT9"]

WTS = barplot.read_files(root, wtsnames)
KOS = barplot.read_files(root, kosnames)

# Create new folder named "Phyton_files"
path = os.path.join(root, "Phyton_files")
os.makedirs(path, exist_ok = True)

WTS_df = pd.DataFrame({
    "average.length.usv": barplot.aggregate(WTS, "mean"),
    "stdev.length.usv": barplot.aggregate(WTS, "stdev"),
    "total.calls": barplot.aggregate(WTS, "nrow"),
    "calls.per.minute": barplot.aggregate (WTS, "CPM")
})

KOS_df = pd.DataFrame({
    "average.length.usv": barplot.aggregate(KOS, "mean"),
    "stdev.length.usv": barplot.aggregate(KOS, "stdev"),
    "total.calls": barplot.aggregate(KOS, "nrow"),
    "calls.per.minute": barplot.aggregate(KOS, "CPM")
})

print(WTS_df)
print(KOS_df)
print(f"WTS group avg = {WTS_df['average.length.usv'].astype(float).mean():.6f}")
print(f"KOS group avg = {KOS_df['average.length.usv'].astype(float).mean():.6f}")

WTvsKO = pd.DataFrame({
    "Genotype": ["WT"]*len(WTS_df["average.length.usv"]) + ["KO"]*len(KOS_df["average.length.usv"]),
    "usv_length_mean": WTS_df["average.length.usv"].astype(float).tolist() + KOS_df["average.length.usv"].astype(float).tolist(),
    "usv_length_sem": WTS_df["stdev.length.usv"].astype(float).tolist() + KOS_df["stdev.length.usv"].astype(float).tolist(),
    "CPM_mean": WTS_df["calls.per.minute"].astype(float).tolist() + KOS_df["calls.per.minute"].astype(float).tolist()
})

WTvsKOsummary = pd.DataFrame({
    "Genotype": ["WT", "KO"],
    "usv_length_mean": [WTS_df['average.length.usv'].astype(float).mean(), KOS_df['average.length.usv'].astype(float).mean()],
    "usv_length_sem": [WTS_df['average.length.usv'].astype(float).sem(), KOS_df['average.length.usv'].astype(float).sem()],
    "CPM_mean": [WTS_df['calls.per.minute'].astype(float).mean(), KOS_df['calls.per.minute'].astype(float).mean()],
    "CPM_sem": [WTS_df['calls.per.minute'].astype(float).sem(), KOS_df['calls.per.minute'].astype(float).sem()]
})

print(WTvsKO)
print(WTvsKOsummary)
WTvsKO_path = os.path.join(root, "Phyton_files", "WTvsKO.xlsx")
WTvsKO.to_excel(WTvsKO_path, index = False)