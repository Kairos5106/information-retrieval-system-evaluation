## Introduction

This notebook contains programs to calculate and compare the MAP and MRR values between different input files. There are visualizations and 

## Instructions

### Before getting started, please be sure to have these files:
1. A set of input files
2. A QREL file/relevance judgment

> Make sure that (1) and (2) are placed according to the folder structure below:
data-analysis/
│
├── input/              
│   └── input.sample-A      # put your input files here according the naming convention
│ 
├── QREL-file               # Put your QREL file here.
├── README.md               # Project overview
├── README.md               # Project overview
└── .gitignore              # Files/folders to ignore in Git

### Make sure to have these dependencies too
1. Python
2. Some Python libraries:
  - pandas
  - seaborn
  - matplotlib
  - numpy