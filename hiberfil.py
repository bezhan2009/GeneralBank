
def first_open(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS people(id SERIAL PRIMARY KEY,user_name VARCHAR(50) UNIQUE,last_name VARCHAR(50) NOT NULL,password VARCHAR(50) NOT NULL,age INT NOT NULL,UNIQUE (id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Accounts_users(id serial, user_id INT NOT NULL , user_name_id VARCHAR(40), account_number VARCHAR(70), balance  INT DEFAULT 10000, FOREIGN KEY (user_id) REFERENCES people (id));")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Transactions_users(id serial, user_id_1 INT NOT NULL, account_number_1 VARCHAR(70), account_number_2 VARCHAR(70), sum_transfer INT NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Logined_users(id serial, login_user_p VARCHAR(40))")
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

        elif not view_for_bugs:
            cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
            conn.commit()

        elif not view_for_bugs_2:
            cursor.execute("INSERT INTO Accounts_users(user_id, account_number) VALUES (%s, %s)", (1, '9847293'))
            conn.commit()
    except Exception as e:
        print(e)
