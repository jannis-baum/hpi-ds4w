from IPython.display import Markdown, display
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

# confusion matrix
def report_cm(title, y_true, y_pred, classifier):
    display(Markdown(f'# {title}'))
    print(f'accuracy: {accuracy_score(y_true, y_pred)}')
    ConfusionMatrixDisplay.from_predictions(
        y_true, y_pred,
        labels=classifier.classes_,
        normalize='true',
        xticks_rotation='vertical'
    )
    plt.show()

# pretty heatmap
# by default set to plot -log(p-value), adjust transform/legend args if using
# for something else
def pretty_hm(
    data, labels,
    transform = lambda x: -np.log(x + np.nextafter(0, 1)),
    legend='-log(p-value)', annot = True, cmap = 'flare'
):
    up_triang = np.triu(np.ones_like(data)).astype(bool)
    ax = sns.heatmap(
        transform(data) if transform else data,
        cmap=cmap, xticklabels=False, yticklabels=False,
        annot=annot, fmt='.0f',
        square=True, linecolor='white', linewidths=0.5,
        mask=up_triang,
        cbar=True if legend else False, cbar_kws={'shrink': 0.6, 'pad': 0.02, 'label': legend}
    )
    ax.invert_xaxis()
    for i, label in enumerate(labels):
        ax.text(i + 0.2, i + 0.5, label, ha='right', va='center')

# transform internal labels into presentable labels
# (capitalize first letter & make underscores into spaces)
def pretty_str(string):
    return (string[0].upper() + string[1:]).replace('_', ' ')
