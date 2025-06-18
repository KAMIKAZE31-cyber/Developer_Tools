import json
import os
from datetime import datetime
from typing import List, Dict, Any
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class HistoryManager:
    def __init__(self, history_file: str = "history.json"):
        # Получаем абсолютный путь к директории проекта
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.history_file = os.path.join(base_dir, "history_files", history_file)
        logger.info(f"History file path: {self.history_file}")
        self._ensure_history_file_exists()

    def _ensure_history_file_exists(self):
        """Создает файл истории, если он не существует"""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            if not os.path.exists(self.history_file):
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                logger.info(f"Created new history file: {self.history_file}")
        except Exception as e:
            logger.error(f"Error creating history file: {e}")

    def add_entry(self, action: str, details: Dict[str, Any] = None) -> None:
        """Добавляет новую запись в историю"""
        try:
            logger.debug(f"Attempting to add entry: {action} with details: {details}")
            
            # Читаем текущую историю
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    try:
                        history = json.load(f)
                        logger.debug(f"Current history length: {len(history)}")
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in {self.history_file}, creating new history")
                        history = []
            else:
                history = []

            # Создаем новую запись
            entry = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'details': details or {}
            }
            
            # Добавляем запись
            history.append(entry)
            logger.debug(f"Added new entry. New history length: {len(history)}")

            # Записываем обновленную историю
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully wrote to {self.history_file}")
        except Exception as e:
            logger.error(f"Error adding entry to history: {e}", exc_info=True)

    def get_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """Получает историю действий"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    try:
                        history = json.load(f)
                        logger.debug(f"Read history with {len(history)} entries")
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in {self.history_file}")
                        history = []
            else:
                history = []
            
            if limit:
                return history[-limit:]
            return history
        except Exception as e:
            logger.error(f"Error reading history: {e}", exc_info=True)
            return []

    def clear_history(self) -> None:
        """Очищает всю историю"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            logger.info(f"Cleared history in {self.history_file}")
        except Exception as e:
            logger.error(f"Error clearing history: {e}", exc_info=True)

# Пример использования:
if __name__ == "__main__":
    # Создаем экземпляр менеджера истории
    history = HistoryManager()
    
    # Добавляем несколько записей
    history.add_entry("Пользователь вошел в систему", {"user_id": 123})
    history.add_entry("Файл был изменен", {"filename": "test.txt", "changes": 5})
    
    # Получаем последние 5 записей
    recent_history = history.get_history(limit=5)
    print("Последние действия:")
    for entry in recent_history:
        print(f"{entry['timestamp']}: {entry['action']}") 