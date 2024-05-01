use rusqlite::{params, Connection, Result};

fn transfer_money(conn: &Connection, user_id: i32, acc_num_1: &str, acc_num_2: &str, amount: i32) -> Result<bool> {
    // Start a transaction to ensure data consistency
    let transaction = conn.transaction()?;

    // Check if the accounts exist and are active
    let mut cursor = transaction.prepare("SELECT account_number FROM Accounts_users WHERE user_id = ? AND account_number = ? AND is_deleted = 'False'")?;
    let result_1: Vec<String> = cursor.query_map(params![user_id, acc_num_1], |row| row.get(0))?.collect();
    let result_1_exists = !result_1.is_empty();

    let mut cursor = transaction.prepare("SELECT account_number FROM Accounts_users WHERE account_number = ? AND is_deleted = 'False'")?;
    let result_2: Vec<String> = cursor.query_map(params![acc_num_2], |row| row.get(0))?.collect();
    let result_2_exists = !result_2.is_empty();

    if result_1_exists && result_2_exists {
        // Check balance before transaction
        let mut cursor = transaction.prepare("SELECT balance FROM Accounts_users WHERE user_id = ? AND account_number = ? AND is_deleted = 'False'")?;
        let balance_1: i32 = cursor.query_row(params![user_id, acc_num_1], |row| row.get(0))?;

        if balance_1 >= amount {
            // Update balances
            transaction.execute("UPDATE Accounts_users SET balance = balance - ? WHERE user_id = ? AND account_number = ?",
                         params![amount, user_id, acc_num_1])?;
            transaction.execute("UPDATE Accounts_users SET balance = balance + ? WHERE account_number = ?",
                         params![amount, acc_num_2])?;

            // Commit the transaction
            transaction.commit()?;
            Ok(true)
        } else {
            // Rollback the transaction if balance is insufficient
            transaction.rollback()?;
            Ok(false) // Returning error should be handled accordingly
        }
    } else {
        // Rollback the transaction if accounts do not exist
        transaction.rollback()?;
        Ok(false)
    }
}

fn main() {
    // Your main logic here
}
