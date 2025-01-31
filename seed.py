import sqlite3

conn = sqlite3.connect("teachers.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    group_name TEXT NOT NULL
)
"""
)

groups = [
    "Группа 1",
    "Группа 2",
    "Группа 3",
    "Группа 4",
    "Группа 5",
    "Группа 6",
    "Группа 7",
    "Группа 8",
    "Группа 9",
    "Группа 10",
]

for group in groups:
    cursor.execute("INSERT INTO Groups (name) VALUES (?)", (group,))

teachers = [
    ("Иван Петров", "Математика", "Группа 1"),
    ("Сергей Иванов", "Физика", "Группа 2"),
    ("Андрей Смирнов", "Химия", "Группа 3"),
    ("Николай Кузнецов", "Биология", "Группа 4"),
    ("Дмитрий Попов", "История", "Группа 5"),
    ("Алексей Васильев", "География", "Группа 6"),
    ("Владимир Михайлов", "Литература", "Группа 7"),
    ("Юрий Новиков", "Русский язык", "Группа 8"),
    ("Павел Сидоров", "Английский язык", "Группа 9"),
    ("Константин Орлов", "Физическая культура", "Группа 10"),
    ("Елена Александрова", "Математика", "Группа 1"),
    ("Марина Дмитриева", "Физика", "Группа 2"),
    ("Татьяна Крылова", "Химия", "Группа 3"),
    ("Светлана Григорьева", "Биология", "Группа 4"),
    ("Анна Петрова", "История", "Группа 5"),
    ("Ольга Белова", "География", "Группа 6"),
    ("Наталья Яковлева", "Литература", "Группа 7"),
    ("Марина Иванова", "Русский язык", "Группа 8"),
    ("Виктория Смирнова", "Английский язык", "Группа 9"),
    ("Ирина Попова", "Физическая культура", "Группа 10"),
    ("Евгений Федоров", "Математика", "Группа 1"),
    ("Михаил Морозов", "Физика", "Группа 2"),
    ("Александр Лебедев", "Химия", "Группа 3"),
    ("Виктор Козлов", "Биология", "Группа 4"),
    ("Геннадий Степанов", "История", "Группа 5"),
    ("Ирина Николаева", "География", "Группа 6"),
]

for teacher in teachers:
    cursor.execute(
        "INSERT INTO Teachers (name, subject, group_name) VALUES (?, ?, ?)",
        (teacher[0], teacher[1], teacher[2]),
    )

conn.commit()
conn.close()

print("Данные добавлены в базу данных.")
