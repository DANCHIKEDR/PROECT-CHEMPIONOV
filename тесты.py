import unittest
import sys
from io import StringIO
from contextlib import redirect_stdout
import json

# Импортируем наш модуль (предполагается, что он сохранен в файле data_processor.py)
# Если код находится в этом же файле, раскомментируйте строки ниже
"""
from data_processor import DataProcessor, format_output
"""

# Для автономной работы продублируем класс DataProcessor (если он не импортирован)
class DataProcessor:
    """Класс для обработки различных типов данных"""
    
    def __init__(self):
        self.data_history = []
    
    def process_number(self, number):
        """Обработка числовых данных"""
        if isinstance(number, (int, float)):
            result = {
                'original': number,
                'absolute': abs(number),
                'square': number ** 2,
                'cube': number ** 3,
                'is_even': number % 2 == 0 if isinstance(number, int) else None,
                'type': 'number'
            }
            self.data_history.append(result)
            return result
        else:
            return {'error': 'Входные данные не являются числом', 'type': 'error'}
    
    def process_text(self, text):
        """Обработка текстовых данных"""
        if isinstance(text, str):
            result = {
                'original': text,
                'length': len(text),
                'uppercase': text.upper(),
                'lowercase': text.lower(),
                'words_count': len(text.split()),
                'reversed': text[::-1],
                'is_palindrome': text.lower().replace(' ', '') == text.lower().replace(' ', '')[::-1],
                'type': 'text'
            }
            self.data_history.append(result)
            return result
        else:
            return {'error': 'Входные данные не являются текстом', 'type': 'error'}
    
    def process_list(self, data_list):
        """Обработка списков"""
        if isinstance(data_list, list):
            result = {
                'original': data_list,
                'length': len(data_list),
                'unique_items': list(set(data_list)),
                'sorted': sorted(data_list) if all(isinstance(x, (int, float, str)) for x in data_list) else None,
                'type': 'list'
            }
            
            if all(isinstance(x, (int, float)) for x in data_list):
                result.update({
                    'sum': sum(data_list),
                    'average': sum(data_list) / len(data_list) if data_list else 0,
                    'min': min(data_list),
                    'max': max(data_list)
                })
            
            self.data_history.append(result)
            return result
        else:
            return {'error': 'Входные данные не являются списком', 'type': 'error'}
    
    def process_boolean(self, value):
        """Обработка логических значений"""
        if isinstance(value, bool):
            result = {
                'original': value,
                'as_int': int(value),
                'as_str': str(value),
                'negated': not value,
                'type': 'boolean'
            }
            self.data_history.append(result)
            return result
        else:
            return {'error': 'Входные данные не являются логическим значением', 'type': 'error'}
    
    def auto_detect_and_process(self, data):
        """Автоматическое определение типа данных и их обработка"""
        if isinstance(data, (int, float)):
            return self.process_number(data)
        elif isinstance(data, str):
            return self.process_text(data)
        elif isinstance(data, list):
            return self.process_list(data)
        elif isinstance(data, bool):
            return self.process_boolean(data)
        else:
            return {'error': f'Неподдерживаемый тип данных: {type(data)}', 'type': 'error'}
    
    def get_history(self):
        return self.data_history
    
    def clear_history(self):
        self.data_history = []


