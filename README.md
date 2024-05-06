# Data Science for Wearables project

Overview of files:

- [`data_collection.py`](data_collection.py) connects to the Myo and records
  data & video for labelling
- [`labelling.py`](labelling.py) uses a CSV of manually annotated frame
  boundaries to create labelled data
- [`tsne.ipynb`](tsne.ipynb) runs t-SNE dimensionality reduction to visualize
  labelled data
- [`rf-all.ipynb`](rf-all.ipynb) trains a Random Forest classifier for holds on
  a given split of all data and evaluates it
- [`rf-omitting-person.ipynb`](rf-omitting-person.ipynb) trains a Random Forest
  classifier for holds on all but one person and then evaluates it on the person
  it has never seen
