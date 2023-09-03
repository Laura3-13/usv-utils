import barplot
import pandas as pd
import os

root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
wtsnames = ["WT1", "WT2", "WT3", "WT4", "WT5", "WT6", "WT7","WT8","WT9"]

kos = barplot.Summary(root, kosnames)
KOS_df = kos.generate_summary()

wts = barplot.Summary(root, wtsnames)
WTS_df = wts.generate_summary()

# Create new folder named "Phyton_files"
path = os.path.join(root, "Phyton_files")
os.makedirs(path, exist_ok = True)

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
print()
WTvsKO_path = os.path.join(root, "Phyton_files", "WTvsKO.xlsx")
WTvsKO.to_excel(WTvsKO_path, index = False)

# Separate the WTvsKO data based on the Genotype
WT_usv_length = WTvsKO[WTvsKO["Genotype"] == "WT"]["usv_length_mean"]
KO_usv_length = WTvsKO[WTvsKO["Genotype"] == "KO"]["usv_length_mean"]
WT_CPM = WTvsKO[WTvsKO["Genotype"] == "WT"]["CPM_mean"]
KO_CPM = WTvsKO[WTvsKO["Genotype"] == "KO"]["CPM_mean"]

print("\033[1;4mSTATISTICS\033[0m")
t_stat, p_value, test_type = barplot.perform_statistics(WT_usv_length, KO_usv_length)
print("USV length")
print("Test used:", test_type)
print("t-statistic:", t_stat)
print("p-value:", p_value)
print()

t_stat, p_value, test_type = barplot.perform_statistics(WT_CPM, KO_CPM)
print("CPM")
print("Test used:", test_type)
print("t-statistics:", t_stat)
print("p-value:", p_value)
print()