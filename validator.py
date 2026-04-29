def validate_pages(pages_str: str) -> bool:
    """
    Проверяет, что строка является положительным целым числом (количество страниц).

    Args:
        pages_str: Строка с количеством страниц.

    Returns:
        bool: True если значение — положительное целое число.
    """
    try:
        value = int(pages_str.strip())
        return value > 0
    except ValueError:
        return False


def validate_not_empty(value: str) -> bool:
    """
    Проверяет, что строка не является пустой.

    Args:
        value: Строка для проверки.

    Returns:
        bool: True если строка не пустая.
    """
    return bool(value.strip())
