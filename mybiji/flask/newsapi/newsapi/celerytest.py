# from celery import Celery
#
# app=Celery('tasks',broker='redis://127.0.0.1:6379/5')
#
#
#
#
# @app.task
# def add(x,y):
#     return  x+y
#
#
#
#
#
# a=add(1,2)
# print(a)




a=257
b=257
print(a is b)
print(id(a))
print(id(b))




li = [1,0,3,7,7,5]
formatList = list({}.fromkeys(li).keys())
print (formatList)









