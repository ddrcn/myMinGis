from Core.Templates import DEFAULT_HTML, MAP_CREATION_SCRIPT, OSM_TILE_CREATION_SCRIPT, ADD_TILE_TO_MAP_SCRIPT, \
    GEOJSON_LAYER_CREATION_SCRIPT, GEOJSON_LAYER_ADD_DATA_SCRIPT, REMOVE_LAYER_SCRIPT, RASTER_LAYER_CREATION_SCRIPT, \
    SHOW_LAYER_SCRIPT, HIDE_LAYER_SCRIPT, BRING_TO_BACK_SCRIPT, BRING_TO_FRONT_SCRIPT
from Core.Exception import MapCreationException, LayerAdditionException
from Core.Layers import Layer, VectorLayer
import geojson


class View:
    TILES_STRING_TO_SCRIPT = {"OpenStreetMaps": OSM_TILE_CREATION_SCRIPT}

    def __init__(self, window, map_tiles="OpenStreetMaps"):
        if map_tiles not in View.TILES_STRING_TO_SCRIPT.keys():
            raise MapCreationException("Undefined map tiles")
        self.layers = []
        self.map_tiles = map_tiles
        self.window = window
        self.window.setHtml(DEFAULT_HTML)
        self.window.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, status):
        if status:
            self.window.page().runJavaScript(MAP_CREATION_SCRIPT +
                                             View.TILES_STRING_TO_SCRIPT[self.map_tiles] + ADD_TILE_TO_MAP_SCRIPT)

    def add_vector_layer(self, layer_name, file_path):
        if self.has_layer(layer_name):
            raise LayerAdditionException("Layer already exists")
        try:
            geo_file = open(file_path, 'r')
            geo_data = geojson.load(geo_file)
            geo_file.close()
        except Exception as ex:
            pass
        else:
            self.layers.append(VectorLayer(layer_name, str(geo_data)))
            self.window.page().runJavaScript(GEOJSON_LAYER_CREATION_SCRIPT % (layer_name,layer_name))
            self.window.page().runJavaScript(GEOJSON_LAYER_ADD_DATA_SCRIPT % (layer_name, str(geo_data)))

    def has_layer(self, layer_name):
        checker = False
        for layer in self.layers:
            if layer.name == layer_name:
                checker = True
        return checker
