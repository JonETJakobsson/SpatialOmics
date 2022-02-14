import sys
from PyQt5.QtWidgets import QWidget, QTabWidget, QApplication, QVBoxLayout
from PyQt5.QtGui import QFont
from widgets import loadGenesWidget
from dataset import Dataset
from napari import Viewer


h1 = QFont("Arial", 13)


# Main widget presents the tabs and can provide other global tools
class mainWidget(QWidget):
    def __init__(self, dataset: Dataset, viewer: Viewer):
        super().__init__()
        self.dataset = dataset
        self.viewer = viewer
        self.initUI()

    def initUI(self):

        # Widgets will be added vertically
        layout = QVBoxLayout(self)

        # Create tabs with names to access induvidual widgets
        self.tabs = QTabWidget()
        self.tabs.addTab(loadGenesWidget(self.dataset, self.viewer), "select columns")

        # Add all widgets in order
        layout.addWidget(self.tabs)

        # Set layout on mainWidget
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo = mainWidget("dataset", "viewer")
    demo.show()

    sys.exit(app.exec_())