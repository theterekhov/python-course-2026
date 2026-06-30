import sys

try:
    from PIL import Image
except ImportError:
    print("Ошибка: не установлена библиотека Pillow.")
    print("Установите её командой: pip install Pillow")
    sys.exit(1)


def read_grid(filename):
    """Читает начальную конфигурацию из файла."""
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден")
        sys.exit(1)

    if not lines:
        print("Ошибка: файл пустой")
        sys.exit(1)

    first_line = lines[0].strip().split()
    if len(first_line) != 2:
        print("Ошибка: первая строка должна содержать количество строк и столбцов")
        sys.exit(1)

    try:
        rows = int(first_line[0])
        cols = int(first_line[1])
    except ValueError:
        print("Ошибка: размеры поля должны быть целыми числами")
        sys.exit(1)

    if rows <= 0 or cols <= 0:
        print("Ошибка: размеры поля должны быть положительными числами")
        sys.exit(1)

    grid = []
    for i in range(rows):
        if i + 1 >= len(lines):
            print(f"Ошибка: недостаточно строк в файле, ожидалось {rows}")
            sys.exit(1)
        row = list(lines[i + 1].strip())
        if len(row) < cols:
            row.extend(["."] * (cols - len(row)))
        elif len(row) > cols:
            row = row[:cols]
        grid.append(row)

    return grid, rows, cols


def count_neighbors(grid, row, col, rows, cols):
    """Считает количество живых соседей для клетки."""
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r = row + i
            c = col + j
            if 0 <= r < rows and 0 <= c < cols:
                if grid[r][c] == "O":
                    count += 1
    return count


def next_generation(grid, ages, rows, cols):
    """Вычисляет следующее поколение и обновляет возраст клеток."""
    new_grid = []
    new_ages = []
    for i in range(rows):
        new_grid.append([])
        new_ages.append([])
        for j in range(cols):
            neighbors = count_neighbors(grid, i, j, rows, cols)
            if grid[i][j] == "O":
                if neighbors == 2 or neighbors == 3:
                    new_grid[i].append("O")
                    new_ages[i].append(ages[i][j] + 1)
                else:
                    new_grid[i].append(".")
                    new_ages[i].append(0)
            else:
                if neighbors == 3:
                    new_grid[i].append("O")
                    new_ages[i].append(1)
                else:
                    new_grid[i].append(".")
                    new_ages[i].append(0)
    return new_grid, new_ages


def grid_to_string(grid, rows, cols):
    """Преобразует сетку в строку для вывода."""
    result = []
    for i in range(rows):
        result.append("".join(grid[i]))
    return "\n".join(result)


def get_shade_color(base_r, base_g, base_b, age, max_age):
    """Возвращает цвет клетки в зависимости от возраста.
    Чем старше клетка, тем ближе цвет к базовому.
    Молодые клетки светлее."""
    if age <= 0:
        return (255, 255, 255)
    ratio = min(age / max_age, 1.0)
    r = int(255 + (base_r - 255) * ratio)
    g = int(255 + (base_g - 255) * ratio)
    b = int(255 + (base_b - 255) * ratio)
    return (r, g, b)


def save_image(grid, ages, rows, cols, base_color, filename, cell_size=20):
    """Сохраняет изображение текущего состояния поля."""
    max_age = 10
    base_r = (base_color >> 16) & 0xFF
    base_g = (base_color >> 8) & 0xFF
    base_b = base_color & 0xFF

    img = Image.new("RGB", (cols * cell_size, rows * cell_size), (255, 255, 255))
    pixels = img.load()

    for i in range(rows):
        for j in range(cols):
            color = get_shade_color(base_r, base_g, base_b, ages[i][j], max_age)
            for y in range(cell_size):
                for x in range(cell_size):
                    pixels[j * cell_size + x, i * cell_size + y] = color

    img.save(filename)


def main():
    input_file = input("Введите имя входного файла с конфигурацией => ").strip()
    grid, rows, cols = read_grid(input_file)

    steps_str = input("Введите количество шагов моделирования => ").strip()
    try:
        steps = int(steps_str)
    except ValueError:
        print("Ошибка: количество шагов должно быть целым числом")
        sys.exit(1)

    if steps <= 0:
        print("Ошибка: количество шагов должно быть положительным")
        sys.exit(1)

    color_str = input("Введите базовый цвет в формате RRGGBB => ").strip()
    try:
        base_color = int(color_str, 16)
    except ValueError:
        print("Ошибка: цвет должен быть в формате RRGGBB")
        sys.exit(1)

    if base_color < 0 or base_color > 0xFFFFFF:
        print("Ошибка: цвет должен быть в диапазоне 000000 - FFFFFF")
        sys.exit(1)

    output_prefix = input("Введите префикс для выходных файлов => ").strip()
    if not output_prefix:
        output_prefix = "output"

    ages = []
    for i in range(rows):
        ages.append([])
        for j in range(cols):
            if grid[i][j] == "O":
                ages[i].append(1)
            else:
                ages[i].append(0)

    output_file = output_prefix + ".txt"
    try:
        f_out = open(output_file, "w")
    except IOError:
        print(f"Ошибка: не удалось создать файл '{output_file}'")
        sys.exit(1)

    f_out.write("Начальная конфигурация:\n")
    f_out.write(grid_to_string(grid, rows, cols))
    f_out.write("\n\n")
    save_image(grid, ages, rows, cols, base_color, output_prefix + "_0.png")

    print("\nНачальная конфигурация:")
    print(grid_to_string(grid, rows, cols))
    print()

    for step in range(1, steps + 1):
        grid, ages = next_generation(grid, ages, rows, cols)

        f_out.write(f"Поколение {step}:\n")
        f_out.write(grid_to_string(grid, rows, cols))
        f_out.write("\n\n")
        save_image(grid, ages, rows, cols, base_color, f"{output_prefix}_{step}.png")

        print(f"Поколение {step}:")
        print(grid_to_string(grid, rows, cols))
        print()

    f_out.close()
    print(f"Результаты сохранены в файл {output_file}")
    print(
        f"Изображения сохранены как {output_prefix}_0.png ... {output_prefix}_{steps}.png"
    )
    print("Симуляция завершена")


if __name__ == "__main__":
    main()
