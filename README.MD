# USV-Utils: Mouse USV Analysis Library

A Phyton tool for processing and analyzing mouse ultrasonic vocalizations (USVs) extracted using **Avisoft-SASLab Pro** software. This library automatically processes USV data into meaningful statistics, such as **USV length** and **calls per minute**, and performs **statistical comparisons** between two experimental groups.


---


## 🎯 **Key Features**
- 📃 **USV Data Classification**: Calculates USV length and calls per minute (CPM).
- 📊 **Statistical Analysis**: Performs automated statistical tests between two groups.
- 📂 **File Management**: Automatically reads USV text files from specified folders.
- ⚙️ **Automation Ready**: Minimal setup - just provide the path and run the main script.


---


## 💻 **Installation Guide**

### **Option 1. Clone the Repository Using Git (Recommended)**
1. **Clone the Repository**
```bash
git clone https://github.com/Laura3-13/usv-utils.git
cd usv-utils # This is the folder created after cloning
```

2. **Create a Conda Environment**
``` bash
conda create -n usv-utils python=3.10
```

3. **Activate the Environment**
``` bash
conda activate usv-utils
```

4. **Install Required Libraries**
``` bash
pip install '-r' requirements.txt
```

---


### **Option 2. Download the Repository as a ZIP File**
1. **Download the Repository**
- Visit the [USV-Utils GitHub Repository](https://github.com/Laura3-13/usv-utils).
- Click the green **Code** button.
- Select **Download ZIP**.

2. **Extract the ZIP File**
- Extract the contents to a folder on your computer.

3. **Navigate to the Extracted Folder**
```bash
cd path_to_extracted_folder/usv-utils # Replace "path_to_extracted_folder" with your actual folder path
```

4. **Create a Conda Environment**
```bash
conda create -n usv-utils python=3.10
```

5. **Activate the Environment**
```bash
conda activate usv-utils
```

6. **Install Required Libraries**
```bash
pip install '-r' requirements.txt
```


---


## 📦 **How to Use**
### **1. Organize Your Data Files**
The script is design to compare **two groups**. By default, the groups are:
- **WT** (Wild-type)
- **KO** (Knockout)

However, you can replace **WT** and **KO** with other group names (e.g., `GroupA` and `GroupB`), as long as the files follow this structure:
- Each group name must be consistent and followed by **numbers**.

### **File Naming Rules**
Your files must follow this naming convention:
- `GroupName1.txt`, `GroupName2.txt`...

**Example:**

- For **WT** and **KO**:
```bash
WT1.txt, WT2.txt, WT3.txt, KO1.txt, KO2.txt, KO3.txt
```
- For other groups, such as **GroupA** and **GroupB**:
```bash
GroupA1.txt, GroupA2.txt, GroupA3.txt, GroupB1.txt, GroupB2.txt, GroupB3.txt, 
```
Ensure all **USV text files** are stored in a single folder.

### **2. Add Your File Path in `__main__.py`**
Open the `__main__.py` file and change the variable `root` to point to your folder containing the USV files:
```phyton
# Get your USV files from your path of choice
root = "INTRODUCE YOUR PATH HERE"

# Change group names here if needed
kosnames = utils.get_file_names(root, "KO") # Replace "KO" with your group name
wtsnames = utils.get_file_names(root, "WT") # Replace "WT" with your group name
```
If you cahnge `KO` and `WT` to other names (e.g., `GroupA` and `GroupB`), make sure your filenames match this new naming scheme.

### **3. Run the Main Script**
Run the following command in your terminal:
```bash
phyton src/__main__.py
```
### **4. Output**
The script will perform the following tasks:
1. **Read** and **process** the USV files for both groups.
2. **Generate summary data:**
    - **USV length** (mean and SEM).
    - **Calls per minute** (CPM).
3. **Print the summaries** to the terminal for both groups.
4. **Provide comparisons** (Group1 vs Group2) with statistical analysis.
5. **Save results** as files in a folder called `Python_files`:
    - **Excel files:** Summary data for each group and combined results.
    - **Statistical Results:** A **text file** containing the statistical test results.
    - **Bar graphs:** two **bar graph images** (one for **USV length** and one for **Calls per minute**).

### **Notes**
- The text files should have **two columns** (start time and end time of each USV call).
- The third column will be ignored automatically.
- The script assumes a **5-minute recording duration** to calculate "calls per minute (CPM)".


---


## 📄 **Expected Input Data Format**
- **Avisoft-SASLab Pro** USV files (Tab-separated ``.txt`` files):
    - **Column 1:** Start Time (seconds)
    - **Column 2:** End Time (seconds)
    - **Column 3:** *Empty Column*


---


## 📑 **Project Structure**
```bash
usv-utils/
│
├── src/                            # Main source code
│   ├── __init__.py                 # Marks this directory as a Python package
│   ├── __main__.py                 # RUN THIS FILE
│   ├── data_workflow.py            # Data processing and summary generation
│   ├──statistical_analysis.py      # Statistical tests (t-test, Mann-Whitney, etc.)
│   ├── plotting.py                 # Plotting functions for barplots
│   └── utils.py                    # Utility functions to fetch file names
│
├── requirements.txt                # Required libraries for the project
├── citation.ris                    # Citation file for importing into reference managers
├── README.md                       # Project documentation and setup guide
└── .gitignore                      # Files and directories to ignore in Git
```


---


## 🖋️ **Citation**

If you use this repository in your research or projects, please cite it appropriately!

On the right side of this GitHub page, you'll find a **Cite this repository** section where you can copy citations in:
- **APA** format
- **BibTeX** format (for LaTeX users)

For other reference managers, such as **EndNote**, **Zotero**, or **Mendeley**, download the `citation.ris` file directly from the repository.


---


## 🐭 **How It works**
1. **Load USV Files:** Extract USV start and end times from Avisoft-SASLab Pro text files.
2. **Process Data:** Calculate USV length and calls per minute (CPM).
3. **Perform Statistical Analysis:**
    - **Compare two groups:** Automatically calculates mean, standard deviation, and performs significance tests.


---


## 🔬 **About the Project**
This library was developed for **neuroscience research** involving the analysis of mouse ultrasonic vocalizations (USVs). It supports efficient batch processing, automatic statistical tests, and data visualization for **behavioral experiments**.


---