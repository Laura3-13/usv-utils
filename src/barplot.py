  
if __name__ == "__main__":
    print("testing")
    root =  "D:/laura/OneDrive - McGill University/Ph.D/IMPACT/USV files"
    kosnames = ["KO1", "KO2", "KO3", "KO4", "KO5", "KO6", "KO7", "KO8", "KO9"]
    kos = Summary.read_files(root, kosnames)

    group = pd.concat(kos).groupby("name")
    CPM = group.apply(Summary.CPM)
    print(CPM)