class Participant:
    """Класс участника конференции"""
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    
    def __repr__(self):
        return f"Participant(id={self.id}, name='{self.name}', email='{self.email}')"


class Application:
    """Класс заявки на участие"""
    def __init__(self, id, title, participant_id, file_path, status="pending"):
        self.id = id
        self.title = title
        self.participant_id = participant_id
        self.file_path = file_path
        self.status = status  # pending, approved, rejected
    
    def __repr__(self):
        return f"Application(id={self.id}, title='{self.title}', status='{self.status}')"


class ApplicationProcessor:
    """
    Модуль для обработки заявок на участие в конференции.
    Поддерживает создание заявок, валидацию данных, сохранение и уведомления.
    """
    
    def __init__(self):
        self.applications = []  # список всех заявок
        self.participants = []  # список участников
        self.history = []       # история действий
    
    def register_participant(self, id, name, email):
        """Регистрация нового участника"""
        # Валидация email
        if not self._validate_email(email):
            return {"success": False, "error": "Неверный формат email"}
        
        # Проверка на дубликат ID
        if any(p.id == id for p in self.participants):
            return {"success": False, "error": f"Участник с ID {id} уже существует"}
        
        participant = Participant(id, name, email)
        self.participants.append(participant)
        self.history.append(f"Зарегистрирован участник: {name}")
        return {"success": True, "participant": participant}
    
    def submit_application(self, id, title, participant_id, file_path):
        """Подача новой заявки"""
        # Проверка обязательных полей
        if not title or not title.strip():
            return {"success": False, "error": "Название статьи не может быть пустым"}
        
        # Проверка существования участника
        participant = self._find_participant(participant_id)
        if not participant:
            return {"success": False, "error": f"Участник с ID {participant_id} не найден"}
        
        # Проверка файла
        file_check = self._validate_file(file_path)
        if not file_check["success"]:
            return {"success": False, "error": file_check["error"]}
        
        # Проверка дубликата заявки по ID
        if any(a.id == id for a in self.applications):
            return {"success": False, "error": f"Заявка с ID {id} уже существует"}
        
        application = Application(id, title.strip(), participant_id, file_path)
        self.applications.append(application)
        self.history.append(f"Подана заявка: {title} (участник: {participant.name})")
        
        # Отправка уведомления (имитация)
        self._send_notification(participant.email, application)
        
        return {"success": True, "application": application}
    
    def get_application_status(self, application_id):
        """Получение статуса заявки"""
        application = self._find_application(application_id)
        if not application:
            return {"success": False, "error": f"Заявка с ID {application_id} не найдена"}
        return {"success": True, "status": application.status}
    
    def update_status(self, application_id, new_status):
        """Обновление статуса заявки (для модератора)"""
        valid_statuses = ["pending", "approved", "rejected"]
        if new_status not in valid_statuses:
            return {"success": False, "error": f"Недопустимый статус. Допустимые: {valid_statuses}"}
        
        application = self._find_application(application_id)
        if not application:
            return {"success": False, "error": f"Заявка с ID {application_id} не найдена"}
        
        old_status = application.status
        application.status = new_status
        self.history.append(f"Статус заявки '{application.title}' изменён: {old_status} -> {new_status}")
        return {"success": True, "application": application}
    
    def get_statistics(self):
        """Получение статистики по заявкам"""
        total = len(self.applications)
        pending = sum(1 for a in self.applications if a.status == "pending")
        approved = sum(1 for a in self.applications if a.status == "approved")
        rejected = sum(1 for a in self.applications if a.status == "rejected")
        
        return {
            "total_applications": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "total_participants": len(self.participants),
            "history_count": len(self.history)
        }
    
    # Вспомогательные приватные методы
    def _validate_email(self, email):
        """Проверка формата email"""
        if not email:
            return False
        return "@" in email and "." in email.split("@")[-1]
    
    def _validate_file(self, file_path):
        """Проверка файла статьи"""
        if not file_path:
            return {"success": False, "error": "Путь к файлу не указан"}
        
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_ext = file_path.lower()[file_path.rfind('.'):] if '.' in file_path else ''
        
        if file_ext not in allowed_extensions:
            return {"success": False, "error": f"Недопустимый тип файла. Разрешены: {allowed_extensions}"}
        
        return {"success": True}
    
    def _find_participant(self, participant_id):
        """Поиск участника по ID"""
        for p in self.participants:
            if p.id == participant_id:
                return p
        return None
    
    def _find_application(self, application_id):
        """Поиск заявки по ID"""
        for a in self.applications:
            if a.id == application_id:
                return a
        return None
    
    def _send_notification(self, email, application):
        """Имитация отправки уведомления на email"""
        self.history.append(f"Уведомление отправлено на {email}: заявка '{application.title}' получена")


# Пример использования
if __name__ == "__main__":
    processor = ApplicationProcessor()
    
    # Регистрация участника
    result = processor.register_participant(1, "Иван Петров", "ivan@example.com")
    print("Регистрация:", result)
    
    # Подача заявки
    result = processor.submit_application(101, "AI в образовании", 1, "article.pdf")
    print("Подача заявки:", result)
    
    # Проверка статуса
    result = processor.get_application_status(101)
    print("Статус:", result)
    
    # Статистика
    print("\nСтатистика:", processor.get_statistics())