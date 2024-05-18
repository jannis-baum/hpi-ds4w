from IPython.display import Markdown, display
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

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
