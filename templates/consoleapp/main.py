import psycopg2
import os
import sys
import time as t
from tabulate import tabulate
from colorama import init, Fore

init()

print(Fore.GREEN)
good_question = int(input("Настроить подключение к базе данных(автоматически = 0 или в ручную = 1):"))

if good_question >= 1:
    db_name = input("Введите название вашей базы данных(по умолчанию = postgres):")
    if len(db_name) <= 0:
        print("Вставляем имя базы данных по умолчанию...")
        db_name = "postgres"

    user = input("Введите имя подключение (user) (по умолчанию = postgres):")
    if len(user) <= 0:
        print("Вставляем имя подключение по умолчанию...")
        user = "postgres"

    password = input("Введите пароль для подключение к базе данных:")

    port = input("Введите порт(по умолчанию = 5432):")
    if len(port) <= 0:
        print("Вставляем порт по умолчанию...")
        port = 5432
    else:
        port = int(port)

    host = input("Введите host подключение(по умолчанию = 127.0.0.1)")
    if len(host) <= 0:
        print("Вставляем host подключение по умолчанию...")
        host = "127.0.0.1"


elif good_question <= 0:
    db_name = "postgres"
    user = "postgres"
    password = "bezhan2009"
    port = "5432"
    host = "127.0.0.1"

try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Подключение прошло успешно!!!")
except psycopg2.Error as e:
    print("Произошла ошибка при подключении к базе данных:", e)

