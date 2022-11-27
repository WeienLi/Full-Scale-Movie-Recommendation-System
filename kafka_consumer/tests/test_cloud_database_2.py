from kafka_consumer.cloud_database import con, get_all_data, insert_data


def test_insert_delete():
    supa = con()
    data = {"userId": "alex", "movieId": "cat+and+we", "value": 2}
    insert_data(supa, "TestOperation", data)
    assert True

    result = insert_data(supa, "TestOperations", data)  # this should fail
    assert result == 0

    data = {}
    data = get_all_data(supa, "Rating", data)
    assert data is not None

    data = {}
    data = get_all_data(supa, "Rating_Wrong", data)
    assert data is None


# pytest --cov-fail-under=${{ env.MIN_PERCENT_COVERAGE }} --junitxml=pytest.xml
# --cov-report=term-missing:skip-covered --cov=. ./ > pytest-coverage.txt || failed=1
