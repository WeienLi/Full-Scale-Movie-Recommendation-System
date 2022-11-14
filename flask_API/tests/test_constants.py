from flask_API.constants import SavedRec

def test_SavedRec():
    str_data = '{"userID": "1", "recommendations": "1,2,3", "timestamp": "2021-10-01 00:00 UTC", "sha": "1234567890", "app_mode": "main"}'
    saved_rec = SavedRec(str_data)
    assert saved_rec.userID == "1"
    assert saved_rec.recommendations == "1,2,3"
    assert saved_rec.timestamp == "2021-10-01 00:00 UTC"
    assert saved_rec.sha == "1234567890"
    assert saved_rec.app_mode == "main"

def test_SavedRec_init():
    saved_rec = SavedRec()
    saved_rec.init("1", "1,2,3", "2021-10-01 00:00 UTC", "1234567890", "main")
    assert saved_rec.userID == "1"
    assert saved_rec.recommendations == "1,2,3"
    assert saved_rec.timestamp == "2021-10-01 00:00 UTC"
    assert saved_rec.sha == "1234567890"
    assert saved_rec.app_mode == "main"

def test_SavedRec_str():
    saved_rec = SavedRec()
    saved_rec.init("1", "1,2,3", "2021-10-01 00:00 UTC", "1234567890", "main")
    str_data = str(saved_rec)
    assert str_data == '{"userID": "1", "recommendations": "1,2,3", "timestamp": "2021-10-01 00:00 UTC", "sha": "1234567890", "app_mode": "main"}'