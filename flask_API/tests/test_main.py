import random

import responses

from flask_API.tests import client

if client is None:
    print("Client is null")
    exit()

USER_API = "http://fall2022-comp585.cs.mcgill.ca:8080/user/"
KNOWN_USER_IDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
UNKNOWN_USER_IDS = [
    "0",
    "11",
]

KNOWN_OCCUPATIONS = [
    "K-12 student",
    "academic/educator",
    "artist",
    "clerical/admin",
    "college/grad student",
    "customer service",
    "doctor/health care",
    "executive/managerial",
    "farmer",
    "homemaker",
    "lawyer",
    "other or not specified",
    "programmer",
    "retired",
    "sales/marketing",
    "scientist",
    "self-employed",
    "technician/engineer",
    "tradesman/craftsman",
    "unemployed",
    "writer",
]
KNOWN_GENDERS = ["M", "F"]


def before_test():
    for user_id in KNOWN_USER_IDS:
        occupation = KNOWN_OCCUPATIONS[random.randint(0, len(KNOWN_OCCUPATIONS) - 1)]
        gender = KNOWN_GENDERS[random.randint(0, len(KNOWN_GENDERS) - 1)]
        responses.add(
            responses.GET,
            USER_API + user_id,
            json={"age": 25, "occupation": occupation, "gender": gender},
            status=200,
        )

    for user_id in UNKNOWN_USER_IDS:
        responses.add(
            responses.GET,
            USER_API + user_id,
            json={"msg": "user not found"},
            status=404,
        )


# home should return Hello World
def test_hello_world(client):
    before_test()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data


# getRecommendations should return a list of recommendations
@responses.activate
def test_getRecommendations(client):
    before_test()
    user_id = KNOWN_USER_IDS[random.randint(0, len(KNOWN_USER_IDS) - 1)]
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 200


# getRecommendations should return a comma separated list of recommendations
@responses.activate
def test_getRecommendations_comma_separated(client):
    before_test()
    user_id = KNOWN_USER_IDS[random.randint(0, len(KNOWN_USER_IDS) - 1)]
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 200
    assert b"," in response.data


# getRecommendations should return 20 recommendations
@responses.activate
def test_getRecommendations_20(client):
    before_test()
    user_id = KNOWN_USER_IDS[random.randint(0, len(KNOWN_USER_IDS) - 1)]
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 200
    assert len(response.data.split(b",")) == 20


# getRecommendations should fail for an unknown user
@responses.activate
def test_getRecommendations_unknown_user(client):
    before_test()
    user_id = UNKNOWN_USER_IDS[random.randint(0, len(UNKNOWN_USER_IDS) - 1)]
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 404


# getRecommendations should not fail for user with missing information
@responses.activate
def test_getRecommendations_missing_info(client):
    user_id = KNOWN_USER_IDS[random.randint(0, len(KNOWN_USER_IDS) - 1)]
    responses.add(
        responses.GET,
        USER_API + user_id,
        json={"age": None, "occupation": "", "gender": " "},
        status=200,
    )
    response = client.get("/recommend/" + user_id)
    assert response.status_code == 200
