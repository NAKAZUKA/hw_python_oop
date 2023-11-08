from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        data = asdict(self)
        message = (
            'Тип тренировки: {training_type}; '
            'Длительность: {duration:.3f} ч.; '
            'Дистанция: {distance:.3f} км; '
            'Ср. скорость: {speed:.3f} км/ч; '
            'Потрачено ккал: {calories:.3f}.'
        )
        return message.format(**data)


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    MIN_IN_H = 60
    M_IN_KM = 1000

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
        raise NotImplementedError(
            'Метод get_spent_calories класса Training '
            'должен быть переопределен в подклассах'
        )

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * (self.weight / self.M_IN_KM) * (self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_COEFFICIENT_SPEED = 0.035
    CALORIES_COEFFICIENT_HEIGHT = 0.029
    M_IN_KM = 1000
    CM_TO_M = 100
    MIN_IN_H = 60

    height: float

    KM_H_TO_M_S = round(M_IN_KM / MIN_IN_H**2, 3)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.CALORIES_COEFFICIENT_SPEED * self.weight
                + ((self.get_mean_speed() * self.KM_H_TO_M_S)**2
                    / self.height * self.CM_TO_M)
                * self.CALORIES_COEFFICIENT_HEIGHT * self.weight)
        ) * self.duration * self.MIN_IN_H


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    MEAN_SPEED_KONST = 1.1
    CALORIES_BURN_RATE = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.MEAN_SPEED_KONST)
        ) * self.CALORIES_BURN_RATE * self.weight * self.duration


TYPES_TRANING = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in TYPES_TRANING:
        return TYPES_TRANING[workout_type](*data)
    raise ValueError("Неверный тип тренировки")


def main(training: Training) -> None:
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
