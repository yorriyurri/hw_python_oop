from dataclasses import dataclass
from typing import ClassVar, Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_H: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Is it necessary to write something here?')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEF_CALORIES_1: ClassVar[float] = 18
    COEF_CALORIES_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        return ((self.COEF_CALORIES_1 * self.get_mean_speed()
                - self.COEF_CALORIES_2) * self.weight
                / self.M_IN_KM * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_CALORIES_1: ClassVar[float] = 0.035
    COEF_CALORIES_2: ClassVar[float] = 0.029

    height: float

    def get_spent_calories(self) -> float:
        return ((self.COEF_CALORIES_1
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEF_CALORIES_2)
                * self.weight * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    COEF_CALORIES_1: ClassVar[float] = 1.1
    COEF_CALORIES_2: ClassVar[float] = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_CALORIES_1)
                * self.COEF_CALORIES_2 * self.weight)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_codes: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    if workout_type in workout_codes:
        workout = workout_codes[workout_type](*data)
        return workout
    return None


def main(training: Training) -> None:
    """Главная функция."""
    if training is None:
        print('Код тренировки не найден.')
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
