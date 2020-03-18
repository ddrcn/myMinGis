from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QDialog, QListWidget, QLineEdit, QTabWidget, QFileDialog


class Element:
    def __init__(self, ui_path, elements, element_type):
        self.element = element_type
        uic.loadUi(ui_path, self.element)
        self.elements = dict()
        for element in elements:
            self.elements[element[1]] = self.element. \
                findChild(element[0], element[1])


class LayersWindow(Element):
    OBJECTS = [(QPushButton, "addLayerButton"), (QPushButton, "removeLayerButton"), (QListWidget, "layersList")]

    def __init__(self, ui_path, parent, ui):
        self.parent = parent
        self.ui = ui
        self.action_button = None
        super().__init__(ui_path, LayersWindow.OBJECTS, QDialog(self.parent.element))

    def initialize(self, action_button):
        self.action_button = action_button
        self.element.rejected.connect(self.hide)

    def show(self):
        self.update_layers_list()
        self.element.show()

    def hide(self):
        self.action_button.setChecked(False)
        self.element.hide()

    def update_layers_list(self):
        self.elements["layersList"].clear()
        for layer in self.ui.view.layers:
            self.elements["layersList"].addItem(layer.name)


class AddLayersWindow(Element):
    OBJECTS = [(QLineEdit, "vectorLayerName"), (QLineEdit, "vectorFilePathName"),
               (QPushButton, "openVectorFileButton"), (QPushButton, "addVectorLayerButton"),
               (QTabWidget, "layerTypeTabMenu")]

    def __init__(self, ui_path, parent, ui):
        self.parent = parent
        self.ui = ui
        super().__init__(ui_path, AddLayersWindow.OBJECTS, QDialog(self.parent.element))

    def initialize(self):
        self.elements["openVectorFileButton"].clicked.connect(self.open_vector_file)
        self.elements["addVectorLayerButton"].clicked.connect(self.add_vector_layer)

    def show(self,tab=0):
        self.elements["layerTypeTabMenu"].setCurrentIndex(tab)
        self.elements["vectorLayerName"].setText("")
        self.elements["vectorFilePathName"].setText("")
        self.element.show()

    def hide(self):
        self.element.hide()

    def open_vector_file(self):
        options = QFileDialog.Options()
        file_name, _= QFileDialog.getOpenFileName(self.parent.element,"Open File","","GeoJSON (*.geojson)",options=options)
        if file_name:
            self.elements["vectorFilePathName"].setText(file_name)


    def add_vector_layer(self):
        try:
            self.ui.view.add_vector_layer(self.elements["vectorLayerName"].text(),self.elements["vectorFilePathName"].text())
        except Exception:
            pass
        else:
            self.hide()
            self.ui.update_layers_list()