import io

import falcon
from falcon import testing
import msgpack
import pytest

from mock import call, MagicMock, mock_open

import tutorial.app
import tutorial.images


@pytest.fixture
def mock_store():
    return MagicMock()


@pytest.fixture
def client(mock_store):
    api = tutorial.app.create_app(mock_store)
    return testing.TestClient(api)


def test_list_images(client):
    doc = {
        'images': [
            {
                'href': '/images/1eaf6ef1-7f2d-4ecc-a8d5-6e8adba7cc0e.png'
            }
        ]
    }

    response = client.simulate_get('/images')
    result_doc = msgpack.unpackb(response.content, encoding='utf-8')

    assert result_doc == doc
    assert response.status == falcon.HTTP_OK

# With clever composition of fixtures, we can observe what happens with
# the mock injected into the image resource.
def test_post_image(client, mock_store):
    file_name = 'fake-image-name.png'

    # We need to know what ImageStore method will be used
    mock_store.save.return_value = file_name
    image_content_type = 'image/png'

    response = client.simulate_post(
        '/images',
        body=b'fake-bytes',
        headers={'content-type': image_content_type}
    )

    assert response.status == falcon.HTTP_CREATED
    assert response.headers['location'] == '/images/{}'.format(file_name)
    saver_call = mock_store.save.call_args

    # saver_call is a unittest.mock.call tuple. It's first element is a
    # tuple of positional arguments supplied when calling the mock.
    assert isinstance(saver_call[0][0], falcon.request_helpers.BoundedStream)
    assert saver_call[0][1] == image_content_type


def test_post_unknown_image_type(client, mock_store):
    file_name = 'unknown-image-type.zzz'

    mock_store.save.return_value = file_name
    image_content_type = 'image/zzz'

    response = client.simulate_post(
        '/images',
        body=b'fake-bytes',
        headers={'content-type': image_content_type}
    )

    assert response.status == falcon.HTTP_BAD_REQUEST


def test_saving_image(monkeypatch):
    mock_file_open = mock_open()

    fake_uuid = '1234'
    def mock_uuidgen():
        return fake_uuid

    fake_image_bytes = b'fake-bytes'
    fake_request_stream = io.BytesIO(fake_image_bytes)
    storage_path = 'fake-path'
    store = tutorial.images.ImageStore(
        storage_path,
        uuidgen=mock_uuidgen,
        fopen=mock_file_open)

    assert store.save(fake_request_stream, 'image/png') == fake_uuid + '.png'
    assert call().write(fake_image_bytes) in mock_file_open.mock_calls
