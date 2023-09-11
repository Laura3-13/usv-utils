import barplot
import pandas as pd
import os
import matplotlib.pylab as plt

root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
wtsnames = ["WT1", "WT2", "WT3", "WT4", "WT5", "WT6", "WT7","WT8","WT9"]

kos = barplot.Summary(root, kosnames)
KOS_df = kos.create()

wts = barplot.Summary(root, wtsnames)
WTS_df = wts.create()

barplot.Summary.print(WTS_df, "WTS_df")
barplot.Summary.print(KOS_df, "KOS_df")

WT_KO = barplot.Join_summary()
WTvsKO = WT_KO.group_data(WTS_df, KOS_df, "WT", "KO")
WTvsKOsummary = WT_KO.calculate_mean_by_group(WTS_df, KOS_df, "WT", "KO")

# Separate the WTvsKO data based on the Genotype
WT_usv_length = WTvsKO[WTvsKO["Genotype"] == "WT"]["usv_length_mean"]
KO_usv_length = WTvsKO[WTvsKO["Genotype"] == "KO"]["usv_length_mean"]
WT_CPM = WTvsKO[WTvsKO["Genotype"] == "WT"]["CPM_mean"]
KO_CPM = WTvsKO[WTvsKO["Genotype"] == "KO"]["CPM_mean"]

# For USV length
usv_length_stats = barplot.Statistics(root)
usv_length_stats.calculate("USV length", WT_usv_length, KO_usv_length)
usv_length_stats.save("USV_length_statistics", "USV length")
# For CPM
CPM_stats = barplot.Statistics(root)
CPM_stats.calculate("CPM", WT_CPM, KO_CPM)
CPM_stats.save("CPM_statistics", "CPM")

# Create barplots
usv_length_plot_path = os.path.join(root, "Python_files", "USV_length.png")
usv_length_plot = barplot.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["usv_length_mean"], WTvsKOsummary["usv_length_sem"], WTvsKO["Genotype"], WTvsKO["usv_length_mean"], "USV length (s)", usv_length_plot_path)
CPM_plot_path = os.path.join(root, "Python_files", "CPM.png")
CPM_plot = barplot.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["CPM_mean"], WTvsKOsummary["CPM_sem"], WTvsKO["Genotype"], WTvsKO["CPM_mean"], "Calls per minute", CPM_plot_path)