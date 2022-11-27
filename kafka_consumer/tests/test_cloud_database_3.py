from kafka_consumer.cloud_database import con, delete_all_data


def test_delete():
    supa = con()
    delete_all_data(supa, "TestOperation")
    assert True
    try:
        delete_all_data(supa, "TestOperations")  # this should fail
    except Exception:
        assert False
