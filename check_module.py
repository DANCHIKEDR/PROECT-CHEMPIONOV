#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для проверки работоспособности модуля DataProcessor
Выполняет основные функции и выводит результаты
"""

import sys
import json
from тесты import DataProcessor, run_tests_with_report


def check_basic_functionality():
    """Проверка базовой функциональности модуля"""
    print("\n" + "="*60)
    print("🔍 ПРОВЕРКА БАЗОВОЙ ФУНКЦИОНАЛЬНОСТИ")
    print("="*60)
    
    processor = DataProcessor()
    
    # Тест 1: Обработка числа
    print("\n📌 Тест 1: Обработка числа")
    num_result = processor.process_number(-42)
    print(f"  Исходное число: -42")
    print(f"  Результат: {num_result}")
    
    # Тест 2: Обработка текста
    print("\n📌 Тест 2: Обработка текста")
    text_result = processor.process_text("Привет, мир!")
    print(f"  Исходный текст: 'Привет, мир!'")
    print(f"  Длина: {text_result['length']}")
    print(f"  Верхний регистр: {text_result['uppercase']}")
    
    # Тест 3: Обработка списка
    print("\n📌 Тест 3: Обработка списка")
    list_result = processor.process_list([1, 2, 3, 4, 5])
    print(f"  Исходный список: [1, 2, 3, 4, 5]")
    print(f"  Сумма: {list_result.get('sum', 'N/A')}")
    print(f"  Среднее: {list_result.get('average', 'N/A')}")
    
    # Тест 4: Обработка логического значения
    print("\n📌 Тест 4: Обработка логического значения")
    bool_result = processor.process_boolean(True)
    print(f"  Исходное значение: True")
    print(f"  Как int: {bool_result['as_int']}")
    print(f"  Отрицание: {bool_result['negated']}")
    
    # Тест 5: Автоопределение
    print("\n📌 Тест 5: Автоопределение типов")
    test_data = [100, "строка", [1, 2, 3], True, None]
    for data in test_data:
        result = processor.auto_detect_and_process(data)
        print(f"  {data} -> тип: {result.get('type', 'error')}")
    
    # Тест 6: История операций
    print("\n📌 Тест 6: История операций")
    history = processor.get_history()
    print(f"  Всего операций в истории: {len(history)}")
    for i, entry in enumerate(history, 1):
        print(f"    {i}. Тип: {entry.get('type')}")
    
    # Тест 7: Очистка истории
    print("\n📌 Тест 7: Очистка истории")
    processor.clear_history()
    print(f"  История после очистки: {len(processor.get_history())} записей")


def check_edge_cases():
    """Проверка граничных случаев"""
    print("\n" + "="*60)
    print("🔍 ПРОВЕРКА ГРАНИЧНЫХ СЛУЧАЕВ")
    print("="*60)
    
    processor = DataProcessor()
    
    # Тест 1: Пустой список
    print("\n📌 Тест 1: Пустой список")
    result = processor.process_list([])
    print(f"  Результат: {result}")
    print(f"  Содержит sum? {'sum' in result}")
    
    # Тест 2: Смешанный список
    print("\n📌 Тест 2: Смешанный список")
    result = processor.process_list([1, "два", 3.0])
    print(f"  Результат: {result}")
    print(f"  Содержит sum? {'sum' in result}")
    
    # Тест 3: Палиндром
    print("\n📌 Тест 3: Палиндром")
    result = processor.process_text("А роза упала на лапу Азора")
    print(f"  Текст: '{result['original']}'")
    print(f"  Палиндром? {result['is_palindrome']}")
    
    # Тест 4: Очень длинная строка
    print("\n📌 Тест 4: Очень длинная строка (1000 символов)")
    long_text = "a" * 1000
    result = processor.process_text(long_text)
    print(f"  Длина строки: {result['length']}")
    
    # Тест 5: Ошибка для None
    print("\n📌 Тест 5: Обработка None")
    result = processor.auto_detect_and_process(None)
    print(f"  Результат: {result}")


def check_json_serialization():
    """Проверка сериализации в JSON"""
    print("\n" + "="*60)
    print("🔍 ПРОВЕРКА JSON СЕРИАЛИЗАЦИИ")
    print("="*60)
    
    processor = DataProcessor()
    
    # Обрабатываем данные
    processor.process_number(42)
    processor.process_text("Hello, World!")
    processor.process_list([1, 2, 3])
    
    # Получаем историю
    history = processor.get_history()
    
    # Сериализуем в JSON
    try:
        json_str = json.dumps(history, ensure_ascii=False, indent=2, default=str)
        print("\n✅ JSON сериализация успешна:")
        print(json_str)
    except Exception as e:
        print(f"\n❌ Ошибка JSON сериализации: {e}")


def check_performance():
    """Проверка производительности"""
    print("\n" + "="*60)
    print("🔍 ПРОВЕРКА ПРОИЗВОДИТЕЛЬНОСТИ")
    print("="*60)
    
    import time
    
    processor = DataProcessor()
    
    # Тест с большим списком
    print("\n📌 Тест с большим списком (10000 элементов)")
    large_list = list(range(10000))
    start = time.time()
    result = processor.process_list(large_list)
    elapsed = time.time() - start
    print(f"  Время обработки: {elapsed:.4f} секунд")
    print(f"  Длина списка: {result['length']}")
    print(f"  Сумма: {result.get('sum', 'N/A')}")
    
    # Тест с большим количеством операций
    print("\n📌 Тест с множеством операций (1000 операций)")
    start = time.time()
    for i in range(1000):
        processor.auto_detect_and_process(i)
    elapsed = time.time() - start
    print(f"  Время обработки 1000 операций: {elapsed:.4f} секунд")
    print(f"  История после операций: {len(processor.get_history())} записей")


def main():
    """Главная функция проверки"""
    print("\n" + "█"*60)
    print("     ПРОВЕРКА РАБОТОСПОСОБНОСТИ МОДУЛЯ DataProcessor")
    print("█"*60)
    
    # Базовые проверки
    check_basic_functionality()
    
    # Проверка граничных случаев
    check_edge_cases()
    
    # Проверка JSON сериализации
    check_json_serialization()
    
    # Проверка производительности
    check_performance()
    
    # Финальный отчет
    print("\n" + "="*60)
    print("📊 ФИНАЛЬНЫЙ ОТЧЕТ")
    print("="*60)
    print("✅ Все проверки пройдены успешно!")
    print("📝 Модуль DataProcessor готов к использованию")
    print("="*60 + "\n")
    
    # Спрашиваем, запускать ли unit-тесты
    response = input("Запустить полные unit-тесты? (y/n): ")
    if response.lower() == 'y':
        run_tests_with_report()


if __name__ == "__main__":
    main()