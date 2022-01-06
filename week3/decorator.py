from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    def get_positive_effects(self):
        return self.positive_effects

    def get_negative_effects(self):
        return self.negative_effects

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect, ABC):
    """Определяют интерфейс классов наследников, для подгруппы классов положительных эффектов"""
    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect, ABC):
    """Определяют интерфейс классов наследников, для подгруппы классов отрицательных эффектов"""
    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Berserk(AbstractPositive):
    """
    Берсерк
    Увеличивает характеристики: Сила, Выносливость, Ловкость, Удача на 7;
    уменьшает характеристики: Восприятие, Харизма, Интеллект на 3;
    количество единиц здоровья увеличивается на 50.
    """

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Berserk"]

    def get_stats(self):
        temp_stats = self.base.get_stats()
        temp_stats['Strength'] += 7
        temp_stats['Endurance'] += 7
        temp_stats['Agility'] += 7
        temp_stats['Luck'] += 7

        temp_stats['Perception'] -= 3
        temp_stats['Charisma'] -= 3
        temp_stats['Intelligence'] -= 3

        temp_stats['HP'] += 50

        return temp_stats


class Blessing(AbstractPositive):
    """
    Благословение
    увеличивает все основные характеристики на 2.
    """
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ["Blessing"]

    def get_stats(self):
        temp_stats = self.base.get_stats()
        temp_stats['Strength'] += 2
        temp_stats['Perception'] += 2
        temp_stats['Endurance'] += 2
        temp_stats['Charisma'] += 2
        temp_stats['Intelligence'] += 2
        temp_stats['Agility'] += 2
        temp_stats['Luck'] += 2

        return temp_stats


class Weakness(AbstractNegative):
    """
    Слабость
    уменьшает характеристики: Сила, Выносливость, Ловкость на 4.
    """
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Weakness"]

    def get_stats(self):
        temp_stats = self.base.get_stats()
        temp_stats['Strength'] -= 4
        temp_stats['Endurance'] -= 4
        temp_stats['Agility'] -= 4

        return temp_stats


class EvilEye(AbstractNegative):
    """
    Сглаз
    уменьшает  характеристику Удача на 10.
    """
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["EvilEye"]

    def get_stats(self):
        temp_stats = self.base.get_stats()
        temp_stats['Luck'] -= 10

        return temp_stats


class Curse(AbstractNegative):
    """
    Проклятье
    уменьшает все основные характеристики на 2.
    """
    def get_negative_effects(self):
        return self.base.get_negative_effects() + ["Curse"]

    def get_stats(self):
        temp_stats = self.base.get_stats()
        temp_stats['Strength'] -= 2
        temp_stats['Perception'] -= 2
        temp_stats['Endurance'] -= 2
        temp_stats['Charisma'] -= 2
        temp_stats['Intelligence'] -= 2
        temp_stats['Agility'] -= 2
        temp_stats['Luck'] -= 2

        return temp_stats


if __name__ == '__main__':
    # создадим героя
    hero = Hero()
    # проверим правильность характеристик по-умолчанию
    assert hero.get_stats() == {'HP': 128,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 15,
                                'Perception': 4,
                                'Endurance': 8,
                                'Charisma': 2,
                                'Intelligence': 3,
                                'Agility': 8,
                                'Luck': 1}
    # проверим список отрицательных эффектов
    assert hero.get_negative_effects() == []
    # проверим список положительных эффектов
    assert hero.get_positive_effects() == []
    # наложим эффект Berserk
    brs1 = Berserk(hero)
    # проверим правильность изменения характеристик
    assert brs1.get_stats() == {'HP': 178,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 22,
                                'Perception': 1,
                                'Endurance': 15,
                                'Charisma': -1,
                                'Intelligence': 0,
                                'Agility': 15,
                                'Luck': 8}
    # проверим неизменность списка отрицательных эффектов
    assert brs1.get_negative_effects() == []
    # проверим, что в список положительных эффектов был добавлен Berserk
    assert brs1.get_positive_effects() == ['Berserk']
    # повторное наложение эффекта Berserk
    brs2 = Berserk(brs1)
    # наложение эффекта Curse
    cur1 = Curse(brs2)
    # проверим правильность изменения характеристик
    assert cur1.get_stats() == {'HP': 228,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 27,
                                'Perception': -4,
                                'Endurance': 20,
                                'Charisma': -6,
                                'Intelligence': -5,
                                'Agility': 20,
                                'Luck': 13}
    # проверим правильность добавления эффектов в список положительных эффектов
    assert cur1.get_positive_effects() == ['Berserk', 'Berserk']
    # проверим правильность добавления эффектов в список отрицательных эффектов
    assert cur1.get_negative_effects() == ['Curse']
    # снятие эффекта Berserk
    cur1.base = brs1
    # проверим правильность изменения характеристик
    assert cur1.get_stats() == {'HP': 178,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 20,
                                'Perception': -1,
                                'Endurance': 13,
                                'Charisma': -3,
                                'Intelligence': -2,
                                'Agility': 13,
                                'Luck': 6}
    # проверим правильность удаления эффектов из списка положительных эффектов
    assert cur1.get_positive_effects() == ['Berserk']
    # проверим правильность эффектов в списке отрицательных эффектов
    assert cur1.get_negative_effects() == ['Curse']
    # проверим незменность характеристик у объекта hero
    assert hero.get_stats() == {'HP': 128,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 15,
                                'Perception': 4,
                                'Endurance': 8,
                                'Charisma': 2,
                                'Intelligence': 3,
                                'Agility': 8,
                                'Luck': 1}
    print('All tests - OK!')