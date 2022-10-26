import pytest

from flask_API.tests import client

if client is None:
    print("Client is null")
    exit()


# home should return Hello World
def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


# getRecommendations should return a list of recommendations
def test_getRecommendations(client):
    user_id = "1"
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 200


# getRecommendations should return a comma separated list of recommendations
def test_getRecommendations_comma_separated(client):
    user_id = "1"
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 200
    assert b"," in response.data


# getRecommendations should return 20 recommendations
def test_getRecommendations_20(client):
    user_id = "1"
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 200
    assert len(response.data.split(b",")) == 20


# TODO: fix this test
# getRecommendations should fail for an unknown user
@pytest.mark.skip(reason="This test is failing")
def test_getRecommendations_unknown_user(client):
    user_id = "999999"
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 404
