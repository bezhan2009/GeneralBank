use rusqlite::{params, Connection};
use std::ffi::{CStr, CString};
use libc::c_char;

#[no_mangle]
pub extern "C" fn transfer_money(
    conn_ptr: *mut Connection,
    user_id: i32,
    acc_num_1: *const c_char,
    acc_num_2: *const c_char,
    amount: i32
) -> bool {
    // Преобразование указателя в ссылку на объект Connection
    let conn = unsafe {
        assert!(!conn_ptr.is_null());
        &mut *conn_ptr
    };

    let tx = match conn.transaction() {
        Ok(tx) => tx,
        Err(_) => return false,
    };

    let acc_num_1_str = unsafe {
        assert!(!acc_num_1.is_null());
        CStr::from_ptr(acc_num_1)
    };
    let acc_num_2_str = unsafe {
        assert!(!acc_num_2.is_null());
        CStr::from_ptr(acc_num_2)
    };

    let acc_num_1_string = match acc_num_1_str.to_str() {
        Ok(s) => s.to_owned(),
        Err(_) => return false,
    };

    let acc_num_2_string = match acc_num_2_str.to_str() {
        Ok(s) => s.to_owned(),
        Err(_) => return false,
    };

    let result_1: (String, i32) = {
        let mut cursor_1 = match tx.prepare(
            "SELECT account_number, balance FROM Accounts_users WHERE user_id = ? AND account_number = ? AND is_deleted = 'False'"
        ) {
            Ok(cursor) => cursor,
            Err(_) => return false,
        };

        match cursor_1.query_row(
            params![user_id, &acc_num_1_string as &dyn rusqlite::ToSql],
            |row| {
                let account_number: String = row.get(0)?;
                let balance: i32 = row.get(1)?;
                Ok((account_number, balance))
            }
        ) {
            Ok(result) => result,
            Err(_) => return false,
        }
    };

    let result_2_exists: bool = {
        let mut cursor_2 = match tx.prepare(
            "SELECT account_number FROM Accounts_users WHERE account_number = ? AND is_deleted = 'False'"
        ) {
            Ok(cursor) => cursor,
            Err(_) => return false,
        };

        match cursor_2.query_row(
            params![&acc_num_2_string as &dyn rusqlite::ToSql],
            |row| Ok(row.get::<usize, String>(0).is_ok())
        ) {
            Ok(result) => result,
            Err(_) => return false,
        }
    };

    if result_2_exists {
        let balance_1 = result_1.1;

        if balance_1 >= amount {
            if tx.execute(
                "UPDATE Accounts_users SET balance = balance - ? WHERE user_id = ? AND account_number = ?",
                params![amount, user_id, &acc_num_1_string as &dyn rusqlite::ToSql]
            ).is_err() {
                return false;
            }

            if tx.execute(
                "UPDATE Accounts_users SET balance = balance + ? WHERE account_number = ?",
                params![amount, &acc_num_2_string as &dyn rusqlite::ToSql]
            ).is_err() {
                return false;
            }

            match tx.commit() {
                Ok(_) => true,
                Err(_) => false,
            }
        } else {
            false
        }
    } else {
        false
    }
}
