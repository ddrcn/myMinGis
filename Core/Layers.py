from Core.Exception import LayerCreationException


class Layer:
    def __init__(self, name, layer_type):
        if layer_type not in ["raster", "vector"]:
            raise LayerCreationException("Undefined layer type")
        self.name = name
        self.type = layer_type


class RasterLayer(Layer):
    def __init__(self, name, data, bounds):
        super().__init__(name, "raster")
        self.data = data
        self.bounds = bounds


class VectorLayer(Layer):
    def __init__(self, name, data):
        super().__init__(name, "vector")
        self.data = data
