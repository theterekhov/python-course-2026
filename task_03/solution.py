import math


def convert_yards_to_feet(yards):
    return yards * 3


def convert_mph_to_fps(mph):
    return mph * 5280 / 3600


def calculate_time(d1, d2, h, v_sand, n, theta1):
    d1_feet = convert_yards_to_feet(d1)
    h_feet = convert_yards_to_feet(h)
    theta1_rad = math.radians(theta1)
    
    x = d1_feet * math.tan(theta1_rad)
    L1 = math.sqrt(x ** 2 + d1_feet ** 2)
    L2 = math.sqrt((h_feet - x) ** 2 + d2 ** 2)
    
    v_sand_fps = convert_mph_to_fps(v_sand)
    t = (L1 + n * L2) / v_sand_fps
    
    return t


def find_optimal_angle(d1, d2, h, v_sand, n):
    min_time = float('inf')
    optimal_angle = 0
    
    for angle in range(0, 91):
        t = calculate_time(d1, d2, h, v_sand, n, angle)
        if t < min_time:
            min_time = t
            optimal_angle = angle
    
    for angle in range(0, 91):
        for dec in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            precise_angle = angle + dec
            t = calculate_time(d1, d2, h, v_sand, n, precise_angle)
            if t < min_time:
                min_time = t
                optimal_angle = precise_angle
    
    return optimal_angle, min_time


def get_input_values():
    d1 = float(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => "))
    h = float(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => "))
    v_sand = float(input("Введите скорость движения спасателя по песку, v_sand (мили в час) => "))
    n = float(input("Введите коэффициент замедления спасателя при движении в воде, n => "))
    return d1, d2, h, v_sand, n


def main():
    d1, d2, h, v_sand, n = get_input_values()
    
    optimal_angle, min_time = find_optimal_angle(d1, d2, h, v_sand, n)
    
    print(f"\nОптимальный угол: {optimal_angle:.1f} градусов")
    print(f"Минимальное время: {min_time:.1f} секунды")
    
    time_at_39 = calculate_time(d1, d2, h, v_sand, n, 39.413)
    print(f"\nДля сравнения (угол 39.4°): {time_at_39:.1f} секунды")
    print(f"Экономия времени: {time_at_39 - min_time:.1f} секунды")


if __name__ == "__main__":
    main()
