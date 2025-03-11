from dbconnection import get_db_connection

def get_user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users where status='active'")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(cursor.rowcount, "record inserted.")
    return users

def get_cycle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    qry = """SELECT c.cycle_id, c.reference_id, c.barcode_id, c.status, COALESCE(u.name, 'N/A') AS last_rented_by
    FROM cycle_rent.cycles AS c 
    LEFT JOIN cycle_rent.users AS u 
    ON u.user_id = c.last_rented_by
    """
    cursor.execute(qry)
    cycles = cursor.fetchall()
    cursor.close()
    conn.close()
    print(cycles)
    # print(cursor.rowcount, "record inserted.")
    return cycles

def get_transaction():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        #qry = "SELECT rt.transaction_id, rt.cycle_id, rt.user_id, rt.rent_start_date, rt.rent_end_date, rt.transaction_status, u.name, u.barcode_id as user_barcode, c.reference_id, c.barcode_id as cycle_barcode FROM rental_transactions as rt, cycles as c, users as u WHERE c.cycle_id=rt.cycle_id AND u.user_id=c.last_rented_by ORDER BY rt.rent_start_date DESC"
        qry = """SELECT  rt.transaction_id, rt.cycle_id, rt.user_id, rt.rent_start_date, rt.rent_end_date, 
        rt.transaction_status, u.name, u.barcode_id AS user_barcode, c.reference_id, c.barcode_id AS cycle_barcode 
        FROM rental_transactions AS rt
        INNER JOIN cycles AS c ON c.cycle_id = rt.cycle_id
        INNER JOIN users AS u ON u.user_id = rt.user_id
        ORDER BY rt.rent_start_date DESC;
        """
        cursor.execute(qry)
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        # print(cursor.rowcount, "record inserted.")
        return transactions
    except Exception as e:
        print(e)

def available_cycle():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cycles where status='Available'")
    cycles = cursor.fetchall()
    cursor.close()
    conn.close()
    print(cycles)
    # print(cursor.rowcount, "record inserted.")
    return cycles

def return_cycle(transaction_id):
    transaction = RentalTransaction.query.get(transaction_id)
    if transaction and transaction.transaction_status == "Rented":
        transaction.transaction_status = "Returned"
        transaction.rent_end_date = db.func.current_timestamp()
        cycle = Cycle.query.get(transaction.cycle_id)
        cycle.status = "Available"
        db.session.commit()
        return transaction
    return None

def getuser_barcode(barcode_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users where barcode_id='{barcode_id}'")
    user = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(cursor.rowcount, "record inserted.")
    return user
