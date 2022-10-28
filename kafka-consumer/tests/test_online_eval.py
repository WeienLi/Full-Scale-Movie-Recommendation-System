import sys

from online_eval import calculate_MRR, get_recommendation_request_feedback

sys.path.append("..")


def test_online_eval():
    consumer = [
        "2047,2223,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2047,1234,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2047,2211,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
        "2022-10-07T14:21:02,2223,GET /data/m/+in+/17.mpg",
        "2022-10-07T14:21:02,2223,GET /data/m/a/17.mpg",
        "2022-10-07T14:21:02,2223,GET /data/m/+v/17.mpg",
        "2022-10-07T14:21:02,1234,GET /data/m/+v/17.mpg",
        "2022-10-07T14:21:02,1234,GET /data/m/e+v+1988/17.mpg",
        "2022-10-07T14:21:02,1234,GET /data/m/w+1/17.mpg",
        "2022-10-07T14:21:02,2211,GET /data/m/+v/17.mpg",
        "2022-10-07T14:21:02,2211,GET /data/m/e+v+1988/17.mpg",
        "2022-10-07T14:21:02,2211,GET /data/m/w+1/17.mpg",
        "2022-10-07T14:21:02,2211,GET /data/m/in+a++w+2010/17.mpg",
    ]

    rec_list = get_recommendation_request_feedback(3, 10, consumer)
    for rec in rec_list:
        print(rec.user)
        print(len(rec.watch_movie))

    accpet_rates = calculate_MRR(rec_list)
    assert accpet_rates[0] == 0.611111111111111
    assert accpet_rates[1] == 0.19206349206349205
    assert accpet_rates[2] == 0.1857142857142857