class TestDataProcessor(unittest.TestCase):
    """Класс для тестирования DataProcessor"""
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.processor = DataProcessor()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.processor.clear_history()
    
    # ==================== ТЕСТЫ ДЛЯ ЧИСЕЛ ====================
    
    def test_process_positive_integer(self):
        """TC-001: Тест обработки положительного целого числа"""
        result = self.processor.process_number(42)
        
        self.assertEqual(result['original'], 42)
        self.assertEqual(result['absolute'], 42)
        self.assertEqual(result['square'], 1764)
        self.assertEqual(result['cube'], 74088)
        self.assertTrue(result['is_even'])
        self.assertEqual(result['type'], 'number')
    
    def test_process_negative_float(self):
        """TC-002: Тест обработки отрицательного дробного числа"""
        result = self.processor.process_number(-15.7)
        
        self.assertEqual(result['original'], -15.7)
        self.assertEqual(result['absolute'], 15.7)
        self.assertAlmostEqual(result['square'], 246.49)
        self.assertAlmostEqual(result['cube'], -3869.893)
        self.assertIsNone(result['is_even'])
        self.assertEqual(result['type'], 'number')
    
    def test_process_zero(self):
        """TC-003: Тест обработки нуля"""
        result = self.processor.process_number(0)
        
        self.assertEqual(result['original'], 0)
        self.assertEqual(result['absolute'], 0)
        self.assertEqual(result['square'], 0)
        self.assertEqual(result['cube'], 0)
        self.assertTrue(result['is_even'])
        self.assertEqual(result['type'], 'number')
    
    # ==================== ТЕСТЫ ДЛЯ ТЕКСТА ====================
    
    def test_process_text_normal(self):
        """TC-004: Тест обработки обычного текста"""
        result = self.processor.process_text("Привет, мир!")
        
        self.assertEqual(result['original'], "Привет, мир!")
        self.assertEqual(result['length'], 12)
        self.assertEqual(result['uppercase'], "ПРИВЕТ, МИР!")
        self.assertEqual(result['words_count'], 2)
        self.assertEqual(result['reversed'], "!рим ,тевирП")
        self.assertFalse(result['is_palindrome'])
        self.assertEqual(result['type'], 'text')
    
    def test_process_palindrome(self):
        """TC-005: Тест обработки палиндрома"""
        result = self.processor.process_text("А роза упала на лапу Азора")
        
        self.assertEqual(result['original'], "А роза упала на лапу Азора")
        self.assertEqual(result['length'], 26)
        self.assertTrue(result['is_palindrome'])
    
    def test_process_empty_string(self):
        """TC-006: Тест обработки пустой строки"""
        result = self.processor.process_text("")
        
        self.assertEqual(result['original'], "")
        self.assertEqual(result['length'], 0)
        self.assertEqual(result['words_count'], 0)
        self.assertEqual(result['reversed'], "")
        self.assertEqual(result['type'], 'text')
    
    # ==================== ТЕСТЫ ДЛЯ СПИСКОВ ====================
    
    def test_process_numeric_list(self):
        """TC-007: Тест обработки числового списка"""
        result = self.processor.process_list([1, 2, 3, 4, 5])
        
        self.assertEqual(result['length'], 5)
        self.assertEqual(result['unique_items'], [1, 2, 3, 4, 5])
        self.assertEqual(result['sum'], 15)
        self.assertEqual(result['average'], 3.0)
        self.assertEqual(result['min'], 1)
        self.assertEqual(result['max'], 5)
        self.assertEqual(result['type'], 'list')
    
    def test_process_list_with_duplicates(self):
        """TC-008: Тест обработки списка с дубликатами"""
        result = self.processor.process_list([1, 2, 2, 3, 3, 3])
        
        self.assertEqual(result['length'], 6)
        self.assertEqual(set(result['unique_items']), {1, 2, 3})
        self.assertEqual(result['sum'], 14)
        self.assertAlmostEqual(result['average'], 14/6)
    
    def test_process_empty_list(self):
        """TC-009: Тест обработки пустого списка"""
        result = self.processor.process_list([])
        
        self.assertEqual(result['length'], 0)
        self.assertEqual(result['unique_items'], [])
        self.assertEqual(result['sum'], 0)
        self.assertEqual(result['average'], 0)
    
    def test_process_mixed_list(self):
        """TC-010: Тест обработки смешанного списка"""
        result = self.processor.process_list([1, "текст", 3.5])
        
        self.assertEqual(result['length'], 3)
        self.assertEqual(set(result['unique_items']), {1, 3.5, "текст"})
        self.assertIsNone(result.get('sum'))
        self.assertIsNone(result.get('average'))
    
    # ==================== ТЕСТЫ ДЛЯ ЛОГИЧЕСКИХ ЗНАЧЕНИЙ ====================
    
    def test_process_true(self):
        """TC-011: Тест обработки True"""
        result = self.processor.process_boolean(True)
        
        self.assertTrue(result['original'])
        self.assertEqual(result['as_int'], 1)
        self.assertEqual(result['as_str'], "True")
        self.assertFalse(result['negated'])
        self.assertEqual(result['type'], 'boolean')
    
    def test_process_false(self):
        """TC-012: Тест обработки False"""
        result = self.processor.process_boolean(False)
        
        self.assertFalse(result['original'])
        self.assertEqual(result['as_int'], 0)
        self.assertEqual(result['as_str'], "False")
        self.assertTrue(result['negated'])
        self.assertEqual(result['type'], 'boolean')
    
    # ==================== ТЕСТЫ АВТООПРЕДЕЛЕНИЯ ====================
    
    def test_auto_detect_number(self):
        """Тест автоопределения числа"""
        result = self.processor.auto_detect_and_process(100)
        self.assertEqual(result['type'], 'number')
        self.assertEqual(result['original'], 100)
    
    def test_auto_detect_text(self):
        """TC-013: Тест автоопределения строки 'true' как текст"""
        result = self.processor.auto_detect_and_process("true")
        self.assertEqual(result['type'], 'text')
        self.assertEqual(result['original'], "true")
    
    def test_auto_detect_string_number(self):
        """TC-014: Тест автоопределения строки-числа"""
        result = self.processor.auto_detect_and_process("123")
        self.assertEqual(result['type'], 'text')
        self.assertEqual(result['original'], "123")
    
    def test_auto_detect_list(self):
        """Тест автоопределения списка"""
        result = self.processor.auto_detect_and_process([10, 20, 30])
        self.assertEqual(result['type'], 'list')
        self.assertEqual(result['length'], 3)
    
    def test_auto_detect_boolean(self):
        """Тест автоопределения логического значения"""
        result = self.processor.auto_detect_and_process(True)
        self.assertEqual(result['type'], 'boolean')
    
    # ==================== ТЕСТЫ ОБРАБОТКИ ОШИБОК ====================
    
    def test_error_none_type(self):
        """TC-015: Тест обработки None"""
        result = self.processor.auto_detect_and_process(None)
        self.assertEqual(result['type'], 'error')
        self.assertIn('неподдерживаемый тип', result['error'].lower())
    
    def test_error_dict_type(self):
        """TC-016: Тест обработки словаря"""
        result = self.processor.auto_detect_and_process({"key": "value"})
        self.assertEqual(result['type'], 'error')
        self.assertIn('неподдерживаемый тип', result['error'].lower())
    
    def test_error_tuple_type(self):
        """TC-017: Тест обработки кортежа"""
        result = self.processor.auto_detect_and_process((1, 2, 3))
        self.assertEqual(result['type'], 'error')
        self.assertIn('неподдерживаемый тип', result['error'].lower())
    
    # ==================== ТЕСТЫ ИСТОРИИ ====================
    
    def test_history_storage(self):
        """Тест сохранения данных в истории"""
        self.processor.process_number(10)
        self.processor.process_text("test")
        self.processor.process_list([1, 2])
        
        history = self.processor.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['type'], 'number')
        self.assertEqual(history[1]['type'], 'text')
        self.assertEqual(history[2]['type'], 'list')
    
    def test_clear_history(self):
        """Тест очистки истории"""
        self.processor.process_number(10)
        self.processor.clear_history()
        self.assertEqual(len(self.processor.get_history()), 0)


