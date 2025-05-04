# Introduction
This notebook contains programs to calculate and compare the MAP (Mean Average Precision) and MRR (Mean Reciprocal Rank) values between different input files. It also includes visualizations for easier comparison.

# Instructions

## 📁 Folder Structure

Before getting started, please make sure to organize your files as follows:

```
data-analysis/
│
├── input/                  # Put your input files here according to the naming convention
│   └── input.sample-A
│   └── ...
│
├── QREL-file/              # Put your QREL (relevance judgment) file(s) here
│   └── qrel.sample.txt
│
├── data-analysis.ipynb     # Python notebook containing programs for analysis
├── README.md               # Project overview
└── .gitignore              # Files/folders to ignore in Git
```

> ✅ Ensure that both input files and QREL files are placed in the correct directories as shown above.

# 📦 Dependencies

Make sure you have the following installed:

1. Python (version 3.x recommended)

2. Required Python libraries:
- pandas
- seaborn
- matplotlib
- numpy

You can install them using pip:
```
pip install pandas seaborn matplotlib numpy
```