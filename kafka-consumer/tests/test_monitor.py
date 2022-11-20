# import sys

# import monitor

# from Database.db import RedisDB

# sys.path.append("..")


# def test_process_message():
#     try:
#         RedisDB()
#         log1 = "2022-10-07T13:43:26,246904,GET /rate/chicken+run+2000=5"
#         log2 = "2022-10-07T14:21:02,245839,GET /data/m/in+a++w+2010/63.mpg"
#         log3 = None
#         log4 = "asdd"
#         log5 = (
#             "2047,246904,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms",
#         )
#         monitor.process_message(log3)
#         monitor.process_message(log4)
#         monitor.process_message(log5)
#         monitor.process_message(log1)
#         monitor.process_message(log2)

#         assert True
#     except Exception:
#         assert False
