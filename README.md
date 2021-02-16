# ESCI 451-Python

Test status: ![test](https://github.com/calum-chamberlain/ESCI451-Python/workflows/test/badge.svg)

You can run these notebooks on [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/calum-chamberlain/ESCI451-Python/master)

## Introduction to Python for VUW ESCI 451 course (Active Earth). 
Designed to be a 4 half-day workshops, first run in March 2020.

These notebooks aim to get students with no previous computing experience to a point where they can
automate simple data I/O and processing, as well as conduct some simple plotting.  These notebooks
do not aim to teach you the nuances of Python as a language, or any advanced ideas in Python.

The notebooks are as follows:

1A. Introduction to Python; - why programming, reproducibility, keeping data and processing seperate.
1B. Python logic - for loops and if statements, basic data types, getting data;
2A. Loading and Plotting data;
2B. Introduction to NumPy;
3A. Pandas and higher-dimension data;
3B. Time-series;
4A. Basic map making;
4B. Working with gridded data.

## Getting started

To run these notebooks locally you will need to install the required Python packages. If you are taking
this as a course at VUW this should have been done for you.  Otherwise, you will need an anaconda or
miniconda installation.  To get miniconda follow the [instructions here](https://docs.conda.io/en/latest/miniconda.html).

Then install the required packages listed in the `environment.yml` file using conda:

```bash
conda create env -f environment.yml
conda activate esci451
```
