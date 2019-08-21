import panda3d.core as p3d

from .converter import load_model, GltfSettings
from .loader import GltfLoader


def patch_loader(loader, gltf_settings=None):
    '''Monkey patch the supplied Loader to add glTF support'''
    if gltf_settings is None:
        gltf_settings = GltfSettings()
    GltfLoader.global_settings = gltf_settings

    registry = p3d.LoaderFileTypeRegistry.get_global_ptr()
    if not hasattr(registry, 'register_type'):
        import types
        _load_model = loader.load_model

        def new_load_model(self, model_path, **kwargs):
            fname = p3d.Filename(model_path)
            if fname.get_extension() in 'gltf', 'glb':
                return load_model(self, model_path, gltf_settings=gltf_settings, **kwargs)
            else:
                return _load_model(model_path, **kwargs)
        loader.load_model = loader.loadModel = types.MethodType(new_load_model, loader)


__all__ = [
    'load_model',
]
