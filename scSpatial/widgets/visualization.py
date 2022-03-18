import plotly.express as px
import pandas as pd
import imageio
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import numpy as np
from vispy.color.colormap import Colormap, MatplotlibColormap

import sys

from ..dataset import Dataset
from ..viewer import Viewer
from ..analysis import Bonefight



class visualizationWidget(QWidget):
    """Widget used to color objects by different features
    (currently gene expression and cell type)"""

    def __init__(self, dataset: Dataset, viewer: Viewer):
        super().__init__()
        self.dataset = dataset
        self.viewer = viewer
        self.initUI()

    def initUI(self):

        # Set when to update visualization options
        # When active segmentation is set
        self.dataset.com.active_segmentation_changed.connect(self.populate_options)
        
        # When changes are made to a segmentations cell_types
        self.dataset.com.cell_types_changed.connect(self.populate_options)

        # Gene selection list
        self.gene_combo = QComboBox(self)
        # When gene is selected
        #self.gene_combo.currentTextChanged.connect(self.color_genes)
        self.add_gene_btn = QPushButton("Add gene")
        self.add_gene_btn.clicked.connect(self.add_gene)

        # Cell type selection list
        self.cell_type_combo = QComboBox(self)
        # When cell type is selected
        #self.cell_type_combo.currentTextChanged.connect(self.color_cell_type)
        self.add_cell_type_btn = QPushButton("Add cell type")
        self.add_cell_type_btn.clicked.connect(self.add_cell_type)

        #Color selection
        color_options = ["blue", "green", "red", "cyan", "magenta", "yellow", "white"]
        self.color_combo = QComboBox(self)
        self.color_combo.addItems(color_options)

        # Reset button
        self.reset_button = QPushButton(self)
        self.reset_button.setText("Reset")
        self.reset_button.clicked.connect(self.color_reset)

        # Layout of widget
        vbox = QVBoxLayout(self)
        vbox.addWidget(QLabel("Select color:"))
        vbox.addWidget(self.color_combo)
        vbox.addWidget(QLabel("Color by gene:"))
        vbox.addWidget(self.gene_combo)
        vbox.addWidget(self.add_gene_btn)
        vbox.addWidget(QLabel("Color by cell type:"))
        vbox.addWidget(self.cell_type_combo)
        vbox.addWidget(self.add_cell_type_btn)
        vbox.addWidget(self.reset_button)
        vbox.addStretch()

        self.layout = vbox

    def populate_options(self):
        """draws visualization options based on the available data in segmentation"""
        import pandas as pd

        # set seg to active segmentation
        self.seg = self.dataset.active_segmentation
        
        used_genes = []
        for gene in self.seg.gene_expression.columns:
            # Only include genes with expression in at least one object
            if sum(self.seg.gene_expression[gene]) > 0:
                used_genes.append(gene)

        self.seg.gene_expression = self.seg.gene_expression[used_genes]

        self.gene_combo.clear()
        for gene in self.seg.gene_expression.columns:
            self.gene_combo.addItem(gene)

        # If cell type information is available
        if isinstance(self.seg.cell_types, pd.DataFrame):
            self.cell_type_combo.clear()
            for cell_type in self.seg.cell_types.columns:
                self.cell_type_combo.addItem(cell_type)

    def add_gene(self):
        """Add gene to viewer"""
    


        gene = self.gene_combo.currentText()
        color = self.color_combo.currentText()
        values = self.seg.gene_expression[gene].values
        values = np.log1p(values)
        values = values/values.max()
        cmap = Colormap(["black", color])
        colors = cmap[values]
        colors = dict(
            zip(self.seg.gene_expression.index, colors.rgba)
        )
        self.viewer.add_labels(
            self.seg.objects,
            name = f"{gene} - {color}",
            color = colors,
            blending = "additive")
        

    def add_cell_type(self):
        """Add cell type to viewer"""
        import numpy as np
        from vispy.color.colormap import MatplotlibColormap

        cell_type = self.cell_type_combo.currentText()
        color = self.color_combo.currentText()
        values = self.seg.cell_types[cell_type].values
        values = np.log1p(values)
        values = values/values.max()
        cmap = Colormap(["black", color])
        colors = cmap[values]
        colors = dict(
            zip(self.seg.cell_types.index, colors.rgba)
        )
        self.viewer.add_labels(
            self.seg.objects,
            name = f"{cell_type} - {color}",
            color = colors,
            blending = "additive")


    def color_genes(self, gene):
        """Sets object color by selected gene"""
        values = self.seg.gene_expression[gene].values
        values = np.log1p(values)
        values = values/values.max()
        cmap = MatplotlibColormap("inferno")
        colors = cmap[values]
        self.viewer.layers[self.seg.__repr__()].color = dict(
            zip(self.seg.gene_expression.index, colors.rgba)
        )
        # Change blending to additive to allow black objects to disapear
        self.viewer.layers[self.seg.__repr__()].blending = "additive"

    def color_cell_type(self, cell_type):
        """Sets object color by selected gene"""
        values = self.seg.cell_types[cell_type].values
        values = np.log1p(values)
        values = values/values.max()
        cmap = MatplotlibColormap("inferno")
        colors = cmap[values]
        self.viewer.layers[self.seg.__repr__()].color = dict(
            zip(self.seg.cell_types.index, colors.rgba)
        )
        # Change blending to additive to allow black objects to disapear
        self.viewer.layers[self.seg.__repr__()].blending = "additive"

    def color_reset(self):
        """Reset object color to auto and translucent."""
        self.viewer.layers[self.seg.__repr__()].color_mode = "auto"
        self.viewer.layers[self.seg.__repr__()].blending = "translucent"
