class DataProcessor:
    """Класс для обработки различных типов данных"""
    
    def __init__(self):
        self.data_history = []  # История обработанных данных
    
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
            
            # Дополнительная статистика для числовых списков
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
        """Получение истории обработки"""
        return self.data_history
    
    def clear_history(self):
        """Очистка истории"""
        self.data_history = []
        print("История очищена")


def format_output(result):
    """Форматирование вывода результатов"""
    if not result:
        print("Нет данных для отображения")
        return
    
    if result.get('type') == 'error':
        print(f"❌ Ошибка: {result['error']}")
        return
    
    data_type = result.get('type', 'unknown')
    print(f"\n{'='*50}")
    print(f"📊 Результаты обработки ({data_type.upper()}):")
    print(f"{'='*50}")
    
    for key, value in result.items():
        if key != 'type' and value is not None:
            print(f"  {key.replace('_', ' ').title()}: {value}")
    print(f"{'='*50}\n")


def interactive_mode():
    """Интерактивный режим работы с пользователем"""
    processor = DataProcessor()
    
    print("\n" + "="*60)
    print("🔧 Обработчик данных - Универсальный инструмент")
    print("="*60)
    print("Доступные типы данных:")
    print("  • Числа (целые, дробные)")
    print("  • Текст (строки)")
    print("  • Списки (через запятую)")
    print("  • Логические значения (true/false)")
    print("\nКоманды:")
    print("  • 'exit' - выход из программы")
    print("  • 'history' - показать историю")
    print("  • 'clear' - очистить историю")
    print("="*60)
    
    while True:
        try:
            user_input = input("\n🔽 Введите данные: ").strip()
            
            # Обработка команд
            if user_input.lower() == 'exit':
                print("👋 До свидания!")
                break
            elif user_input.lower() == 'history':
                history = processor.get_history()
                if history:
                    print("\n📜 История обработки:")
                    for i, item in enumerate(history, 1):
                        print(f"{i}. Тип: {item.get('type', 'unknown')} - {item.get('original', 'N/A')}")
                    print(f"\nВсего обработано: {len(history)} записей")
                else:
                    print("📭 История пуста")
                continue
            elif user_input.lower() == 'clear':
                processor.clear_history()
                continue
            
            # Автоматическое определение типа и обработка
            if user_input.lower() in ['true', 'false']:
                # Логические значения
                data = user_input.lower() == 'true'
            elif user_input.replace('.', '').replace('-', '').isdigit():
                # Числа
                data = float(user_input) if '.' in user_input else int(user_input)
            elif ',' in user_input and not user_input.strip().startswith('"'):
                # Списки (простые)
                try:
                    items = [item.strip() for item in user_input.split(',')]
                    # Преобразуем элементы в числа, если возможно
                    converted_items = []
                    for item in items:
                        if item.replace('.', '').replace('-', '').isdigit():
                            converted_items.append(float(item) if '.' in item else int(item))
                        elif item.lower() in ['true', 'false']:
                            converted_items.append(item.lower() == 'true')
                        else:
                            converted_items.append(item)
                    data = converted_items
                except:
                    data = user_input
            else:
                # Текст
                data = user_input
            
            # Обработка данных
            result = processor.auto_detect_and_process(data)
            format_output(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Программа прервана пользователем")
            break
        except Exception as e:
            print(f"❌ Произошла ошибка: {e}")


def batch_mode_example():
    """Пример пакетной обработки данных"""
    print("\n📦 Пакетный режим (пример):")
    processor = DataProcessor()
    
    test_data = [
        42,
        -15.7,
        "Привет, мир!",
        "А роза упала на лапу Азора",
        [1, 2, 3, 4, 5],
        [1.5, 2.3, 3.7, 4.1],
        True,
        False
    ]
    
    for data in test_data:
        print(f"\nОбработка: {data} (тип: {type(data).__name__})")
        result = processor.auto_detect_and_process(data)
        format_output(result)
    
    print(f"\n📊 Статистика: Обработано {len(processor.get_history())} элементов")


if __name__ == "__main__":
    print("Выберите режим работы:")
    print("1 - Интерактивный режим (ввод с клавиатуры)")
    print("2 - Пакетный режим (пример обработки)")
    
    choice = input("Ваш выбор (1 или 2): ").strip()
    
    if choice == "1":
        interactive_mode()
    elif choice == "2":
        batch_mode_example()
    else:
        print("Неверный выбор. Запускаю интерактивный режим...")
        interactive_mode()