import falcon
from falcon import testing
import msgpack
import pytest
from mock import mock_open, call

from tutorial.app import api


@pytest.fixture
def client():
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

def test_posted_image_gets_saved(client, monkeypatch):
    mock_file_open = mock_open()
    monkeypatch.setattr('io.open', mock_file_open)

    fake_uuid = '1234'
    monkeypatch.setattr('uuid.uuid4', lambda: fake_uuid)

    # when the service recieves an image through POST
    fake_image_bytes = b'fake-bytes'
    response = client.simulate_post(
        '/images',
        body=fake_image_bytes,
        headers={'content-type': 'image/png'})

    # ...it must return a 201 code, save the file, and return the image's resource location
    assert response.status == falcon.HTTP_CREATED
    assert call().write(fake_image_bytes) in mock_file_open.mock_calls
    assert response.headers['location'] == '/images/{}.png'.format(fake_uuid)
