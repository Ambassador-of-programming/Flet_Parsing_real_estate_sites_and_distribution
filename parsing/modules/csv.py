from typing import List
import datetime
import csv


def append_to_csv(data: List[str]):
    """
    Добавляет новую строку данных в существующий CSV файл.

    :param data: Список строк с данными для добавления
    """
    filename = 'cian_data.csv'
    try:
        with open(filename, 'w+', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Текущая дата и время
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Добавляем дату к данным
            data_with_date = data + [current_date]

            writer.writerow(data_with_date)

    except IOError:
        print(
            f"Ошибка при открытии файла '{filename}'. Убедитесь, что файл существует и доступен для записи.")
    except Exception as e:
        print(f"Произошла ошибка при добавлении данных: {str(e)}")
