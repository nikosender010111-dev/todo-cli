"""Модуль тестирования для Todo CLI."""

import unittest
import os
import json
from todo_cli import (
    add_task, mark_done, delete_task, clear_all, filter_tasks,
    validate_task_id, save_tasks, load_tasks, backup_tasks,
    TaskNotFoundError
)


class TestTodoApp(unittest.TestCase):
    """Тестовый класс для проверки функциональности."""
    
    def setUp(self):
        self.test_filename = "test_tasks_temp.json"
    
    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        for file in os.listdir("."):
            if file.startswith("test_tasks_temp.json.backup_"):
                os.remove(file)
    
    def test_add_task(self):
        tasks = []
        tasks = add_task(tasks, "New Task", "Description")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "New Task")
        self.assertEqual(tasks[0]["id"], 1)
    
    def test_mark_done(self):
        tasks = [{"id": 1, "title": "Test", "done": False}]
        tasks, success = mark_done(tasks, 1)
        self.assertTrue(success)
        self.assertTrue(tasks[0]["done"])
    
    def test_mark_done_not_found(self):
        tasks = [{"id": 1, "title": "Test", "done": False}]
        tasks, success = mark_done(tasks, 999)
        self.assertFalse(success)
    
    def test_delete_task(self):
        tasks = [{"id": 1, "title": "Test", "done": False}]
        tasks, success = delete_task(tasks, 1)
        self.assertTrue(success)
        self.assertEqual(len(tasks), 0)
    
    def test_filter_pending_tasks(self):
        tasks = [
            {"id": 1, "done": False},
            {"id": 2, "done": True},
            {"id": 3, "done": False}
        ]
        result = filter_tasks(tasks, "pending")
        self.assertEqual(len(result), 2)
    
    def test_filter_done_tasks(self):
        tasks = [
            {"id": 1, "done": False},
            {"id": 2, "done": True},
            {"id": 3, "done": False}
        ]
        result = filter_tasks(tasks, "done")
        self.assertEqual(len(result), 1)
    
    def test_validate_task_id(self):
        tasks = [{"id": 1, "title": "Test"}]
        self.assertTrue(validate_task_id(tasks, 1))
    
    def test_validate_task_id_not_found(self):
        tasks = [{"id": 1, "title": "Test"}]
        with self.assertRaises(TaskNotFoundError):
            validate_task_id(tasks, 999)
    
    def test_save_and_load_tasks(self):
        tasks = [{"id": 1, "title": "Test", "done": False}]
        save_tasks(tasks, self.test_filename)
        loaded = load_tasks(self.test_filename)
        self.assertEqual(loaded, tasks)
    
    def test_clear_all(self):
        tasks = [{"id": 1}, {"id": 2}, {"id": 3}]
        result = clear_all(tasks)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()




ДОКУМЕНТАЦИЯ:


#Todo CLI — Менеджер задач из консоли

##Команда проекта

| Участник | Модуль | Функции |
|----------|--------|---------|
| Участник А | interface.py | Парсинг аргументов, вывод задач, цветные сообщения |
| Участник Б | file_handler.py | Загрузка/сохранение JSON, бэкапирование |
| Участник В | logic.py | CRUD-операции, фильтрация задач |
| Участник Г | error_handler.py | Исключения, декоратор, валидация |

##Установка и запуск

```bash

# Скачать файл

curl -O https://your-server/todo_cli.py

# Запуск

python todo_cli.py --help


Git-ветки:


git checkout -b feature/interface
git checkout -b feature/file-handler
git checkout -b feature/logic
git checkout -b feature/error-handler