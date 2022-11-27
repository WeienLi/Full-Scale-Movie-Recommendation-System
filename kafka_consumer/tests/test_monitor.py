# import sys

# from Database.db import RedisDB
# from kafka_consumer.monitor import process_message

# # from monitor import process_message


# sys.path.append("..")


# def test_process_message():

#     db = RedisDB()
#     assert db is not None

#     log1 = "2022-10-07T13:43:26,246904,GET /rate/chicken+run+2000=5"
#     log2 = "2022-10-07T14:21:02,245839,GET /data/m/in+a++w+2010/63.mpg"
#     log3 = None
#     log4 = "asdd"
#     log5 = "2047,246904,re, 200, result: +in+, a, +v, b+a, a+c, a, in+a++w+2010, e+v+1988, q+a+c, the+v+b, w+1, s, d+o, a+v, a+a+a+1949, w, v, b+a, s, 1+s, 107 ms"
#     log6 = "2022-10-07T14:21:02,246904,GET /data/m/e+v+1988/63.mpg"
#     log7 = "2022-10-07T14:21:02,246904,GET /data/m/the+v+b/63.mpg"
#     log8 = "2022-10-07T14:21:02,246904,GET /data/m/d+o/63.mpg"
#     log9 = "2022-10-07T14:21:02,246904,GET /data/m/a+a+a+1949/63.mpg"
#     process_message(log3)
#     process_message(log4)
#     process_message(log5)
#     process_message(log1)
#     process_message(log2)
#     process_message(log6)
#     process_message(log7)
#     process_message(log8)
#     process_message(log9)

#     assert True
