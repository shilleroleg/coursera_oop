"""
Продолжая работу над игрой, вы добрались до системы достижений. Иногда по сценарию игры требуется наградить игрока за то,
 что он достигает определенного результата в игре. Это может быть, например: прохождение всех заданий в игре,
 достижение определенного уровня, совершение какого-то сложного действия и т.д.

У каждой игры есть движок и интерфейс пользователя. Эти два компонента работают параллельно и взаимодействуют друг
с другом. Достижения генерируются движком игры, а отображаются пользовательским интерфейсом. Кроме того,
на современных игровых площадках, таких как Steam, Google Play, также отображаются достижения, полученные игроком.
Реализуется это с помощью паттерна Наблюдатель.

В реализации нашей игры есть движок Engine, который может создавать уведомления о достижениях. Пример достижения,
которое генерирует движок:
{"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}

Вам необходимо написать обертку над движком, которая будет иметь возможность подписывать наблюдателей и рассылать им
уведомления. Вы так же должны написать реализацию классов иерархии наблюдателей.
"""
from abc import ABC, abstractmethod


class Engine:
    pass


class ObservableEngine(Engine):
    def __init__(self):
        self.__subscriber = set()

    def subscribe(self, subscriber):
        self.__subscriber.add(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscriber.remove(subscriber)

    def notify(self, message):
        for subscriber in self.__subscriber:
            subscriber.update(message)


class AbstractObserver(ABC):
    # def __init__(self, name):
    #     self.name = name

    @abstractmethod
    def update(self, achievement):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, achievement):
        self.achievements.add(achievement.get('title'))


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = []

    def update(self, achievement):
        # Проверяем, что достижение уникальное
        if achievement not in self.achievements:
            self.achievements.append(achievement)


if __name__ == "__main__":
    achieve = {"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}
    achieve2 = {"title": "Неудачник", "text": "Дается при провале всех заданий в игре"}
    achieve3 = {"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"}

    short1 = ShortNotificationPrinter()
    full1 = FullNotificationPrinter()
    full2 = FullNotificationPrinter()

    manager = ObservableEngine()

    manager.subscribe(short1)
    manager.subscribe(full1)
    manager.subscribe(full2)

    manager.notify(achieve)

    print(short1.achievements)
    print(full1.achievements)
    print(full2.achievements)

    # Проверяем отписку
    print('Unsubscribe')
    manager.unsubscribe(full2)
    manager.notify(achieve2)

    print(short1.achievements)
    print(full1.achievements)
    print(full2.achievements)

    # Достижения хранятся только уникальные
    manager.notify(achieve3)

    print(short1.achievements)
    print(full1.achievements)


