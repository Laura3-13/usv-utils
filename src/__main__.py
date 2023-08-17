import barplot
import pandas as pd

root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
wtsnames = ["WT1", "WT2", "WT3", "WT4", "WT5", "WT6", "WT7","WT8","WT9"]

WTS = barplot.read_files(root, wtsnames)
KOS = barplot.read_files(root, kosnames)

WTS_df = pd.DataFrame({
    "average.lenght.usv": barplot.aggregate(WTS, "mean"),
    "stdev.length.usv": barplot.aggregate(WTS, "stdev"),
    "total.calls": barplot.aggregate(WTS, "nrow"),
    "calls.per.minute": barplot.aggregate (WTS, "CPM")
})

KOS_df = pd.DataFrame({
    "average.length.usv": barplot.aggregate(KOS, "mean"),
    "stde.length.usv": barplot.aggregate(KOS, "stdev"),
    "total.calls": barplot.aggregate(KOS, "nrow"),
    "calls.per.minute": barplot.aggregate(KOS, "CPM")
})

print(len(WTS))
print(len(KOS))
print(kosnames[0])
print(KOS[0])
print(WTS_df)