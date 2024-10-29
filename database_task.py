import pyodbc

# Строка подключения к SQL Server в Docker
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"           # Подключение к локальному контейнеру Docker
    "DATABASE=master;"                 # Сначала подключаемся к master для создания БД
    "UID=SA;"
    "PWD=MoisseyPupkin!123;"
)

try:
    # Подключаемся к SQL Server
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    print("Подключение успешно.")
except Exception as e:
    print("Ошибка подключения:", e)

# 1. Запрос на создание БД
connection.autocommit = True  # Отключаем транзакции для создания базы данных
try:
    cursor.execute("CREATE DATABASE FitnessClubDB")
    print("База данных создана.")
except Exception as e:
    print("Ошибка при создании базы данных:", e)
finally:
    connection.autocommit = False  # Включаем обратно для других операций

# Подключаемся к новой базе данных
connection_string_db = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=FitnessClubDB;"
    "UID=SA;"
    "PWD=Printer1999klass2;"
)

try:
    connection = pyodbc.connect(connection_string_db)
    cursor = connection.cursor()
    print("Подключение к FitnessClubDB успешно.")
except Exception as e:
    print("Ошибка подключения к FitnessClubDB:", e)

# 2. Запрос на создание таблицы
try:
    cursor.execute("""
    CREATE TABLE Instructors (
        ID INT PRIMARY KEY IDENTITY(1,1),
        FirstName NVARCHAR(50),
        LastName NVARCHAR(50),
        SectionID INT
    );
    """)
    print("Таблица Instructors создана.")
except Exception as e:
    print("Ошибка при создании таблицы Instructors:", e)

# 3. Запрос на заполнение таблицы данными
try:
    cursor.execute("INSERT INTO Instructors (FirstName, LastName, SectionID) VALUES (?, ?, ?)",
                   'Алексей', 'Иванов', 1)
    cursor.execute("INSERT INTO Instructors (FirstName, LastName, SectionID) VALUES (?, ?, ?)",
                   'Мария', 'Петрова', 2)
    cursor.execute("INSERT INTO Instructors (FirstName, LastName, SectionID) VALUES (?, ?, ?)",
                   'Ольга', 'Сидорова', 3)
    connection.commit()  # Применяем изменения
    print("Таблица Instructors заполнена данными.")
except Exception as e:
    print("Ошибка при заполнении таблицы данными:", e)

# 4. Запрос на вывод данных из БД
try:
    cursor.execute("SELECT * FROM Instructors")
    rows = cursor.fetchall()

    # Упаковываем данные в список словарей
    data = [{"ID": row[0], "FirstName": row[1], "LastName": row[2], "SectionID": row[3]} for row in rows]
    print("Данные из таблицы Instructors:")
    for record in data:
        print(record)
except Exception as e:
    print("Ошибка при выводе данных:", e)

# Закрываем подключение
finally:
    cursor.close()
    connection.close()
    print("Подключение закрыто.")
