from Database.db import RedisDB


def test_set_should_store_value():
    """Test that the value is stored in the database"""
    db = RedisDB()
    db.set("test", "value")
    assert db.get("test") == "value"


def test_get_should_return_value():
    """Test that the value is returned from the database"""
    db = RedisDB()
    db.set("test", "value")
    assert db.get("test") == "value"


def test_incr_should_increment_value():
    """Test that the value is incremented in the database"""
    db = RedisDB()
    db.set("test", "1")
    db.incr("test")
    assert db.get("test") == "2"


def test_get_should_return_none():
    """Test that the value is returned from the database"""
    db = RedisDB()
    assert db.get("test") is None


def test_incr_should_return_one():
    """Test that the value is incremented in the database even when key doesn't initially exist"""
    db = RedisDB()
    assert db.incr("test") == "1"


def test_incr_should_be_type_string():
    """Test that the value is incremented in the database and is a string"""
    db = RedisDB()
    db.set("test", 1)
    assert type(db.incr("test")) == str