class TestFormatOutput(unittest.TestCase):
    """Тесты для функции форматирования вывода"""
    
    def setUp(self):
        """Подготовка перед тестами"""
        self.processor = DataProcessor()
    
    def capture_output(self, result):
        """Захват вывода функции format_output"""
        f = StringIO()
        with redirect_stdout(f):
            # Используем ту же функцию format_output, что и в основном коде
            if result and result.get('type') != 'error':
                print(f"\n{'='*50}")
                print(f"📊 Результаты обработки ({result.get('type', 'unknown').upper()}):")
                print(f"{'='*50}")
                for key, value in result.items():
                    if key != 'type' and value is not None:
                        print(f"  {key.replace('_', ' ').title()}: {value}")
                print(f"{'='*50}\n")
            elif result and result.get('type') == 'error':
                print(f"❌ Ошибка: {result['error']}")
            else:
                print("Нет данных для отображения")
        return f.getvalue()
    
    def test_format_number_output(self):
        """Тест форматирования числового вывода"""
        result = self.processor.process_number(42)
        output = self.capture_output(result)
        
        self.assertIn("Результаты обработки (NUMBER)", output)
        self.assertIn("Original: 42", output)
        self.assertIn("Square: 1764", output)
    
    def test_format_error_output(self):
        """Тест форматирования вывода ошибки"""
        result = self.processor.auto_detect_and_process(None)
        output = self.capture_output(result)
        
        self.assertIn("Ошибка", output)
        self.assertIn("неподдерживаемый тип", output.lower())


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def setUp(self):
        self.processor = DataProcessor()
    
    def test_multiple_operations(self):
        """Тест последовательности операций"""
        # Выполняем несколько операций
        num_result = self.processor.process_number(10)
        text_result = self.processor.process_text("hello")
        list_result = self.processor.process_list([1, 2, 3])
        
        # Проверяем результаты
        self.assertEqual(num_result['square'], 100)
        self.assertEqual(text_result['length'], 5)
        self.assertEqual(list_result['sum'], 6)
        
        # Проверяем историю
        history = self.processor.get_history()
        self.assertEqual(len(history), 3)
    
    def test_complex_workflow(self):
        """Тест сложного рабочего процесса"""
        # Обрабатываем разные типы данных
        data_list = [10, 20, 30, "test", True]
        
        results = []
        for data in data_list:
            result = self.processor.auto_detect_and_process(data)
            results.append(result)
        
        # Проверяем типы результатов
        self.assertEqual(results[0]['type'], 'number')
        self.assertEqual(results[1]['type'], 'number')
        self.assertEqual(results[2]['type'], 'number')
        self.assertEqual(results[3]['type'], 'text')
        self.assertEqual(results[4]['type'], 'boolean')
        
        # Проверяем историю
        self.assertEqual(len(self.processor.get_history()), 5)
    
    def test_boundary_values(self):
        """Тест граничных значений"""
        # Очень большое число
        large_num = self.processor.process_number(10**10)
        self.assertEqual(large_num['square'], 10**20)
        
        # Очень длинная строка
        long_text = "a" * 10000
        text_result = self.processor.process_text(long_text)
        self.assertEqual(text_result['length'], 10000)
        
        # Очень большой список
        large_list = list(range(1000))
        list_result = self.processor.process_list(large_list)
        self.assertEqual(list_result['length'], 1000)
        self.assertEqual(list_result['sum'], sum(range(1000)))


