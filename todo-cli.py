"""КЕЙС 2: CLI-утилита для управления списком дел
Разработка с разделением на модули для командной работы"""

"""Авторы: Участник А, Участник Б, Участник В, Участник Г
"""

import argparse
import json
import os
import sys
import traceback
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Callable


def parse_arguments(args: List[str]) -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Менеджер задач — CLI утилита для управления списком дел",
        epilog="Пример: python todo_cli.py add --title 'Купить молоко'"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Доступные команды")

    parser_add = subparsers.add_parser("add", help="Добавить новую задачу")
    parser_add.add_argument("--title", required=True, help="Название задачи")
    parser_add.add_argument("--description", default="", help="Описание задачи")

    parser_list = subparsers.add_parser("list", help="Показать все задачи")
    parser_list.add_argument("--status", choices=["done", "pending"], help="Фильтр по статусу")

    parser_done = subparsers.add_parser("done", help="Отметить задачу как выполненную")
    parser_done.add_argument("--id", type=int, required=True, help="ID задачи")

    parser_delete = subparsers.add_parser("delete", help="Удалить задачу")
    parser_delete.add_argument("--id", type=int, required=True, help="ID задачи")

    subparsers.add_parser("clear", help="Удалить все задачи")

    return parser.parse_args(args)


def display_tasks(tasks: List[dict]) -> None:
    """Отображает список задач в читаемом формате."""
    if not tasks:
        print("Список задач пуст.")
        return

    print("\nВаши задачи:")
    print("=" * 70)
    for task in tasks:
        status_icon = "✅" if task.get("done") else "⏳"
        status_text = "Выполнена" if task.get("done") else "В процессе"
        print(f"{status_icon} [{task['id']}] {task['title']} ({status_text})")
        if task.get("description"):
            print(f"Описание: {task['description']}")
        print(f"Создано: {task.get('created_at', 'неизвестно')}")
        print("-" * 70)


def show_message(msg: str, msg_type: str = "info") -> None:
    """Показывает сообщение пользователю с цветом."""
    colors = {
        "info": "\033[94m",
        "success": "\033[92m",
        "error": "\033[91m",
        "warning": "\033[93m"
    }
    reset = "\033[0m"
    color = colors.get(msg_type, colors["info"])
    print(f"{color}{msg}{reset}")



DEFAULT_FILENAME = "tasks.json"


def load_tasks(filename: str = DEFAULT_FILENAME) -> List[Dict]:
    """Загружает задачи из JSON-файла."""
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            if isinstance(tasks, list):
                return tasks
            return []
    except (json.JSONDecodeError, IOError) as e:
        raise IOError(f"Ошибка чтения файла {filename}: {e}")


def save_tasks(tasks: List[Dict], filename: str = DEFAULT_FILENAME) -> bool:
    """Сохраняет задачи в JSON-файл. Возвращает True при успехе."""
    try:
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        raise IOError(f"Ошибка записи файла {filename}: {e}")


def backup_tasks(filename: str = DEFAULT_FILENAME) -> str:
    """Создаёт бэкап файла с задачами."""
    if not os.path.exists(filename):
        return ""

    backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(filename, backup_name)
    return backup_name



def add_task(tasks: List[Dict], title: str, description: str = "") -> List[Dict]:
    """Добавляет новую задачу. Возвращает обновлённый список."""
    new_id = max([t["id"] for t in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": title,
        "description": description,
        "done": False,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(new_task)
    return tasks


def mark_done(tasks: List[Dict], task_id: int) -> tuple[List[Dict], bool]:
    """
    Отмечает задачу как выполненную.
    Возвращает (обновлённый список, успех_операции).
    """
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                return tasks, False
            task["done"] = True
            return tasks, True
    return tasks, False

def delete_task(tasks: List[Dict], task_id: int) -> tuple[List[Dict], bool]:
    """Удаляет задачу по ID."""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return tasks, True
    return tasks, False


def clear_all(tasks: List[Dict]) -> List[Dict]:
    """Удаляет все задачи."""
    return []


def filter_tasks(tasks: List[Dict], status: Optional[str] = None) -> List[Dict]:
    """Фильтрует задачи по статусу(done / pending)."""
    if status is None:
        return tasks

    if status == "done":
        return [t for t in tasks if t.get("done", False)]
    elif status == "pending":
        return [t for t in tasks if not t.get("done", False)]
    return tasks



class TodoAppError(Exception):
    """ Базовое исключение приложения."""
    pass


class TaskNotFoundError(TodoAppError):
    """Задача не найдена."""
    pass


class InvalidCommandError(TodoAppError):
    """Неверная команда."""
    pass


class FileOperationError(TodoAppError):
    """Ошибка при работе с файлом."""
    pass


def handle_errors(func: Callable) -> Callable:
    """Декоратор для перехвата и обработки ошибок."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskNotFoundError as e:
            show_message(f"Ошибка: {e}", "error")
            show_message("Совет: проверьте ID задачи с помощью команды 'list'", "info")
            return None
        except FileOperationError as e:
            show_message(f"Файловая ошибка: {e}", "error")
            show_message("Совет: проверьте права доступа к файлу", "info")
            return None
        except InvalidCommandError as e:
            show_message(f"Ошибка команды: {e}", "error")
            show_message("Используйте --help для справки", "info")
            return None
        except Exception as e:
            show_message(f"Непредвиденная ошибка: {e}", "error")
            if "--debug" in sys.argv:
                traceback.print_exc()
            else:
                show_message("Запустите с флагом --debug для деталей", "info")
            return None
    return wrapper


def validate_task_id(tasks: list, task_id: int) -> bool:
    """Проверяет существование задачи с таким ID."""
    if not any(t["id"] == task_id for t in tasks):
        raise TaskNotFoundError(f"Задача с ID={task_id} не найдена")
    return True


@handle_errors
def main():
    """Главная функция приложения."""
    args = parse_arguments(sys.argv[1:])

    tasks = load_tasks()

    if args.command == "add":
        add_task(tasks, args.title, args.description)
        save_tasks(tasks)
        show_message(f"Задача '{args.title}' добавлена!", "success")

    elif args.command == "list":
        filtered = filter_tasks(tasks, getattr(args, 'status', None))
        display_tasks(filtered)

    elif args.command == "done":
        validate_task_id(tasks, args.id)
        tasks, success = mark_done(tasks, args.id)
        if success:
            save_tasks(tasks)
            show_message(f" Задача {args.id} отмечена как выполненная!", "success")
        else:
            show_message(f"⚠ Задача {args.id} уже была выполнена", "warning")

    elif args.command == "delete":
        validate_task_id(tasks, args.id)
        tasks, _ = delete_task(tasks, args.id)
        save_tasks(tasks)
        show_message(f" Задача {args.id} удалена", "success")

    elif args.command == "clear":
        backup_tasks()
        tasks = clear_all(tasks)
        save_tasks(tasks)
        show_message(" Все задачи удалены (бэкап создан)", "warning")


if __name__ == "__main__":
    main()