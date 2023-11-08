from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE_TEMPLATE = (
        'Тип тренировки: {}; Длительность: {:.3f} ч.; Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; Потрачено ккал: {:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

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
            "Метод get_spent_calories должен быть переопределен в подклассах"
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

    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * (self.weight / self.M_IN_KM) * (self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_COEFFICIENT_1 = 0.035
    CALORIES_COEFFICIENT_2 = 0.029
    M_IN_KM = 1000
    CM_TO_M = 100
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float
    height: float

    KM_H_TO_M_S = round(M_IN_KM / MIN_IN_H**2, 3)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.CALORIES_COEFFICIENT_1 * self.weight
                + ((super().get_mean_speed() * self.KM_H_TO_M_S)**2
                    / self.height * self.CM_TO_M)
                * self.CALORIES_COEFFICIENT_2 * self.weight)
        ) * self.duration * self.MIN_IN_H


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    MEAN_SPEED_KONST = 1.1
    CALORIES_MEAN_SPEED = 2

    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + self.MEAN_SPEED_KONST) * \
            self.CALORIES_MEAN_SPEED * self.weight * self.duration


TYPES_TRENING = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in TYPES_TRENING.keys():
        return TYPES_TRENING[workout_type](*data)
    return 'Неверный тип тренировки'


def main(training: Training) -> None:
    message = training.show_training_info().get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
