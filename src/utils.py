import os
import glob

def get_file_names(root, prefix): # to avoid writting the name of every single file
    pattern = os.path.join(root, prefix + "*.txt")
    files = glob.glob(pattern)
    return [os.path.splitext(os.path.basename(f))[0] for f in files if os.path.splitext(os.path.basename(f))[0].replace(prefix, "").isdigit()]

def get_excel_file_names(basedir, prefix):
        file_names = []
        for filename in os.listdir(basedir):
            if filename.startswith(prefix):
                file_names.append(filename.split('.')[0])  # Remove the file extension
        return file_names