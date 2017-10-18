import os

import falcon

from .images import Resource, ImageStore

def create_app(image_store):
    image_resource = Resource(image_store)
    api = falcon.API()
    api.add_route('/images', image_resource)
    return api


def get_app():
    storage_path = os.environ.get('TUTORIAL_STORAGE_PATH', '.')
    image_store = ImageStore(storage_path)
    return create_app(image_store)