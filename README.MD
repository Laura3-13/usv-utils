# USV-Utils: Mouse USV Analysis Library

A Phyton tool for processing and analyzing mouse ultrasonic vocalizations (USVs) extracted using **Avisoft-SASLab Pro** software. This library automatically processes USV data into meaningful statistics, such as **USV length**, **calls per minute**, and performs **statistical comparisons** between two experimental groups.


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
### **1. Add Your File Path in `__main__.py`**
Open the `__main__.py` file and change the variable `root` to point to your data folder:
```phyton
# Get your USV files from your path of choice
root = "INTRODUCE YOUR PATH HERE"
```

### **2. Run the Main Script**
Run the following command in your terminal:
```bash
phyton src/__main__.py
```


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
├── README.md                       # Project documentation and setup guide
└── .gitignore                      # Files and directories to ignore in Git
```


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