"""
Модуль: assignment_of_experts.py
Программный модуль для назначения экспертов на статьи.
Поддерживает ввод и обработку целых чисел, строк, списков, дат.
Дата создания модуля: 25.03.2026
"""

from datetime import datetime
from typing import List, Dict, Optional


class Article:
    """
    Класс Статья
    """
    def __init__(self, article_id: int, title: str, author: str, content: str):
        self.id = article_id
        self.title = title
        self.author = author
        self.content = content
        self.status = "waiting"
        self.assigned_experts: List[int] = []
        self.created_at = datetime.now()
    
    def add_expert(self, expert_id: int) -> bool:
        """
        Добавить эксперта к статье
        """
        if expert_id not in self.assigned_experts:
            self.assigned_experts.append(expert_id)
            return True
        return False
    
    def change_status(self, new_status: str) -> None:
        """
        Изменить статус статьи
        """
        valid_statuses = ["waiting", "experts_assigned", "under_review", "accepted", "rejected"]
        if new_status in valid_statuses:
            self.status = new_status
    
    def __str__(self) -> str:
        return f"Статья #{self.id}: {self.title} (автор: {self.author}, статус: {self.status})"


class Expert:
    """
    Класс Эксперт
    """
    def __init__(self, expert_id: int, full_name: str, field: str, email: str):
        self.id = expert_id
        self.full_name = full_name
        self.field = field
        self.email = email
        self.assigned_articles: List[int] = []
    
    def assign_to_article(self, article_id: int) -> bool:
        """
        Назначить эксперта на статью
        """
        if article_id not in self.assigned_articles:
            self.assigned_articles.append(article_id)
            return True
        return False
    
    def __str__(self) -> str:
        return f"Эксперт #{self.id}: {self.full_name} ({self.field})"


class Moderator:
    """
    Класс Модератор
    """
    def __init__(self, user_id: int, username: str):
        self.id = user_id
        self.username = username
    
    def assign_experts_to_article(self, article: Article, expert_ids: List[int], 
                                   experts: Dict[int, Expert]) -> Dict[str, any]:
        """
        Назначить экспертов на статью -> Результат операции
        """
        result = {
            "success": True,
            "article_id": article.id,
            "assigned_experts": [],
            "errors": []
        }
        
        for expert_id in expert_ids:
            if expert_id in experts:
                expert = experts[expert_id]
                article.add_expert(expert_id)
                expert.assign_to_article(article.id)
                result["assigned_experts"].append(expert.full_name)
            else:
                result["errors"].append(f"Эксперт с ID {expert_id} не найден")
                result["success"] = False
        
        if result["success"] and len(result["assigned_experts"]) > 0:
            article.change_status("experts_assigned")
            result["message"] = f"Статье #{article.id} назначены эксперты: {', '.join(result['assigned_experts'])}"
        
        return result


class NotificationService:
    """
    Сервис уведомлений
    """
    @staticmethod
    def send_notification(expert: Expert, article_title: str) -> str:
        """
        Отправить уведомление эксперту
        """
        message = f"Уважаемый {expert.full_name}, вам назначена статья '{article_title}' для рецензирования."
        return f"[Уведомление] {expert.email}: {message}"