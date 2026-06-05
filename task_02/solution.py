import math


def convert_yards_to_feet(yards):
    return yards * 3


def convert_mph_to_fps(mph):
    return mph * 5280 / 3600


def calculate_distance_on_sand(d1, theta1_degrees):
    d1_feet = convert_yards_to_feet(d1)
    theta1_rad = math.radians(theta1_degrees)
    x = d1_feet * math.tan(theta1_rad)
    L1 = math.sqrt(x ** 2 + d1_feet ** 2)
    return L1, x


def calculate_distance_in_water(h, x, d2):
    h_feet = convert_yards_to_feet(h)
    L2 = math.sqrt((h_feet - x) ** 2 + d2 ** 2)
    return L2


def calculate_total_time(L1, L2, v_sand, n):
    v_sand_fps = convert_mph_to_fps(v_sand)
    t = (L1 + n * L2) / v_sand_fps
    return t


def get_input_values():
    d1 = float(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => "))
    h = float(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => "))
    v_sand = float(input("Введите скорость движения спасателя по песку, v_sand (мили в час) => "))
    n = float(input("Введите коэффициент замедления спасателя при движении в воде, n => "))
    theta1 = float(input("Введите направление движения спасателя по песку, theta1 (градусы) => "))
    return d1, d2, h, v_sand, n, theta1


def display_result(theta1, time_seconds):
    theta1_int = int(theta1)
    print(f"\nЕсли спасатель начнёт движение под углом theta1, равным {theta1_int} градусам, он")
    print(f"достигнет утопающего через {time_seconds:.1f} секунды")


def main():
    d1, d2, h, v_sand, n, theta1 = get_input_values()
    L1, x = calculate_distance_on_sand(d1, theta1)
    L2 = calculate_distance_in_water(h, x, d2)
    time_seconds = calculate_total_time(L1, L2, v_sand, n)
    display_result(theta1, time_seconds)


# Модульные тесты
def test_convert_yards_to_feet():
    assert convert_yards_to_feet(1) == 3
    assert convert_yards_to_feet(8) == 24
    assert convert_yards_to_feet(50) == 150


def test_convert_mph_to_fps():
    result = convert_mph_to_fps(5)
    expected = 5 * 5280 / 3600
    assert abs(result - expected) < 0.0001


def test_calculate_distance_on_sand():
    L1, x = calculate_distance_on_sand(8, 39.413)
    assert L1 > 0
    assert x > 0


def test_calculate_distance_in_water():
    x = 50
    L2 = calculate_distance_in_water(50, x, 10)
    assert L2 > 0


def test_calculate_total_time():
    v_sand = 5
    n = 2
    L1 = 100
    L2 = 50
    t = calculate_total_time(L1, L2, v_sand, n)
    assert t > 0


if __name__ == "__main__":
    test_convert_yards_to_feet()
    test_convert_mph_to_fps()
    test_calculate_distance_on_sand()
    test_calculate_distance_in_water()
    test_calculate_total_time()
    print("Все тесты пройдены!")
    main()
