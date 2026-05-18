# Todo CLI - Утилита управления списком дел

## Команда разработки

| Участник   | Модуль        | Ответственность                             |
|------------|---------------|---------------------------------------------|
| Участник А | interface     | Парсинг CLI, вывод задач, цветные сообщения |
| Участник Б | file_handler  | Загрузка/сохранение JSON, бэкапы            |
| Участник В | logic         | CRUD-операции, фильтрация задач             |
| Участник Г | error_handler | Исключения, декоратор, валидация            |

## Установка и запуск

```bash
cd todo-cli
python todo_cli.py --help
```

Команды:

|Команда:	               | Пример:                                        |
|------------------------|------------------------------------------------|
| add	                   | python todo_cli.py add --title "Купить молоко" |
| list	                 | python todo_cli.py list                        |
| list --status done     | python todo_cli.py list --status done          |
| list --status pending  | python todo_cli.py list --status pending       |
| done --id	             | python todo_cli.py done --id 1                 |
| delete --id            | python todo_cli.py delete --id 1               |
| clear                  | python todo_cli.py clear                       |


Тестирование:

```bash
python test_todo.py
```

Git-ветки:


```bash
git checkout -b feature/interface
git checkout -b feature/file-handler
git checkout -b feature/logic
git checkout -b feature/error-handler
```


Pull Request процесс:


1.Создать ветку

2.Разработать модуль

3.Создать Pull Request в main

4.Пройти code review

5.Слить изменения