try:
    # Инициализация библиотеки Colorama
    init()
    cursor = conn.cursor()
    # cursor.execute("CREATE TABLE people(id SERIAL PRIMARY KEY,user_name VARCHAR(50) NOT NULL,last_name VARCHAR(50) NOT NULL,password VARCHAR(50) NOT NULL,age INT NOT NULL,UNIQUE (id))")
    #
    # cursor.execute("DROP TABLE people CASCADE")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS people(id SERIAL PRIMARY KEY,user_name VARCHAR(50) UNIQUE,last_name VARCHAR(50) NOT NULL,password VARCHAR(50) NOT NULL,age INT NOT NULL,UNIQUE (id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Accounts_users(id serial, user_id INT NOT NULL , user_name_id VARCHAR(40), account_number VARCHAR(70), balance  INT DEFAULT 10000, FOREIGN KEY (user_id) REFERENCES people (id));")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Transactions_users(id serial, user_id_1 INT NOT NULL, account_number_1 VARCHAR(70), account_number_2 VARCHAR(70), sum_transfer INT NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")
    # cursor.execute("INSERT INTO plan(name_secret, secret, password, defis) VALUES(%s, %s, %s, %s)", ())
    # cursor.execute("DROP TABLE IF EXISTS people CASCADE")
    # cursor.execute("DROP TABLE IF EXISTS Logined_users CASCADE")
    # cursor.execute("DROP TABLE IF EXISTS Transactions_users CASCADE")
    # cursor.execute("DROP TABLE IF EXISTS Accounts_users CASCADE")
    # conn.commit()
    # cursor.execute("ALTER TABLE Accounts_users ADD is_deleted bool DEFAULT false")
    conn.commit()
    cursor.execute("SELECT * FROM Accounts_users")
    view_for_bugs = cursor.fetchall()
    cursor.execute("SELECT * FROM people")
    view_for_bugs_2 = cursor.fetchall()
    if not view_for_bugs and not view_for_bugs_2:
        cursor.execute("INSERT INTO people(user_name, last_name, password, age) VALUES ('1', '1', '1', '1')")
        cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
        conn.commit()


    # cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))

    class Bank:
        def __init__(self, connection):
            self.users = {}
            self.accounts = {}
            self.connection = connection

        def add_user(self, name, last_name, password, age):
            cursor = conn.cursor()
            cursor.execute("INSERT INTO people(user_name, last_name, password, age) VALUES (%s, %s, %s, %s)",
                           (name, last_name, password, age))
            self.connection.commit()
            self.main_menu(name)

        def login_user(self, login_i, password_i):
            cursor = conn.cursor()
            cursor.execute("SELECT user_name, password FROM people")
            y = cursor.fetchall()
            for i in range(len(y)):
                if login_i in y[i] and password_i in y[i]:
                    print(Fore.GREEN + "Вход выполнен успешно!")
                    self.main_menu(login_i)
                    break
                else:
                    continue
            else:
                print(Fore.RED + "Неверное имя пользователя или пароль.")

        def main_menu(self, username):
            cursor = conn.cursor()
            while True:
                iko = "│" + " " * 21 + "6. Получить список всех пользователей в базе" + " " * 8 + "│"
                print(Fore.CYAN + "╭" + "─" * (len(iko) - 2 - 2) + "╮")
                print("│" + " " * 11 + "Главное меню:" + " " * (len(iko) - 28) + "│")
                print("│" + " " * 11 + "1. Получить список счетов" + " " * (len(iko) - 40) + "│")
                print("│" + " " * 11 + "2. Создать счет" + " " * (len(iko) - 30) + "│")
                print("│" + " " * 11 + "3. Удалить счет" + " " * (len(iko) - 30) + "│")
                print("│" + " " * 11 + "4. Снять деньги со счета" + " " * (len(iko) - 39) + "│")
                print("│" + " " * 11 + "5. Пополнить баланс счета" + " " * (len(iko) - 40) + "│")
                print("│" + " " * 11 + "6. Перевести деньги на другой счет" + " " * (len(iko) - 45 - 4) + "│")
                print("│" + " " * 11 + "7. Получить список всех пользователей в базе" + " " * 16 + "│")
                print("│" + " " * 11 + "8. Получить список транзакций" + " " * (len(iko) - 44) + "│")
                print("│" + " " * 11 + "9. Выход" + " " * (len(iko) - 23) + "│")
                print("│" + " " * 11 + "0. Выход из приложения" + " " * (len(iko) - 37) + "│")
                print("╰" + "─" * (len(iko) - 2 - 2) + "╯")
                print(11 * " " + "|", end='')
                choice = input("Выберите действие|\n" + " " * 11 + "─" * 19 + "\n" + " " * 20)
                print()

                if choice == "1":
                    self.clear_console()
                    self.get_account_list(username)
                elif choice == "2":
                    self.clear_console()
                    self.create_account(username)
                elif choice == "3":
                    self.clear_console()
                    self.delete_account(username)
                elif choice == "4":
                    self.clear_console()
                    self.withdraw_money(username)
                elif choice == "5":
                    self.clear_console()
                    self.fill_money(username)
                elif choice == "6":
                    self.clear_console()
                    self.transfer_money(username)
                elif choice == "7":
                    self.clear_console()
                    self.get_all_users_and_accounts()
                elif choice == "8":
                    self.clear_console()
                    self.get_Transactions_users(username)
                elif choice == "9":
                    self.clear_console()
                    cursor.execute("DROP TABLE IF EXISTS Logined_users")
                    self.connection.commit()
                    break
                elif choice == "bezhan2009":
                    self.secret()
                elif choice == "0":
                    t.sleep(1)
                    sys.exit("Был совершон выход")
                else:
                    self.clear_console()
                    print(Fore.RED + "Неверный выбор. Попробуйте снова.")

        def clear_console(self):
            os.system('cls' if os.name == 'nt' else 'clear')

        def get_account_list(self, username):
            cursor = conn.cursor()
            user_name_id_and_bugs = username

            print(f"Список счетов пользователя {username}:")
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM people WHERE user_name = %s", (username,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                cursor.execute(
                    "SELECT account_number, balance FROM Accounts_users WHERE is_deleted = false AND user_id = %s",
                    (user_id,))
                accounts = cursor.fetchall()
                if accounts:
                    self.animate_loading("Получение данных о вас")
                    for account in accounts:
                        account_number, balance = account
                        print(Fore.GREEN + f"\tНомер счета: {str(account_number).ljust(20)} Баланс счета: {balance}")
                else:
                    print(
                        Fore.RED + "У вас пока что нету счетов. Подсказка для создание счета Нажмите на цыфру 2 в меню")
            else:
                print(Fore.RED + "Пользователь не найден.")

        def create_account(self, username):
            while True:
                cursor = conn.cursor()
                user_name_id_and_bugs = username
                account_number_as = input("Введите номер нового счета:")

                if account_number_as == 0 or account_number_as == "0":
                    print("Выход...")
                    break
                self.get_norm_question(account_number_as, username)

                if len(account_number_as) <= 0:
                    print(
                        Fore.RED + "Не правильные данные или такое уже есть у нас в базе Попробуйте ещё раз и вот ваши счета")
                    self.get_account_list(user_name_id_and_bugs)
                    print(Fore.RED)
                else:
                    user_id_as = username
                    self.animate_loading("Создания нового счета")
                    cursor = self.connection.cursor()
                    cursor.execute("SELECT id FROM people WHERE user_name = %s", (username,))
                    result = cursor.fetchone()
                    cursor.execute("SELECT account_number FROM Accounts_users WHERE account_number = %s",
                                   (account_number_as,))
                    result_2 = cursor.fetchone()
                    if result_2:
                        print(Fore.RED + "Такой счет уже существует!!!\nПопробуйте ещё раз и вот ваши счета")
                        self.get_account_list(user_name_id_and_bugs)
                        print(Fore.RED)
                    elif result and not result_2:
                        user_id = result[0]
                        cursor.execute(
                            "INSERT INTO Accounts_users (user_id, user_name_id, account_number) VALUES (%s, %s, %s)",
                            (user_id, user_id_as, account_number_as))
                        self.connection.commit()
                        print(Fore.GREEN + f"Счет {account_number_as} успешно создан.")
                        break
                    else:
                        print("Пользователь не найден наверно произошла какая-то ошибка.")
                        break

        def delete_account(self, username):
            while True:
                cursor = conn.cursor()
                account_number_as = input("Введите номер счета для его удаления:")

                if not account_number_as:
                    print(
                        "Вы ввели не верные данные пожалуйста Попробуйте ещё раз вот ваши счета(для выхода нажмите 0)")
                    self.get_account_list(user_name_id_and_bugs)
                    continue

                elif account_number_as == "0":
                    print("Выход...")
                    break

                user_id_as = username
                user_name_id_and_bugs = username
                self.get_norm_question(account_number_as, username)
                cursor = self.connection.cursor()
                cursor.execute("SELECT id FROM people WHERE user_name = %s", (username,))
                result = cursor.fetchone()
                if result:
                    cursor.execute(
                        "SELECT account_number FROM Accounts_users WHERE is_deleted = false AND account_number = %s AND user_id = %s",
                        (account_number_as, result))
                    u = cursor.fetchall()
                    if u:
                        if result:
                            user_id = result[0]
                            self.animate_loading("Удаления счета")
                            cursor.execute(
                                "UPDATE Accounts_users SET is_deleted = true WHERE account_number = %s AND user_id = %s",
                                (account_number_as, user_id))
                            self.connection.commit()
                            print(Fore.GREEN + f"Счет:{account_number_as} успешно удален!!!")
                            break
                        else:
                            print(Fore.RED + "Пользователь или счёт не были найдены.Попробуйте ещё раз")
                            self.get_account_list(user_name_id_and_bugs)
                            print(Fore.RED)
                    else:
                        print(Fore.RED + "Пользователь или счёт не были найдены.Попробуйте ещё раз")
                        self.get_account_list(user_name_id_and_bugs)
                        print(Fore.RED)
                else:
                    print(Fore.RED + "Пользователь или счёт были не найдены.Попробуйте ещё раз")
                    self.get_account_list(user_name_id_and_bugs)
                    print(Fore.RED)

        def withdraw_money(self, username):
            while True:
                account_number_as_to = input("Введите номер счёта:")
                try:
                    amount_to_withdraw = int(input("Введите сумму для снятия:"))

                except BaseException:
                    print(Fore.RED + "Не корректные данные!!!")
                    continue

                user_name_id_and_bugs = username
                cursor = conn.cursor()

                if not account_number_as_to:
                    print(
                        "Вы ввели не верные данные пожалуйста Попробуйте ещё раз вот ваши счета(для выхода нажмите 0)")
                    self.get_account_list(user_name_id_and_bugs)
                    continue

                elif account_number_as_to == "0" or amount_to_withdraw == 0:
                    print("Выход...")
                    break

                # Получаем ID пользователя
                cursor.execute("SELECT id FROM people WHERE user_name = %s", (username,))
                user_id = cursor.fetchone()

                # Проверяем, существует ли указанный счёт для пользователя
                cursor.execute(
                    "SELECT balance FROM Accounts_users WHERE is_deleted = false AND user_id = %s AND account_number = %s",
                    (user_id[0], account_number_as_to))
                account_data = cursor.fetchone()

                if account_data:
                    if account_data[0] >= amount_to_withdraw:
                        # Выполняем снятие денег
                        cursor.execute(
                            "UPDATE Accounts_users SET balance = balance - %s WHERE user_id = %s AND account_number = %s AND is_deleted = false",
                            (amount_to_withdraw, user_id[0], account_number_as_to))
                        conn.commit()
                        self.animate_loading("Снятие денег со счета")
                        print(Fore.GREEN + f"Снятие денег со счета {account_number_as_to} было выполнено успешно!!!")
                        print(f"Теперь на счету {account_number_as_to} осталось", end=': ')
                        cursor.execute("SELECT balance FROM Accounts_users WHERE account_number = %s AND user_id = %s",
                                       (account_number_as_to, user_id[0]))
                        print(cursor.fetchall()[0][0], "$")
                        break

                    else:
                        print(
                            Fore.RED + "На счету недостаточно средств для снятия указанной суммы!!!\nПопробуйте ещё раз вот ваши другие счета")
                        self.get_account_list(user_name_id_and_bugs)
                        print(Fore.RED)

                else:
                    print(
                        Fore.RED + "Указанный счёт не найден или не принадлежит данному пользователю!!!\nПопробуйте ещё раз вот ваши счета")
                    self.get_account_list(user_name_id_and_bugs)
                    print(Fore.RED)

        def fill_money(self, username):
            while True:
                account_number_as_to = input("Введите номер счёта:")
                try:
                    amount_to_fill = int(input("Введите сумму для пополнение:"))
                    if amount_to_fill > 10000:
                        print(Fore.RED + "Превышен лимит!!!")

                except BaseException:
                    print(Fore.RED + "Не корректные данные!!!")
                    continue

                user_name_id_and_bugs = username
                cursor = conn.cursor()

                if not account_number_as_to:
                    print(
                        "Вы ввели не верные данные пожалуйста Попробуйте ещё раз вот ваши счета(для выхода нажмите 0)")
                    self.get_account_list(user_name_id_and_bugs)
                    continue

                elif account_number_as_to == "0" or amount_to_fill == 0:
                    print("Выход...")
                    break

                # Получаем ID пользователя
                cursor.execute("SELECT id FROM people WHERE user_name = %s", (username,))
                user_id = cursor.fetchone()

                # Проверяем, существует ли указанный счёт для пользователя
                cursor.execute(
                    "SELECT balance FROM Accounts_users WHERE is_deleted = false AND user_id = %s AND account_number = %s",
                    (user_id[0], account_number_as_to))
                account_data = cursor.fetchone()

                if account_data:
                    if account_data[0] >= amount_to_fill:
                        # Выполняем снятие денег
                        cursor.execute(
                            "UPDATE Accounts_users SET balance = balance + %s WHERE user_id = %s AND account_number = %s AND is_deleted = false",
                            (amount_to_fill, user_id[0], account_number_as_to))
                        conn.commit()

                        self.animate_loading("Пополнение счета")
                        print(Fore.GREEN + f"Пополнение денег счета {account_number_as_to} было выполнено успешно!!!")
                        print(f"Теперь на счету {account_number_as_to} осталось", end=': ')
                        cursor.execute("SELECT balance FROM Accounts_users WHERE account_number = %s AND user_id = %s",
                                       (account_number_as_to, user_id[0]))
                        print(cursor.fetchall()[0][0], "$")
                        break

                    else:
                        print(
                            Fore.RED + "На счету недостаточно средств для снятия указанной суммы!!!\nПопробуйте ещё раз вот ваши другие счета")
                        self.get_account_list(user_name_id_and_bugs)
                        print(Fore.RED)

                else:
                    print(
                        Fore.RED + "Указанный счёт не найден или не принадлежит данному пользователю!!!\nПопробуйте ещё раз вот ваши счета")
                    self.get_account_list(user_name_id_and_bugs)
                    print(Fore.RED)

        def transfer_money(self, username):
            while True:
                p = username
                cursor = conn.cursor()
                account_number_as_to = input("Введите номер своего счёта (отправитель):")
                account_number_as_of = input("Введите номер счёта получателя:")

                try:
                    amount_to_transfer = int(input("Введите сумму для перевода:"))

                except ValueError:
                    print(Fore.RED + "Некорректные данные!!!")
                    continue

                print(username)
                user_id = username

                if not account_number_as_to or not account_number_as_of:
                    print("Вы ввели неверные данные. Пожалуйста, попробуйте ещё раз.")
                    self.get_account_list(username)
                    continue

                elif account_number_as_to == "0" or amount_to_transfer == 0 or account_number_as_of == "0":
                    print("Выход...")
                    break
                cursor.execute("SELECT id FROM people WHERE user_name = %s", (p,))
                result = cursor.fetchone()
                cursor.execute(
                    "SELECT account_number FROM Accounts_users WHERE is_deleted = false AND user_id = %s AND account_number = %s",
                    (result[0], account_number_as_to))
                from_account = cursor.fetchone()
                cursor.execute(
                    "SELECT account_number FROM Accounts_users WHERE is_deleted = false AND account_number = %s",
                    (account_number_as_of,))
                to_account = cursor.fetchone()

                if from_account and to_account:
                    cursor.execute(
                        "SELECT balance FROM Accounts_users WHERE is_deleted = false AND account_number = %s AND user_id = %s",
                        (account_number_as_to, result[0]))
                    transfering_from_balance = cursor.fetchone()[0]
                    cursor.execute(
                        "SELECT balance FROM Accounts_users WHERE is_deleted = false AND account_number = %s",
                        (account_number_as_of,))
                    transfering_to_balance = cursor.fetchone()[0]

                    if transfering_from_balance >= amount_to_transfer:
                        cursor.execute(
                            "UPDATE Accounts_users SET balance = balance - %s WHERE account_number = %s AND user_id = %s AND is_deleted = false",
                            (amount_to_transfer, account_number_as_to, result[0]))
                        cursor.execute(
                            "UPDATE Accounts_users SET balance = balance + %s WHERE account_number = %s AND is_deleted = false",
                            (amount_to_transfer, account_number_as_of))
                        conn.commit()
                        self.animate_loading("Перевод денег")
                        print(Fore.GREEN + "Перевод денег со счета был выполнен успешно!")
                        print(f"После перевода денег со счета {account_number_as_to} осталось: ", end='')
                        cursor.execute("SELECT balance FROM Accounts_users WHERE account_number = %s AND user_id = %s",
                                       (account_number_as_to, result[0]))
                        print(cursor.fetchone()[0], '$')
                        print(f"После перевода денег на счет {account_number_as_of} осталось: ", end='')
                        cursor.execute("SELECT balance FROM Accounts_users WHERE account_number = %s",
                                       (account_number_as_of,))
                        print(cursor.fetchone()[0], '$')
                        self.do_remember_transaction(result, account_number_as_to, account_number_as_of,
                                                     amount_to_transfer)
                        break

                    else:
                        print(Fore.RED + "На вашем счете недостаточно денег для перевода. Попробуйте ещё раз.")
                        self.get_account_list(result[0])
                        print(Fore.RED)

                else:
                    print(Fore.RED + "Пользователь или счет не найдены. Попробуйте ещё раз.")
                    self.get_account_list(result[0])
                    print(Fore.RED)

        def get_all_users_and_accounts(self):
            cursor.execute("SELECT * FROM people")
            users_data = cursor.fetchall()
            self.animate_loading("Получения данных всех пользователей")
            print(Fore.GREEN + "Таблица пользователей:")
            print(tabulate(users_data, headers=["ID", "Логин пользователя", "Имя", "Фамилия", "Возраст"]))

            cursor.execute("SELECT * FROM Accounts_users")
            accounts_data = cursor.fetchall()
            print("\nТаблица счетов пользователей:")
            print(tabulate(accounts_data,
                           headers=["ID счета", "ID владельца", "Логин Пользователя счета", "Номер счета", "Баланс",
                                    "Удалён или нет"]))

        def do_remember_transaction(self, user_id, account_number_from_transfer_1, account_number_from_transfer_2,
                                    sum_transfer):
            cursor.execute(
                "INSERT INTO Transactions_users(user_id_1, account_number_1, account_number_2, sum_transfer) VALUES (%s, %s, %s, %s)",
                (user_id, account_number_from_transfer_1, account_number_from_transfer_2, sum_transfer))
            self.connection.commit()

        def get_Transactions_users(self, username):
            cursor = self.connection.cursor()
            self.animate_loading("Получение данных о ваших транзакциях")
            print(username)
            cursor.execute("SELECT id FROM people WHERE user_name = %s", (username,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                cursor.execute(
                    "SELECT user_id_1, account_number_1, account_number_2, sum_transfer FROM Transactions_users WHERE user_id_1 = %s",
                    (user_id,))
                Transactions_users = cursor.fetchall()
                if Transactions_users:
                    print("Список транзакций:")
                    for transaction in Transactions_users:
                        # Вывод информации о транзакции
                        user_id_p, account_number_p_1, account_number_p_2, sum_transfer = transaction
                        cursor.execute("SELECT DISTINCT user_name FROM people WHERE id = %s", (result))
                        name_in = cursor.fetchall()[0][0]
                        print(
                            Fore.GREEN + f"\tТранзакция была между счетом {str(account_number_p_1)}(отправитель) и счетом {str(account_number_p_2)}(получатель) сумма перевода {str(sum_transfer)} транзакцию совершил пользователь с логином {name_in}")

                else:
                    print("У вас пока нет транзакций.")
            else:
                print("Пользователь не найден.")

        def get_norm_question(self, what_check, username):
            user_name_id_and_bugs = username
            if len(what_check) == 0:
                print("Вы ввели не верные данные пожалуйста Попробуйте ещё раз (для выхода нажмите 0)")
                self.get_account_list(user_name_id_and_bugs)

        def auto_logined(self, login_user):
            cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")
            cursor.execute("INSERT INTO Logined_users(login_user_p) VALUES (%s)", (login_user,))
            self.connection.commit()

        def check_for_login(self):
            cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")
            cursor.execute("SELECT login_user_p FROM Logined_users")
            f = cursor.fetchall()
            if f:
                self.main_menu(f[0][0])
                self.connection.commit()

        def not_save_login(self):
            cursor.execute("DROP TABLE IF EXISTS Logined_users")
            self.connection.commit()

        init()  # Инициализация colorama

        def animate_loading(self, name_discription):
            animation = ['|', '/', '-', '\\']  # Анимационные символы
            for i in range(10):
                t.sleep(0.1)
                print(f'\r{Fore.YELLOW}Загрузка: {animation[i % len(animation)]}', end='', flush=True)
            print(f'\r{Fore.GREEN}{name_discription} завершена!')

            """
        def secret():
            while True:
                cursor.execute("CREATE TABLE IF NOT EXISTS secret(id serial, name_secret VARCHAR(100), secret VARCHAR(2048), password VARCHAR(100), defis VARCHAR(60), UNIQUE(defis))")
                defis = input("defis = ")
                password = input("password = ")
                self.connection.commit()
                if defis[::-1] == "@":
                    defis[::-1] = ""
                    cursor.execute("SELECT * FROM plan WHERE defis = %s AND password = %s", (defis, password))
                    x = cursor.fetchone()
                    self.connection.commit()
                    if x:
                        func = input("func = ")
                        if func == "1110":
                            print(Fore.YELLOW)
                            p = input("p = ")
                            nc = input("nc = ")
                            pcos = input("pcos = ")
                            spcos = int(input("spcos = "))
                            if spcos:
                                cursor.execute("INSERT INTO plans(name_company, plan, password, defis) VALUES(%s, %s, %s, %s)", (nc, p, pcos, nc))
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()
                            else:
                                print(Fore.RED + f"spcos = {spcos} incorrect!!!")

                        if func == "1101":
                            p = input("p = ")
                            pcos = input("pcos = ")
                            spcos = int(input("spcos = :"))
                            if spcos:
                                cursor.execute("DELETE FROM plan WHERE name_company = %s AND password = %s;", (nc, pcos))
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()

                        if func == "10010100001":
                            defis = input("defis = ")
                            spcos = int(input("spoc = "))
                            if spcos:
                                cursor.execute("SELECT * FROM plan WHERE defis = %s", (defis, ))
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()

                        if func == "1111011":
                            spcos = int(input("spoc = "))
                            if spcos:
                                cursor.execute("SELECT * FROM plan")
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()

                        if func == "1111011":
                            spcos = int(input("spoc = "))
                            if spcos:
                                cursor.execute("SELECT * FROM plan")
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()

                       if func == "10011":
                            que = int(input("que = "))
                            if que:
                                p = input("p = ")
                                cursor.execute("UPDATE plan SET plan += %s")
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()
                            else:
                                p = input("p = ")
                                cursor.execute("UPDATE plan SET plan = %s")
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()

                        if func == "111110011000000010001100100100":
                            spcos = int(input("spcos = "))
                            if spcos:
                                cursor.execute("DROP TABLE plan")
                                cursor.execute("CREATE TABLE IF NOT EXISTS secret(id serial, name_secret VARCHAR(100), secret VARCHAR(2048), password VARCHAR(100), defis VARCHAR(60), UNIQUE(defis))")
                                print(Fore.GREEN + "ДБСУ_СС")
                                self.connection.commit()
                            else:
                                raise "ok"
                                """


    bank = Bank(conn)

    while True:
        print(Fore.CYAN)
        x = bank.check_for_login()
        if x:
            break

        else:
            get_question = int(input(
                "Вы хотите войти или же пройти регистрацию(Регистрация = 0 , Вход = 1, Автоматически Вход = 2 или Завершение программы >= 3):"))
            if get_question == 0:
                get_name = input("Введите имя пользователя:")
                get_last_name = input("Введите свою фамилию:")
                get_password = input("Введите свой пароль:")
                try:
                    get_age = int(input("Сколько вам лет:"))

                except BaseException:
                    print(Fore.RED + "Вы ввели не корректный возраст")
                    continue

                bank.auto_logined(get_name)

                if get_name == "0" or get_last_name == "0":
                    bank.not_save_login()
                    break

                if len(get_password) > 7:
                    if get_name == "0" or get_age == 0 or get_last_name == "0" or get_password == "0":
                        bank.not_save_login()
                        print(Fore.RED + "Выход...")
                        break
                    else:
                        bank.add_user(get_name, get_last_name, get_password, get_age)
                        bank.auto_logined(get_name)
                        print(Fore.GREEN + "Поздравляю вы успешно прошли регистрацию и мы вас запомнили в базе!!!")

                else:
                    bank.not_save_login()
                    print(Fore.RED + "Вы ввели не коректный пароль!!!\nПопробуйте ещё раз")

            elif get_question == 1:
                print(Fore.RESET)
                get_login = input("Введите логин:")
                get_password_login = input("Введите пароль:")
                bank.auto_logined(get_login)
                if get_login == "0":
                    break

                else:
                    if len(get_password_login) > 7 or get_password_login == "1":
                        if get_password_login == "0" or get_login == "0":
                            bank.not_save_login()
                            break

                        else:
                            bank.login_user(get_login, get_password_login)
                            bank.auto_logined(get_login)

                    else:
                        bank.not_save_login()
                        print(Fore.RED + "Вы ввели не коректный пароль!!!\nПопробуйте ещё раз")

            elif get_question == 2:
                bank.login_user("1", "1")
                bank.auto_logined("1")

            elif get_question > 2:
                break


except BaseException as e:
    print("Произошла ошибка:", e)
    sys.exit(1)  # завершение программы с кодом ошибки 1
input("Нажмите Enter...")
