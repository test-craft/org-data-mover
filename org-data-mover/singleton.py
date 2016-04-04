class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


# class MyClass:
#     __metaclass__ = Singleton
#
# if __name__ == '__main__':
#     s1 = MyClass()
#     s2 = MyClass()
#     if id(s1) == id(s2):
#         print "Same"
#     else:
#         print "Different"
