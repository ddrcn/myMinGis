from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction
from Core.Elements import Element, LayersWindow, AddLayersWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Core.View import View


class UI:
    MAIN_WINDOW_OBJECTS = [(QMenuBar, "menuBar")]

    def __init__(self):
        self.main_window = Element("UI/GISmin.ui", UI.MAIN_WINDOW_OBJECTS, QMainWindow())
        self.main_window.element.setCentralWidget(QWebEngineView())
        self.view = View(self.main_window.element.centralWidget())
        self.main_window.element.show()

        self.layers_window = LayersWindow("UI/LayersWindow.ui", self.main_window, self)

        self.main_window.element.setCentralWidget(QWebEngineView())
        self.view = View(self.main_window.element.centralWidget())

        self.initialize_menu_bar()

        self.add_layer_window = AddLayersWindow("UI/AddLayerWindow.ui", self.main_window, self)

        self.main_window.element.show()
        self.initialize()

    def initialize(self):
        self.layers_window.initialize(self.main_window.element.findChild(QAction, "actionLayers_Window"))
        self.add_layer_window.initialize()

    def initialize_menu_bar(self):
        self.main_window.element.findChild(QAction, "actionLayers_Window").setChecked(False)
        self.main_window.element.findChild(QAction, "actionLayers_Window").toggled.connect(
            lambda checked: self.show_layers_window() if checked else self.hide_layers_window()
        )
        self.main_window.element.findChild(QAction,"actionVector_Layer").triggered.connect(self.show_add_vector)

    def show_layers_window(self):
        self.layers_window.show()

    def hide_layers_window(self):
        self.layers_window.hide()

    def show_add_vector(self):
        self.add_layer_window.show(1)

    def update_layers_list(self):
        self.layers_window.update_layers_list()