from dataclasses import dataclass, fields, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    SPEED_MULTIPLIER = 18
    SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        return ((
            self.SPEED_MULTIPLIER * self.get_mean_speed()
            - self.SPEED_SHIFT) * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        return ((
            self.WEIGHT_MULTIPLIER_1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.WEIGHT_MULTIPLIER_2 * self.weight)
            * (self.duration * self.MIN_IN_HOUR)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
                + self.SPEED_SHIFT) * self.SPEED_MULTIPLIER * self.weight


ACTIVITIES = {
    'SWM': (Swimming, len(fields(Swimming))),
    'RUN': (Running, len(fields(Running))),
    'WLK': (SportsWalking, len(fields(SportsWalking)))
}
TYPE_VALUERROR = ('Тип тренировки {type} не известен')
DATA_VALUERROR = ('Задано не верное количество параметров {wrong_number}',
                  'для данного типа тренировки {type},',
                  ' необходимо {true_number}')


def read_package(workout_type: str, data: float) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in ACTIVITIES:
        raise ValueError(TYPE_VALUERROR.format(type=workout_type))
    activities_data = ACTIVITIES[workout_type]
    if len(data) != activities_data[1]:
        raise ValueError(
            DATA_VALUERROR.format(
                wrong_number=len(data),
                type=workout_type,
                true_number=activities_data[1])
        )
    return activities_data[0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
