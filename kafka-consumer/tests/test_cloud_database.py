import sys

import cloud_database
from utils.constants import MessageType

sys.path.append("..")


def test_connection():
    try:
        cloud_database.connection()
        assert True
    except Exception:
        assert False


def test_getKafkaLogs():
    supabase = cloud_database.connection()
    consumer = [
        "GET /data/m/the+tulse+luper+suitcases_+part+1+the+moab+story+2003/6x1.mpg",
        "2047,2223,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2047,22223,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2047,2223,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2022-10-25T21:33:41, 11833, GET /data/m/the+tulse+luper+suitcases_+part+1+the+moab+story+2003/6x1.mpg",
        "2022-10-07T14:21:02,83916,GET /data/m/god+speed+you+black+emperor+1976/17.mpg",
        "2022-10-07T14:21:02,511229,GET /data/m/la+traviata+1982/97.mpg",
        "2022-10-07T14:21:02,427946,GET /data/m/house+of+games+1987/29.mpg",
        "2022-10-07T14:21:02,259756,GET /data/m/the+benchwarmers+2006/71.mpg",
        "2022-10-07T14:21:02,201097,GET /data/m/family+weekend+2013/99.mpg",
        "2022-10-07T14:21:02,208868,GET /data/m/black+cat_+white+cat+1998/25.mpg",
        "2022-10-07T14:21:02,410596,GET /data/m/bigger+than+the+sky+2005/48.mpg",
        "2022-10-07T14:21:02,325322,GET /data/m/talk+of+angels+1998/24.mpg",
        "2022-10-07T14:21:02,134392,GET /data/m/close+encounters+of+the+third+kind+1977/45.mpg",
        "2022-10-07T14:21:02,245839,GET /data/m/the+man+who+knew+too+much+1956/63.mpg",
        "2022-10-07T13:43:26,246904,GET /rate/chicken+run+2000=5",
        "2022-10-07T14:21:06,224612,GET /rate/cheech++chong+get+out+of+my+room+1985=4",
        "2022-10-07T14:21:06,1505,GET /rate/the+great+lie+1941=5",
        "2022-10-07T13:43:28,95269,GET /rate/crocodile+dundee+1986=4",
        "2022-10-07T13:43:28,319079,GET /rate/se7en+1995=4",
        "2022-10-07T13:43:29,52590,GET /rate/the+avengers+2012=5",
        "2022-10-07T14:21:07,360347,GET /rate/drifting+clouds+1996=3",
        "2022-10-07T13:43:29,93955,GET /rate/kuroneko+1968=3",
        "2022-10-07T14:21:08,143924,GET /rate/the+shawshank+redemption+1994=5",
        "2022-10-07T13:43:30,488058,GET /rate/last+life+in+the+universe+2003=4",
    ]
    try:
        cloud_database.getKafkaLogs(supabase, MessageType.WATCHTIME, 1, consumer)
        cloud_database.getKafkaLogs(supabase, MessageType.RATING, 1, consumer)
        assert True
    except Exception:
        assert False


def test_process_message_for_cloud():
    log1 = "2022-10-07T13:43:26,246904,GET /rate/chicken+run+2000=5"
    log2 = (
        "2022-10-07T14:21:02,245839,GET /data/m/the+man+who+knew+too+much+1956/63.mpg"
    )
    log3 = None
    log4 = "asdd"
    supabase = cloud_database.connection()
    try:
        result = cloud_database.process_message_for_cloud(
            supabase, log1, MessageType.RATING
        )
        assert result == 1
    except Exception:
        assert False

    try:
        result = cloud_database.process_message_for_cloud(
            supabase, log2, MessageType.WATCHTIME
        )
        assert result == 1
    except Exception:
        assert False
    try:
        result = cloud_database.process_message_for_cloud(
            supabase, log3, MessageType.WATCHTIME
        )
        assert result == 0
    except Exception:
        assert False

    try:
        result = cloud_database.process_message_for_cloud(
            supabase, log4, MessageType.WATCHTIME
        )
        assert result == 0
    except Exception:
        assert False


def get_table_length():
    supabase = cloud_database.connection()
    length = get_table_length(supabase, "WatchTime")
    assert length > 0

    supabase = cloud_database.connection()
    length = get_table_length(supabase, "Rating")
    assert length > 0
