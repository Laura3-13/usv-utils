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
WT_usv_length = WTvsKO[WTvsKO["Genotype"] == "WT"]["usv_length_mean"]
KO_usv_length = WTvsKO[WTvsKO["Genotype"] == "KO"]["usv_length_mean"]
WT_CPM = WTvsKO[WTvsKO["Genotype"] == "WT"]["CPM_mean"]
KO_CPM = WTvsKO[WTvsKO["Genotype"] == "KO"]["CPM_mean"]

# For USV length
usv_length_stats = statistical_analysis.Statistics(root)
usv_length_stats.calculate("USV length", WT_usv_length, KO_usv_length)
usv_length_stats.save("USV_length_statistics", "USV length")
usv_length_stats_results = usv_length_stats.get_results()
# For CPM
CPM_stats = statistical_analysis.Statistics(root)
CPM_stats.calculate("CPM", WT_CPM, KO_CPM)
CPM_stats.save("CPM_statistics", "CPM")
CPM_stats_results = CPM_stats.get_results()

# Create barplots
usv_length_plot_path = os.path.join(root, "Python_files", "USV_length.png")
usv_length_plot = plotting.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["usv_length_mean"], WTvsKOsummary["usv_length_sem"], WTvsKO["Genotype"], WTvsKO["usv_length_mean"], "USV length (s)", usv_length_plot_path)
CPM_plot_path = os.path.join(root, "Python_files", "CPM.png")
CPM_plot = plotting.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["CPM_mean"], WTvsKOsummary["CPM_sem"], WTvsKO["Genotype"], WTvsKO["CPM_mean"], "Calls per minute", CPM_plot_path)