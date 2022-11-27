import sys

from kafka_consumer.cloud_database import con, gtl, parse_message_local, pmfc

# from utils.constants import MessageType


sys.path.append("..")


def test_connection():
    supa = con()
    assert supa is not None


def test_parse_message_local():
    message = [
        "GET /data/m/the+tulse+luper+suitcases_+part+1+the+moab+story+2003/6x1.mpg",
        "2022-10-07T14:21:02,83916,GET /data/m/god+speed+you+black+emperor+1976/17.mpg",
        "2022-10-07T14:21:02,839 16,GET /data/m/god+speed+you+black+emperor+1976/17.mpg",
        "2047,2223,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2047,22@23,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2022-10-07T13:43:28,319 079,GET /rate/se7en+1995=4",
        "2022-10-07T13:43:29,52590,GET /rate/the+avengers+2012=5",
        "asda",
        "2022-10-07T13:43:29,52590,GET /rate/the+avengers+2012=5x",
        "2022-10-07T14:21:02,83916,GET /data/m/god+speed+you+black+emperor+1976/1x7.mpg",
    ]

    result = parse_message_local(message[0])
    assert result[0] == "BROKEN"

    result = parse_message_local(message[1])
    assert result[0] == "WATCHTIME"

    result = parse_message_local(message[2])
    assert result[0] == "BROKEN"

    result = parse_message_local(message[3])
    assert result[0] == "RECOMMEND"

    result = parse_message_local(message[4])
    assert result[0] == "BROKEN"

    result = parse_message_local(message[5])
    assert result[0] == "BROKEN"

    result = parse_message_local(message[6])
    assert result[0] == "RATING"

    result = parse_message_local(message[7])
    assert result[0] == "BROKEN"

    result = parse_message_local(message[8])
    assert result[0] == "BROKEN"

    result = parse_message_local(message[9])
    assert result[0] == "BROKEN"


def test_process_message_for_cloud():
    log1 = "2022-10-07T13:43:26,246904,GET /rate/chicken+run+2000=5"
    log2 = (
        "2022-10-07T14:21:02,245839,GET /data/m/the+man+who+knew+too+much+1956/63.mpg"
    )
    log3 = None
    log4 = "asdd"
    log5 = "2022-10-07T14:21:02,245839,GET /data/m/the+man+who+knew+too+much+1956/3.mpg"
    supabase = con()

    result = pmfc(supabase, log1, "RATING")
    assert result == 1

    result = pmfc(supabase, log2, "WATCHTIME")
    assert result == 1

    result = pmfc(supabase, log3, "WATCHTIME")
    assert result == 0

    result = pmfc(supabase, log4, "WATCHTIME")
    assert result == 0

    result = pmfc(supabase, log5, "WATCHTIME")
    assert result == 0

    result = pmfc(supabase, log2, "RATING")
    assert result == 0


def test_get_table_length():
    supabase = con()
    length = gtl(supabase, "WatchTime")
    assert length > 0

    supabase = con()
    length = gtl(supabase, "Rating")
    assert length > 0
