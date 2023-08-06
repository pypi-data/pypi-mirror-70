# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtWidgets import QVBoxLayout, QWidget

from .containers import LayersTreeMVFactory


class LayersTreeWidget(QWidget):
    """
    Widget for displaying the list of avaliable layers for constructing models.
    """

    def __init__(self, layerstree_mv_factory: "LayersTreeMVFactory", parent=None):
        super().__init__(parent)

        self.__model = layerstree_mv_factory.Model(parent=self)
        self.__view = layerstree_mv_factory.View(parent=self)
        self.__view.setModel(self.__model)

        self.__main_layout = QVBoxLayout()

        self.__setup_ui()

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__view)

        self.setLayout(self.__main_layout)

    def __reduce__(self):
        return (LayersTreeWidget, (LayersTreeMVFactory(),))


LayersTreeWidgetFactory = providers.Factory(
    LayersTreeWidget, layerstree_mv_factory=LayersTreeMVFactory
)
