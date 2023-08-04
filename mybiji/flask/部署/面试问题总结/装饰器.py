# def outer():
#     x = 1
#     def inner():
#         print("x=%s" % x)
#         print("inner func excuted")
#
#     print("outer func excuted")
#     return inner  # 返回内部函数名

# outer()


# def outer():
#     x = 1
#     y = 2
#
#     def inner():
#         print("x= %s" %x)
#         print("y= %s" %y)
#
#     print(inner.__closure__)   # (<cell at 0x000001593F22C738: int object at 0x00007FFC34313810>, <cell at 0x000001593EDCAA38: int object at 0x00007FFC34313830>)
#                                #   结果表明,在inner内部，引用了两个外部局部变量。如果引用的是非局部变量，那么这里输出的为None.
#
#     return inner
#
# outer()


from urllib.request import urlopen

def index(url):
    def get():
        return urlopen(url).read()
    return get

python = index("http://www.python.org") # 返回的是get函数的地址
print(python()) # 执行get函数《并且将返回的结果打印出来

baidu = index("http://www.baidu.com")
print(baidu())