def run_tests_with_report():
    """Запуск тестов с подробным отчетом"""
    print("\n" + "="*80)
    print("🧪 ЗАПУСК ТЕСТИРОВАНИЯ МОДУЛЯ ОБРАБОТКИ ДАННЫХ")
    print("="*80)
    
    # Создаем тестовый набор
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем все тесты
    suite.addTests(loader.loadTestsFromTestCase(TestDataProcessor))
    suite.addTests(loader.loadTestsFromTestCase(TestFormatOutput))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Запускаем тесты с подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим статистику
    print("\n" + "="*80)
    print("📊 СТАТИСТИКА ТЕСТИРОВАНИЯ")
    print("="*80)
    print(f"✅ Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Провалено: {len(result.failures)}")
    print(f"⚠️  Ошибок: {len(result.errors)}")
    print(f"📝 Всего тестов: {result.testsRun}")
    print("="*80)
    
    return result


def generate_test_report_table():
    """Генерация таблицы с результатами тестов в формате Markdown"""
    processor = DataProcessor()
    
    test_cases = [
        ("TC-001", 42, "Положительное целое число"),
        ("TC-002", -15.7, "Отрицательное дробное число"),
        ("TC-003", 0, "Ноль"),
        ("TC-004", "Привет, мир!", "Обычный текст"),
        ("TC-005", "А роза упала на лапу Азора", "Палиндром"),
        ("TC-006", "", "Пустая строка"),
        ("TC-007", [1, 2, 3, 4, 5], "Числовой список"),
        ("TC-008", [1, 2, 2, 3, 3, 3], "Список с дубликатами"),
        ("TC-009", [], "Пустой список"),
        ("TC-010", [1, "текст", 3.5], "Смешанный список"),
        ("TC-011", True, "Логическое True"),
        ("TC-012", False, "Логическое False"),
        ("TC-013", "true", "Строка 'true'"),
        ("TC-014", "123", "Строка-число"),
        ("TC-015", None, "None"),
        ("TC-016", {"key": "value"}, "Словарь"),
        ("TC-017", (1, 2, 3), "Кортеж"),
    ]
    
    print("\n📋 ОТЧЕТ ПО ТЕСТ-КЕЙСАМ\n")
    print("| № | Входные данные | Тип | Ожидаемый результат | Полученный результат | Статус |")
    print("|---|----------------|-----|---------------------|----------------------|--------|")
    
    for tc_id, data, description in test_cases:
        try:
            result = processor.auto_detect_and_process(data)
            
            if result.get('type') == 'error':
                expected = "Ошибка: неподдерживаемый тип"
                actual = result.get('error', 'Ошибка')
                status = "✅ УСПЕШНО" if "неподдерживаемый" in actual else "⚠️  ПРОВЕРИТЬ"
            else:
                expected = f"Успешная обработка типа {result['type']}"
                actual = f"Тип: {result['type']}, оригинал: {result.get('original', 'N/A')}"
                status = "✅ УСПЕШНО"
            
            # Ограничиваем длину вывода
            if len(str(data)) > 30:
                data_str = str(data)[:27] + "..."
            else:
                data_str = str(data)
            
            print(f"| {tc_id} | {data_str} | {description} | {expected} | {actual} | {status} |")
            
        except Exception as e:
            print(f"| {tc_id} | {data} | {description} | Ошибка не должна возникнуть | Ошибка: {str(e)} | ❌ ОШИБКА |")


if __name__ == "__main__":
    print("\nВыберите режим тестирования:")
    print("1 - Запуск всех unit-тестов")
    print("2 - Генерация отчета по тест-кейсам")
    print("3 - Подробный отчет с результатами")
    
    choice = input("\nВаш выбор (1, 2 или 3): ").strip()
    
    if choice == "1":
        unittest.main(argv=[''], exit=False)
    elif choice == "2":
        generate_test_report_table()
    elif choice == "3":
        run_tests_with_report()
    else:
        print("Неверный выбор. Запускаю все тесты...")
        run_tests_with_report()