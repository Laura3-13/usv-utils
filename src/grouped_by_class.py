import data_workflow_vocalmat
import statistical_analysis
import plotting
import utils
import os

root =  "D:/laura/OneDrive - McGill University/Ph.D/Shank3/Shank3 New Tests/USV/USV adult females and males/USV females excel files"
kosnames = utils.get_excel_file_names(root, "KO")
wtsnames = utils.get_excel_file_names(root, "WT")

# Get unique classes from the "Class" column
classes = kosnames["Class"].unique()

# Initialize dataframes to store results
all_wts_df = []
all_kos_df = []

for class_name in classes:
    class_data_ko = kosnames[kosnames["Class"] == class_name]
    class_data_wt = wtsnames[wtsnames["Class"] == class_name]
    kos = data_workflow_vocalmat.Summary(root, kosnames)
    KOS_df = kos.create()
    wts = data_workflow_vocalmat.Summary(root, wtsnames)
    WTS_df = wts.create()
    # Appends the results to the list
    all_kos_df.append(KOS_df)
    all_wts_df.append(WTS_df)

    # Perform statistics and plotting separately for each class
    WT_KO = data_workflow_vocalmat.Join_summary()
    WTvsKO = WT_KO.group_data(WTS_df, KOS_df, "WT", "KO")
    WTvsKOsummary = WT_KO.calculate_mean_by_group(WTS_df, KOS_df, "WT", "KO")

    # Separate the WTvsKO data based on the Genotype
    WT_usv_length = WTvsKO[WTvsKO["Genotype"] == "WT"]["usv_length_mean"]
    KO_usv_length = WTvsKO[WTvsKO["Genotype"] == "KO"]["usv_length_mean"]
    WT_CPM = WTvsKO[WTvsKO["Genotype"] == "WT"]["CPM_mean"]
    KO_CPM = WTvsKO[WTvsKO["Genotype"] == "KO"]["CPM_mean"]

    # For USV length
    usv_length_stats = statistical_analysis.Statistics(root)
    usv_length_stats.calculate("USV length", WT_usv_length, KO_usv_length)
    usv_length_stats.save("USV_length_statistics", "USV length")
    # For CPM
    CPM_stats = statistical_analysis.Statistics(root)
    CPM_stats.calculate("CPM", WT_CPM, KO_CPM)
    CPM_stats.save("CPM_statistics", "CPM")

    # Create barplots
    usv_length_plot_path = os.path.join(root, "Python_files", f"USV_length_{class_name}.png")
    usv_length_plot = plotting.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["usv_length_mean"], WTvsKOsummary["usv_length_sem"], WTvsKO["Genotype"], WTvsKO["usv_length_mean"], "USV length (s)", usv_length_plot_path)
    CPM_plot_path = os.path.join(root, "Python_files", f"CPM_{class_name}.png")
    CPM_plot = plotting.plot_barplot(WTvsKO, WTvsKOsummary["Genotype"], WTvsKOsummary["CPM_mean"], WTvsKOsummary["CPM_sem"], WTvsKO["Genotype"], WTvsKO["CPM_mean"], "Calls per minute", CPM_plot_path)