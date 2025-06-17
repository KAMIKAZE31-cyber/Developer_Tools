import json
import os
from datetime import datetime
from typing import List, Dict, Any

class HistoryManager:
    def __init__(self, history_file: str = "history.json"):
        self.history_file = history_file
        self._ensure_history_file_exists()

    def _ensure_history_file_exists(self):
        """Создает файл истории, если он не существует"""
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add_entry(self, action: str, details: Dict[str, Any] = None) -> None:
        """Добавляет новую запись в историю"""
        with open(self.history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details or {}
        }
        
        history.append(entry)

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def get_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """Получает историю действий"""
        with open(self.history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        if limit:
            return history[-limit:]
        return history

    def clear_history(self) -> None:
        """Очищает всю историю"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

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