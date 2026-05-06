from fastapi.testclient import TestClient
from unittest.mock import patch, ANY 
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "msg": "Hello World" }

def test_upload_empty_package():
    response = client.post(
        "/upload/"
    )
    assert response.status_code == 400
    assert response.json() == { "detail": "Input and File not found" }

@patch('main.json.load')
@patch('main.worker.delay')
def test_upload_input_only(mock_worker_delay, mock_json_read):

    mock_json_read.return_value = { "sample_1": [ "test" ] }
    
    res = client.post(
        "/upload/",
        data={
            "input": "Did you know that cats can live up to 20 years?"
        }
    )

    mock_json_read.assert_called_once_with(ANY)
    mock_worker_delay.assert_called_once_with(
        "Did you know that cats can live up to 20 years?",
        None,
        "\n".join(mock_json_read.return_value["sample_1"])
    )
    assert res.status_code == 200
    assert res.json() == { "msg": "[SUCCESS]: worker started" }

@patch('main.json.load')
@patch('main.worker.delay')
def test_upload_file_only(mock_worker_delay,  mock_json_read):
    mock_json_read.return_value = { "sample_1": ["test"] }

    res = client.post(
        "/upload/",
        files={
            "file": ("text.txt", b"hello", "text/plain")
        }
    )

    mock_json_read.assert_called_once_with(ANY)
    mock_worker_delay.assert_called_once_with(
        None,
        b"hello",
        "\n".join(mock_json_read.return_value["sample_1"])
    )
    assert res.status_code == 200
    assert res.json() == {"msg": "[SUCCESS]: worker started"}

@patch('main.json.load')
@patch('main.worker.delay')
def test_upload_valid_package(mock_worker_delay, mock_json_read): 
    mock_json_read.return_value = { "sample_1": ["test"] }

    response = client.post(
        "/upload/",
        data={
            "input": "Please summarize the following"
        },
        files={
            "file": ("text.txt", b"hello", "text/plain")
        }
    )

    mock_json_read.assert_called_once_with(ANY)
    mock_worker_delay.assert_called_once_with(
        "Please summarize the following",
        b"hello",
        "\n".join(mock_json_read.return_value["sample_1"])
    )
    assert response.status_code == 200
    assert response.json() == { "msg": "[SUCCESS]: worker started" }

 
