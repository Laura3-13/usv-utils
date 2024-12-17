import os
import glob

def get_file_names(root, prefix): # to avoid writting the name of every single file
    pattern = os.path.join(root, prefix + "*.txt")
    files = glob.glob(pattern)
    return [os.path.splitext(os.path.basename(f))[0] for f in files if os.path.splitext(os.path.basename(f))[0].replace(prefix, "").isdigit()]