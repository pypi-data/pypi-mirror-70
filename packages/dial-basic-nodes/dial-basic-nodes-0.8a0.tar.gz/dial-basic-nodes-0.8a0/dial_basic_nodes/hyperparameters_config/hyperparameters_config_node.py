# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.node_editor import Node

from .hyperparameters_config_widget_gui import HyperparametersConfigWidgetGuiFactory

from .hyperparameters_config_widget import HyperparametersConfigWidgetFactory

if TYPE_CHECKING:
    from .hyperparameters_config_widget_gui import HyperparametersConfigWidgetGui


class HyperparametersConfigNode(Node):
    def __init__(
        self, hyperparameters_config_widget: "HyperparametersConfigWidgetGui",
    ):
        super().__init__(
            title="Hyperparameters Config", inner_widget=hyperparameters_config_widget,
        )

        self.add_output_port("Hyperparameters", port_type=dict)
        self.outputs["Hyperparameters"].set_generator_function(self.get_hyperparameters)

    def get_hyperparameters(self):
        return self.inner_widget.get_hyperparameters()

    def __reduce__(self):
        return (HyperparametersConfigNode, (self.inner_widget,), super().__getstate__())


HyperparametersConfigNodeGuiFactory = providers.Factory(
    HyperparametersConfigNode,
    hyperparameters_config_widget=HyperparametersConfigWidgetGuiFactory,
)

HyperparametersConfigNodeFactory = providers.Factory(
    HyperparametersConfigNode,
    hyperparameters_config_widget=HyperparametersConfigWidgetFactory,
)
