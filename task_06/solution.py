import math
import zip_util


def to_dms(decimal_degrees, is_latitude):
    """Преобразует десятичные градусы в формат градусы/минуты/секунды."""
    direction = "N"
    if is_latitude:
        if decimal_degrees < 0:
            direction = "S"
    else:
        if decimal_degrees < 0:
            direction = "W"
        else:
            direction = "E"

    decimal_degrees = abs(decimal_degrees)
    degrees = int(decimal_degrees)
    minutes_float = (decimal_degrees - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60

    return f"{degrees:03d}∘ {minutes}'{seconds:.2f}\"{direction}"


def haversine(lat1, lon1, lat2, lon2):
    """Вычисляет расстояние по формуле гаверсинусов.
    Возвращает расстояние в милях."""
    R = 3958.8

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_by_zip(zip_codes, code):
    """Ищет запись по почтовому индексу."""
    for z in zip_codes:
        if z[0] == code:
            return z
    return None


def find_by_city_state(zip_codes, city, state):
    """Ищет все записи по названию города и штата."""
    result = []
    for z in zip_codes:
        if z[3].lower() == city.lower() and z[4].lower() == state.lower():
            result.append(z)
    return result


def main():
    zip_codes = zip_util.read_zip_all()

    while True:
        cmd = input("Command ('loc', 'zip', 'dist', 'end') => ").strip()

        if not cmd:
            continue

        cmd = cmd.lower()

        if cmd == "end":
            print("Done")
            break

        elif cmd == "loc":
            zip_code = input("Enter a ZIP Code to lookup => ").strip()

            z = find_by_zip(zip_codes, zip_code)
            if z is None:
                print(f"Ошибка: почтовый индекс {zip_code} не найден")
            else:
                lat_dms = to_dms(z[1], True)
                lon_dms = to_dms(z[2], False)
                print(f"ZIP Code {z[0]} is in {z[3]}, {z[4]}, {z[5]} county,")
                print(f"coordinates: ({lat_dms},{lon_dms})")

        elif cmd == "zip":
            city = input("Enter a city name to lookup => ").strip()
            state = input("Enter the state name to lookup => ").strip()

            results = find_by_city_state(zip_codes, city, state)
            if not results:
                print(f"Ошибка: город {city} в штате {state.upper()} не найден")
            else:
                zip_list = []
                for r in results:
                    zip_list.append(r[0])
                print(
                    f"The following ZIP Code(s) found for {results[0][3]}, {results[0][4]}: {', '.join(zip_list)}"
                )

        elif cmd == "dist":
            zip1 = input("Enter the first ZIP Code => ").strip()

            z1 = find_by_zip(zip_codes, zip1)
            if z1 is None:
                print(f"Ошибка: почтовый индекс {zip1} не найден")
                continue

            zip2 = input("Enter the second ZIP Code => ").strip()

            z2 = find_by_zip(zip_codes, zip2)
            if z2 is None:
                print(f"Ошибка: почтовый индекс {zip2} не найден")
                continue

            d = haversine(z1[1], z1[2], z2[1], z2[2])
            print(f"The distance between {zip1} and {zip2} is {d:.2f} miles")

        else:
            print("Invalid command, ignoring")


if __name__ == "__main__":
    main()
