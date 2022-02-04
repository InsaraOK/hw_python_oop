from dataclasses import dataclass
from typing import Any, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    PHRASE_TO_PRINT = ('Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Cр. скорость: {speed:.3f} км/ч; ' 
        'Потрачено ккал: {calories:.3f}.')
    
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
        
    def get_message(self) -> str:
        return self.PHRASE_TO_PRINT.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )    


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
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
    RUN_CAL1 = 18  # множитель для средней скорости
    RUN_CAL2 = 20  # вычитаемая костанта из значения средней скорости
    MIN_IN_1HOUR = 60 
    
    def get_spent_calories(self) -> float:
        return ((
            self.RUN_CAL1 * self.get_mean_speed()
            - self.RUN_CAL2) * self.weight / self.M_IN_KM 
            * self.duration * self.MIN_IN_1HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WALK_CAL1 = 0.035  # множитель для веса
    WALK_CAL2 = 0.029  # множитель для скорости
    MIN_IN_1HOUR = 60
   
    height: float
        
    def get_spent_calories(self) -> float:
        return (
            self.WALK_CAL1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.WALK_CAL2 * self.weight) * self.duration * self.MIN_IN_1HOUR
       

@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIM_CAL1 = 1.1  # множитель для средней скорости
    SWIM_CAL2 = 2  # множитель для веса

    length_pool: float
    count_pool: float
    
    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed()
            + self.SWIM_CAL1) * self.SWIM_CAL2 * self.weight
        

ACTIVITIES: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}
PARAMETERS_NAMBER: Dict[str, int] = {
    'SWM': 5,
    'RUN': 3,
    'WLK': 4
}
  

def read_package(workout_type: str, data: Any) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in ACTIVITIES:         
        return ACTIVITIES[workout_type](*data)
    elif workout_type not in ACTIVITIES:
        raise ValueError('Тип тренировки не известен')
    elif len(data) != PARAMETERS_NAMBER[workout_type]: 
        raise ValueError('Тип тренировки не известен') 
    

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
