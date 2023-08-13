import barplot

root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
wtsnames = ["WT1", "WT2", "WT3", "WT4", "WT5", "WT6", "WT7","WT8","WT9"]

wts = barplot.read_files(root, wtsnames)
kos = barplot.read_files(root, kosnames)



print(len(wts))
print(len(kos))
print(kosnames[0])
print(kos[0])