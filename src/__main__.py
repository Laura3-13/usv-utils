import data_workflow
import statistical_analysis
import plotting
import utils
import os

# Get your USV files from your path of choice
root =  "INTRODUCE YOUR PATH HERE"

# Change group names here if needed
kosnames = utils.get_file_names(root, "KO") # Replace "KO" with your group name
wtsnames = utils.get_file_names(root, "WT") # Replace "WT" with your group name

kos = data_workflow.Summary(root, kosnames)
KOS_df = kos.create()

wts = data_workflow.Summary(root, wtsnames)
WTS_df = wts.create()

data_workflow.Summary.print(WTS_df, "WTS_df")
data_workflow.Summary.print(KOS_df, "KOS_df")

WT_KO = data_workflow.Join_summary()
WTvsKO = WT_KO.group_data(WTS_df, KOS_df, "WT", "KO")
WTvsKOsummary = WT_KO.calculate_mean_by_group(WTS_df, KOS_df, "WT", "KO")
print("saving WTvsKO file...")
WTvsKO_path = os.path.join(root, "Python_files", "WTvsKO.xlsx")
WTvsKO.to_excel(WTvsKO_path)

# Separate the WTvsKO data based on the Genotype
WT_usv_duration = WTvsKO[WTvsKO["Genotype"] == "WT"]["usv_duration_mean"]
KO_usv_duration = WTvsKO[WTvsKO["Genotype"] == "KO"]["usv_duration_mean"]
WT_CPM = WTvsKO[WTvsKO["Genotype"] == "WT"]["CPM_mean"]
KO_CPM = WTvsKO[WTvsKO["Genotype"] == "KO"]["CPM_mean"]

# For USV duration
usv_duration_stats = statistical_analysis.Statistics(root)
usv_duration_stats.calculate("USV duration", WT_usv_duration, KO_usv_duration)
usv_duration_stats.save("USV_duration_statistics", "USV duration")
usv_duration_stats_results = usv_duration_stats.get_results()
# For CPM
CPM_stats = statistical_analysis.Statistics(root)
CPM_stats.calculate("CPM", WT_CPM, KO_CPM)
CPM_stats.save("CPM_statistics", "CPM")
CPM_stats_results = CPM_stats.get_results()

# Create barplots
usv_duration_plot_path = os.path.join(root, "Python_files", "USV_duration.png")
usv_duration_plot = plotting.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["usv_duration_mean"], WTvsKOsummary["usv_duration_sem"], WTvsKO["Genotype"], WTvsKO["usv_duration_mean"], "USV duration (s)", usv_duration_plot_path)
CPM_plot_path = os.path.join(root, "Python_files", "CPM.png")
CPM_plot = plotting.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["CPM_mean"], WTvsKOsummary["CPM_sem"], WTvsKO["Genotype"], WTvsKO["CPM_mean"], "Calls per minute", CPM_plot_path)