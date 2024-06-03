# Data Science for Wearables project

Overview of files:

- [`record_data.py`](record_data.py) connects to the Myo and records
  data & video for labelling
- [`prepare_data.py`](prepare_data.py) uses raw recorded data, and CSV/Excel
  files of manually annotated frame boundaries to create labelled, aggregated
  and calibrated data
- [`tsne.ipynb`](tsne.ipynb) runs t-SNE dimensionality reduction to visualize
  labelled data
- [`feasibility-study.ipynb`](feasibility-study.ipynb) hypothesis testing on
  sensor distributions for different holds
