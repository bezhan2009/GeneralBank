class User:
    def __init__(self, username, last_name, password, age):
        self.username = username
        self.last_name = last_name
        self.password = password
        self.age = age

    def display_info(self):
        print(f"Username: {self.username}")
        print(f"Last Name: {self.last_name}")
        print(f"Age: {self.age}")

    def is_adult(self):
        return self.age >= 18


# Создаем объект класса User
test_user = User("bezhan", "karimov", "bezhan2009", 14)


def init(conn):
    try:
        cursor = conn.cursor()

        # Создание таблиц
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people(
                id SERIAL PRIMARY KEY,
                user_name VARCHAR(50) UNIQUE,
                last_name VARCHAR(50) NOT NULL,
                password VARCHAR(50) NOT NULL,
                age INT NOT NULL,
                UNIQUE (id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Accounts_users(
                id SERIAL,
                user_id INT NOT NULL,
                user_name_id VARCHAR(40),
                account_number VARCHAR(70),
                is_deleted BOOLEAN DEFAULT false,
                balance INT DEFAULT 10000,
                FOREIGN KEY (user_id) REFERENCES people (id)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Transactions_users(
                id SERIAL,
                user_id_1 INT NOT NULL,
                account_number_1 VARCHAR(70),
                account_number_2 VARCHAR(70),
                sum_transfer INT NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Logined_users(
                id SERIAL,
                login_user_p VARCHAR(40)
            );
        """)

        conn.commit()

        # Проверка и добавление данных
        cursor.execute("SELECT * FROM Accounts_users")
        view_for_bugs = cursor.fetchall()
        cursor.execute("SELECT * FROM people")
        view_for_bugs_2 = cursor.fetchall()

        if not view_for_bugs and not view_for_bugs_2:
            cursor.execute(
                "INSERT INTO people(user_name, last_name, password, age) VALUES (%s, %s, %s, %s)",
                (test_user.username, test_user.last_name, test_user.password, test_user.age)
            )
            cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
            conn.commit()

        elif not view_for_bugs:
            cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
            conn.commit()

        elif not view_for_bugs_2:
            cursor.execute(
                "INSERT INTO people(user_name, last_name, password, age) VALUES (%s, %s, %s, %s)",
                (test_user.username, test_user.last_name, test_user.password, test_user.age)
            )
            conn.commit()

    except Exception as e:
        print("Error occurred:", e)


def create_test_user(conn):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO people(user_name, last_name, password, age) VALUES (%s, %s, %s, %s)",
        (test_user.username, test_user.last_name, test_user.password, test_user.age)
    )
    conn.commit()
