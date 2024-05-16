# Data Science for Wearables project

Overview of files:

- [`data_collection.py`](data_collection.py) connects to the Myo and records
  data & video for labelling
- [`labelling.py`](labelling.py) uses a CSV of manually annotated frame
  boundaries to create labelled data
- [`aggregate_data.py`](aggregate_data.py) aggregates labelled data into one CSV
  file
- [`tsne.ipynb`](tsne.ipynb) runs t-SNE dimensionality reduction to visualize
  labelled data
- [`rf-classifier.ipynb`](rf-all.ipynb) example of using a Random Forest to
  classify holds
- [`feasibility-study.ipynb`](feasibility-study.ipynb) hypothesis testing on
  sensor distributions for different holds
