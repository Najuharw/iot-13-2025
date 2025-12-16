import logging
import os
from functools import wraps


class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass


def logged(exception, mode="console"):
    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.ERROR)
    logger.handlers.clear()

    handler = (
        logging.StreamHandler()
        if mode == "console"
        else logging.FileHandler("log.txt", encoding="utf-8")
    )

    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception as e:
                logger.error(f"{func.__name__}: {str(e)}")
                raise

        return wrapper

    return decorator


class FileManager:

    @logged(FileNotFound, mode="console")
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            try:
                with open(self.filepath, "w", encoding="utf-8"):
                    pass
            except Exception:
                raise FileNotFound(f"Не вдалося створити файл '{self.filepath}'")

    @logged(FileCorrupted, mode="file")
    def read(self):
        try:
            result = []
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        result.append(line.split(","))
            return result
        except Exception:
            raise FileCorrupted("Файл пошкоджено або недоступний")

    @logged(FileCorrupted, mode="file")
    def write(self, data):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                for row in data:
                    f.write(",".join(map(str, row)) + "\n")
        except Exception:
            raise FileCorrupted("Запис у файл неможливий")

    @logged(FileCorrupted, mode="console")
    def append_sorted(self, row):
        try:
            data = self.read()

            if not data:
                header = ["Ім'я", "Вік"]
                body = []
            else:
                header = data[0]
                body = data[1:]

            body.append([str(item) for item in row])
            body.sort(key=lambda x: int(x[1]))

            self.write([header] + body)

        except Exception:
            raise FileCorrupted("Помилка при додаванні та сортуванні")

    @logged(FileCorrupted, mode="console")
    def show_average(self):
        try:
            data = self.read()
            body = data[1:]

            if not body:
                print("Список порожній")
                return

            ages = [int(person[1]) for person in body]
            avg_age = sum(ages) / len(ages)

            print(
                f"--- Статистика ---\n"
                f"Всього людей: {len(ages)}\n"
                f"Середній вік: {avg_age:.2f} років"
            )

        except Exception:
            raise FileCorrupted("Помилка розрахунку середнього віку")


# ====== TESTING ======

fm = FileManager("data.csv")

fm.write([["Ім'я", "Вік"], ["Інна", 25]])

fm.append_sorted(["Анна", 30])
fm.append_sorted(["Андріана", 4])
fm.append_sorted(["Олег", 60])
fm.append_sorted(["Максим", 16])
fm.append_sorted(["Олена", 19])

print("Вміст відсортованого файлу:")
for line in fm.read():
    print(line)

print()
fm.show_average()
