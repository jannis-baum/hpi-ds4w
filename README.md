# Climbing Hold Recognition With Electromyography Data

This repository contains the supporting code for our Data Science for Wearables
project of the summer term 2024 at HPI.

## Overview

- the scripts [`record_data.py`](record_data.py) and
  [`prepare_data.py`](prepare_data.py) are used to record new EMG data along
  with a video for later labelling, and to prepare and aggregate a dataset based
  on the manual labels, respectively
- the [`analysis/`](analysis) directory contains Jupyter notebooks for
  statistical analysis and data exploration
- the [`models/`](models) directory contains Jupyter notebooks for
  training and evaluating models used to classify climbing holds
- the [`script/`](script) directory contains Python code that supports the
  mentioned scripts and notebooks

## Setup

1. create a Python environment with the version according to `.python-version`
2. install the `requirements.txt`, e.g. with `pip install -r requirements.txt`
