# ESCI 451-Python

Test status: [![CircleCI](https://circleci.com/gh/calum-chamberlain/GPHS445_notebooks.svg?style=svg)](https://circleci.com/gh/calum-chamberlain/ESCI451-Python)

You can run these notebooks on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/calum-chamberlain/ESCI451-Python/master)

## Introduction to Python for VUW ESCI 451 course (Active Earth). 
Designed to be a 1-day workshop, first run in March 2020.

These notebooks aim to get students with no previous computing experience to a point where they can
automate simple data I/O and processing, as well as conduct some simple plotting.  These notebooks
do not aim to teach you the nuances of Python as a language, or any advanced ideas in Python.

The notebooks are as follows:

0. Introduction to Python; - why programming, reproducibility, keeping data and processing seperate.
1. Python logic - for loops and if statements;
2. Functions, classes and methods;
3. Plotting data with matplotlib (1); - simple plotting of lists, required for visualisation of data later
4. Simple data IO and processing with Numpy; - read from text-file, slice, add, divide, etc.
5. Meta-data and data IO with Pandas; - read data from xls sheets, get someones dataset from them, play
6. More plotting with matplotlib;
7. Geoscience data wrangling: play with some fun data;
8. Mini-project, get climate data and plot it and uncertainity - point students towards [this page](https://towardsdatascience.com/time-series-analysis-and-climate-change-7bb4371021e) for extensions.

## Getting started

To run these notebooks locally you will need to install the required Python packages. If you are taking
this as a course at VUW this should have been done for you.  Otherwise, install the required packages
listed in the `environment.yml` file using conda:

```bash
conda create env -f environment.yml
conda activate esci451
```
