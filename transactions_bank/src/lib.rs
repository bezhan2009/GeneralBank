use rusqlite::{params, Connection, Result, Savepoint};
use std::ffi::CStr;
use std::str;

#[no_mangle]
pub extern "C" fn transfer_money(conn_ptr: *mut Connection, user_id: i32, acc_num_1: *const libc::c_char, acc_num_2: *const libc::c_char, amount: i32) -> bool {
    // Преобразование указателя в ссылку на объект Connection
    let conn = unsafe {
        assert!(!conn_ptr.is_null());
        &mut *conn_ptr
    };

    // Создание savepoint для управления транзакцией
    let mut savepoint = match conn.savepoint() {
        Ok(savepoint) => savepoint,
        Err(_) => return false,
    };

    // Начало транзакции после создания savepoint
    match conn.transaction() {
        Ok(tx) => {
            // Преобразуем acc_num_1 из *const libc::c_char в строку Rust
            let acc_num_1_str = unsafe {
                assert!(!acc_num_1.is_null());
                CStr::from_ptr(acc_num_1)
            };
            let acc_num_1_string = match acc_num_1_str.to_str() {
                Ok(s) => s.to_owned(),
                Err(_) => {
                    savepoint.rollback().expect("Failed to rollback savepoint");
                    return false;
                }
            };

            let mut cursor_1 = match tx.prepare("SELECT account_number, balance FROM Accounts_users WHERE user_id = ? AND account_number = ? AND is_deleted = 'False'") {
                Ok(cursor) => cursor,
                Err(_) => {
                    savepoint.rollback().expect("Failed to rollback savepoint");
                    return false;
                }
            };

            let result_1: (String, i32) = match cursor_1.query_row(params![user_id, &acc_num_1_string as &dyn rusqlite::ToSql], |row| {
                let account_number: String = row.get(0)?;
                let balance: i32 = row.get(1)?;
                Ok((account_number, balance))
            }) {
                Ok(result) => result,
                Err(_) => {
                    savepoint.rollback().expect("Failed to rollback savepoint");
                    return false;
                }
            };

            let mut cursor_2 = match tx.prepare("SELECT account_number FROM Accounts_users WHERE account_number = ? AND is_deleted = 'False'") {
                Ok(cursor) => cursor,
                Err(_) => {
                    savepoint.rollback().expect("Failed to rollback savepoint");
                    return false;
                }
            };

            let result_2_exists: bool = match cursor_2.query_row(params![acc_num_2], |row| Ok(row.get::<usize, String>(0).is_ok())) {
                Ok(result) => result,
                Err(_) => {
                    savepoint.rollback().expect("Failed to rollback savepoint");
                    return false;
                }
            };

            if result_2_exists {
                let balance_1 = result_1.1;

                if balance_1 >= amount {
                    match tx.execute("UPDATE Accounts_users SET balance = balance - ? WHERE user_id = ? AND account_number = ?",
                                     params![amount, user_id, &acc_num_1_string as &dyn rusqlite::ToSql]) {
                        Ok(_) => {},
                        Err(_) => {
                            savepoint.rollback().expect("Failed to rollback savepoint");
                            return false;
                        }
                    }

                    match tx.execute("UPDATE Accounts_users SET balance = balance + ? WHERE account_number = ?",
                                     params![amount, acc_num_2]) {
                        Ok(_) => {},
                        Err(_) => {
                            savepoint.rollback().expect("Failed to rollback savepoint");
                            return false;
                        }
                    }

                    // Прочие операции внутри транзакции...

                    // Завершение транзакции
                    match tx.commit() {
                        Ok(_) => true,
                        Err(_) => {
                            savepoint.rollback().expect("Failed to rollback savepoint");
                            false
                        }
                    }
                } else {
                    savepoint.rollback().expect("Failed to rollback savepoint");
                    false
                }
            } else {
                savepoint.rollback().expect("Failed to rollback savepoint");
                false
            }
        }
        Err(_) => false
    }
}
