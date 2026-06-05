import math


def calculate_rescue_time(d1, d2, h, v_sand, n, theta1):
    FEET_PER_YARD = 3
    FEET_PER_MILE = 5280

    d1_feet = d1 * FEET_PER_YARD
    h_feet = h * FEET_PER_YARD
    theta1_rad = math.radians(theta1)

    x = d1_feet * math.tan(theta1_rad)
    L1 = math.sqrt(x**2 + d1_feet**2)
    L2 = math.sqrt((h_feet - x)**2 + d2**2)

    v_sand_fps = v_sand * FEET_PER_MILE / 3600
    t = (L1 + n * L2) / v_sand_fps

    return t


def main():
    d1 = float(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => "))
    h = float(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => "))
    v_sand = float(input("Введите скорость движения спасателя по песку, v_sand (мили в час) => "))
    n = float(input("Введите коэффициент замедления спасателя при движении в воде, n => "))
    theta1 = float(input("Введите направление движения спасателя по песку, theta1 (градусы) => "))

    time_seconds = calculate_rescue_time(d1, d2, h, v_sand, n, theta1)
    theta1_int = int(theta1)

    print(f"\nЕсли спасатель начнёт движение под углом theta1, равным {theta1_int} градусам, он")
    print(f"достигнет утопающего через {time_seconds:.1f} секунды")


if __name__ == "__main__":
    main()
