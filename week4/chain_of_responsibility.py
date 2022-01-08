class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet(SomeObject):
    pass


class EventSet(SomeObject):
    pass


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, char, event):
        if self.__successor is not None:
            return self.__successor.handle(char, event)


class IntHandler(NullHandler):
    pass


class FloatHandler(NullHandler):
    pass


class StrHandler(NullHandler):
    pass


if __name__ == "__main__":
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    chain.handle(obj, EventGet(int))        # 42
    chain.handle(obj, EventGet(float))      # 3.14
    chain.handle(obj, EventGet(str))        # 'some text'
    chain.handle(obj, EventSet(100))
    chain.handle(obj, EventGet(int))        # 100
    chain.handle(obj, EventSet(0.5))
    chain.handle(obj, EventGet(float))      # 0.5
    chain.handle(obj, EventSet('new text'))
    chain.handle(obj, EventGet(str))        # 'new text'
