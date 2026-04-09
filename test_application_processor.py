import unittest
from application_processor import ApplicationProcessor


class TestApplicationProcessor(unittest.TestCase):
    
    def setUp(self):
        """Создание нового экземпляра перед каждым тестом"""
        self.processor = ApplicationProcessor()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.processor = None
    
    # Позитивные тесты
    def test_register_participant_success(self):
        result = self.processor.register_participant(1, "Анна Сидорова", "anna@mail.ru")
        self.assertTrue(result["success"])
        self.assertEqual(len(self.processor.participants), 1)
    
    def test_register_participant_valid_email(self):
        result = self.processor.register_participant(2, "Петр Иванов", "petr@gmail.com")
        self.assertTrue(result["success"])
    
    def test_submit_application_success(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        result = self.processor.submit_application(100, "Моя статья", 1, "article.pdf")
        self.assertTrue(result["success"])
        self.assertEqual(len(self.processor.applications), 1)
    
    def test_submit_application_with_title_stripped(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        result = self.processor.submit_application(101, "  Статья с пробелами  ", 1, "doc.docx")
        self.assertTrue(result["success"])
        self.assertEqual(result["application"].title, "Статья с пробелами")
    
    def test_get_application_status(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        self.processor.submit_application(200, "Тестовая статья", 1, "file.pdf")
        result = self.processor.get_application_status(200)
        self.assertTrue(result["success"])
        self.assertEqual(result["status"], "pending")
    
    def test_update_status(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        self.processor.submit_application(300, "Статья для модерации", 1, "paper.pdf")
        result = self.processor.update_status(300, "approved")
        self.assertTrue(result["success"])
        self.assertEqual(result["application"].status, "approved")
    
    def test_statistics(self):
        self.processor.register_participant(1, "Участник1", "test1@mail.com")
        self.processor.register_participant(2, "Участник2", "test2@mail.com")
        self.processor.submit_application(400, "Статья1", 1, "file1.pdf")
        self.processor.submit_application(401, "Статья2", 2, "file2.docx")
        stats = self.processor.get_statistics()
        self.assertEqual(stats["total_applications"], 2)
        self.assertEqual(stats["total_participants"], 2)
    
    def test_history_after_actions(self):
        self.processor.register_participant(1, "Тест", "test@test.com")
        self.processor.submit_application(500, "История", 1, "history.pdf")
        self.assertGreaterEqual(len(self.processor.history), 2)
    
    # Негативные тесты (варианты отказа)
    def test_register_participant_invalid_email(self):
        result = self.processor.register_participant(1, "Иван", "invalid-email")
        self.assertFalse(result["success"])
        self.assertIn("email", result["error"].lower())
    
    def test_register_participant_duplicate_id(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        result = self.processor.register_participant(1, "Петр", "petr@test.com")
        self.assertFalse(result["success"])
        self.assertIn("уже существует", result["error"])
    
    def test_submit_application_empty_title(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        result = self.processor.submit_application(101, "", 1, "file.pdf")
        self.assertFalse(result["success"])
        self.assertIn("пустым", result["error"])
    
    def test_submit_application_participant_not_found(self):
        result = self.processor.submit_application(101, "Статья", 999, "file.pdf")
        self.assertFalse(result["success"])
        self.assertIn("не найден", result["error"])
    
    def test_submit_application_invalid_file_extension(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        result = self.processor.submit_application(101, "Статья", 1, "image.png")
        self.assertFalse(result["success"])
        self.assertIn("тип файла", result["error"])
    
    def test_submit_application_empty_file_path(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        result = self.processor.submit_application(101, "Статья", 1, "")
        self.assertFalse(result["success"])
        self.assertIn("не указан", result["error"])
    
    def test_submit_application_duplicate_id(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        self.processor.submit_application(101, "Первая статья", 1, "file1.pdf")
        result = self.processor.submit_application(101, "Вторая статья", 1, "file2.pdf")
        self.assertFalse(result["success"])
        self.assertIn("уже существует", result["error"])
    
    def test_update_status_invalid_status(self):
        self.processor.register_participant(1, "Иван", "ivan@test.com")
        self.processor.submit_application(101, "Статья", 1, "file.pdf")
        result = self.processor.update_status(101, "invalid_status")
        self.assertFalse(result["success"])
        self.assertIn("Недопустимый статус", result["error"])
    
    def test_update_status_application_not_found(self):
        result = self.processor.update_status(999, "approved")
        self.assertFalse(result["success"])
        self.assertIn("не найдена", result["error"])
    
    def test_get_status_application_not_found(self):
        result = self.processor.get_application_status(999)
        self.assertFalse(result["success"])
        self.assertIn("не найдена", result["error"])


if __name__ == '__main__':
    unittest.main()