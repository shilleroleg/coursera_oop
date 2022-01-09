"""
Реализовать Chain of Responsibility.
Необходимо реализовать поведение:
    EventGet(<type>) создаёт событие получения данных соответствующего типа
    EventSet(<value>) создаёт событие изменения поля типа type(<value>)

Необходимо реализовать классы NullHandler, IntHandler, FloatHandler, StrHandler так, чтобы можно было создать цепочку:
chain = IntHandler(FloatHandler(StrHandler(NullHandler)))

Описание работы цепочки:

    chain.handle(obj, EventGet(int)) — вернуть значение obj.integer_field
    chain.handle(obj, EventGet(str)) — вернуть значение obj.string_field
    chain.handle(obj, EventGet(float)) — вернуть значение obj.float_field
    chain.handle(obj, EventSet(1)) — установить значение obj.integer_field =1
    chain.handle(obj, EventSet(1.1)) — установить значение obj.float_field = 1.1
    chain.handle(obj, EventSet("str")) — установить значение obj.string_field = "str"
"""


class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, kind):
        self.kind = kind
        self.value = None


class EventSet:
    def __init__(self, value):
        self.kind = type(value)
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if issubclass(event.kind, int):
            if event.value is not None:
                obj.integer_field = event.value
            return obj.integer_field
        else:
            # Передаю обработку дальше
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if issubclass(event.kind, float):
            if event.value is not None:
                obj.float_field = event.value
            return obj.float_field
        else:
            # Передаю обработку дальше
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if issubclass(event.kind, str):
            if event.value is not None:
                obj.string_field = event.value
            return obj.string_field
        else:
            # Передаю обработку дальше
            return super().handle(obj, event)


if __name__ == "__main__":
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    print(chain.handle(obj, EventGet(int)))        # 42
    print(chain.handle(obj, EventGet(float)))      # 3.14
    print(chain.handle(obj, EventGet(str)))        # 'some text'
    chain.handle(obj, EventSet(100))
    print(chain.handle(obj, EventGet(int)))        # 100
    chain.handle(obj, EventSet(0.5))
    print(chain.handle(obj, EventGet(float)))      # 0.5
    chain.handle(obj, EventSet('new text'))
    print(chain.handle(obj, EventGet(str)))        # 'new text'
