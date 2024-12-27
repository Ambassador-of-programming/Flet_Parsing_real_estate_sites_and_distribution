def extract_digits(input_string: str) -> int:
    # Используем генератор списка для извлечения только цифр
    digits = [char for char in input_string if char.isdigit()]

    # Объединяем цифры в строку
    digit_string = ''.join(digits)

    # Если длина больше 11, обрезаем до последних 11 цифр
    if len(digit_string) > 11:
        digit_string = digit_string[-11:]

    # Преобразуем в целое число
    return int(digit_string)
