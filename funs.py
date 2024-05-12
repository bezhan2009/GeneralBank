from flask import (Flask,
                   render_template
                   )

app = Flask(__name__)
app.secret_key = 'bezhan200910203040'

'''db_name = "postgres"
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
except psycopg2.Error as e:
    print(e)
    redirect_to_connect()
'''


def get_err(err):
    with app.app_context():
        return render_template("error_p.html", reall_error=err)


def login_user(conn, login, password):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people WHERE user_name = %s AND password = %s", (login, password))
    x = cursor.fetchone()
    if x:
        return True
    else:
        return False


def create_an_account(conn, _id, acc_num, username):
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Accounts_users  '
                       '(user_id, account_number) '
                       'VALUES (%s, %s)', (_id, acc_num,))
        cursor.execute('UPDATE Accounts_users SET user_name_id = %s WHERE user_id = %s', (username, _id))
        conn.commit()

        return True  # Возвращаем True, если операции прошли успешно

    except BaseException as e:
        conn.rollback()
        return False  # Возвращаем False, если возникла ошибка


def delete_an_account(conn, _id, acc_id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_number FROM Accounts_users WHERE user_id = %s AND id = %s AND is_deleted = 'False'",
        (_id, acc_id))
    result = cursor.fetchall()
    if result:
        cursor.execute("UPDATE Accounts_users SET is_deleted = 'True' WHERE user_id = %s AND account_number = %s",
                       (_id, acc_id))
        conn.commit()
        return True
    else:
        return False


def withdraw_money(conn, _id, acc_num, amount):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_number FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'",
        (_id, acc_num))
    result = cursor.fetchall()
    if result:
        cursor.execute(
            "SELECT balance FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'",
            (_id, acc_num))
        get_balance = cursor.fetchall()
        if get_balance[0][0] > int(amount):
            cursor.execute(
                "UPDATE Accounts_users SET balance = balance - %s WHERE user_id = %s AND account_number = %s",
                (amount, _id, acc_num))
            conn.commit()
            return True

        else:
            return render_template('amount_error.html')
    else:
        return False


def fill_money(conn, _id, acc_num, amount):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_number FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'",
        (_id, acc_num))
    result = cursor.fetchall()
    if result:
        cursor.execute("UPDATE Accounts_users SET balance = balance + %s WHERE user_id = %s AND account_number = %s",
                       (amount, _id, acc_num))
        conn.commit()
        return True

    else:
        return False


def transfer_money(conn, _id, acc_num_1, acc_num_2, amount):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_number FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'",
        (_id, acc_num_1))
    result_1 = cursor.fetchall()
    cursor.execute(
        "SELECT account_number FROM Accounts_users WHERE account_number = %s AND is_deleted = 'False'",
        (acc_num_2,))
    result_2 = cursor.fetchall()
    if result_1 and result_2:
        cursor.execute(
            "SELECT balance FROM Accounts_users WHERE user_id = %s AND account_number = %s AND is_deleted = 'False'",
            (_id, acc_num_1))
        cursor.execute(
            "SELECT balance FROM Accounts_users WHERE account_number = %s AND is_deleted = 'False'",
            (acc_num_2,))
        get_balance = cursor.fetchall()
        if get_balance[0][0] > int(amount):
            cursor.execute(
                "UPDATE Accounts_users SET balance = balance - %s WHERE user_id = %s AND account_number = %s",
                (amount, _id, acc_num_1))
            cursor.execute(
                "UPDATE Accounts_users SET balance = balance + %s WHERE account_number = %s",
                (amount, acc_num_2))

            conn.commit()
            return True

        else:
            return False
    else:
        return False


def delete_an_account_from_user_accounts(conn, user_id, acc_num):
    cursor = conn.cursor()
    try:
        # Проверяем, существует ли счет пользователя
        cursor.execute("SELECT * FROM Accounts_users WHERE user_id = %s AND account_number = %s", (user_id, acc_num))
        account_exists = cursor.fetchone()

        # Если счет существует, помечаем его как удаленный
        if account_exists:
            cursor.execute("UPDATE Accounts_users SET is_deleted = TRUE WHERE user_id = %s AND account_number = %s",
                           (user_id, acc_num))
            conn.commit()
            return True
        else:
            # Если счет не существует, возвращаем False
            return False
    except Exception as e:
        # Обработка ошибок, если возникнут проблемы при выполнении запросов
        print(f"Error deleting account: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
