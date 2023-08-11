import barplot

root = "home"

wts_names = ["WT1", "WT2"]
kos_names = ["KO1", "KO2"]

wts = barplot.read_files(root, wts_names)
kos = barplot.read_files(root, kos_names)