import uuid
from datetime import datetime
from flask import Flask, jsonify, request, render_template,  redirect, url_for, flash
from flask_cors import CORS
from dbconnection import get_db_connection
from db_utils import get_user,get_cycle,get_transaction,available_cycle

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'flash message'
response_object = {'status': 'success','status_code': 200, 'message': None}
# # enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/user_update", methods=['POST'])
def user_update():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                organization_id = request.form.get('organization_id')
                barcode_id = request.form.get('barcode_id')
                user_id = request.form.get('user_id')
                qry = f"UPDATE users SET organization_id='{organization_id}', barcode_id='{barcode_id}' where user_id={user_id}"
                cursor.execute(qry)
                conn.commit()
                response_object['message'] = "User updated!"
                return redirect(url_for('users'))
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object['message'] = "error"
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object['message'] = "error"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

@app.route("/user_delete/<user_id>")
def user_delete(user_id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            qry = f"UPDATE users SET status='inactive' where user_id={user_id}"
            cursor.execute(qry)
            conn.commit()
            print("user--------------------->",user_id)
            response_object['message'] = "User deleted!"
            return redirect(url_for('users'))
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object['message'] = "error"
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object['message'] = "error"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

# Test Route to Fetch Data
@app.route('/users', methods=['GET','POST'])
def users():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                name = request.form.get('name')
                organization_id = request.form.get('organization_id')
                barcode_id = request.form.get('barcode_id')
                qry = "INSERT INTO users (name, barcode_id, organization_id, status) VALUES (%s, %s, %s, %s)"
                val = (name, barcode_id, organization_id, 'active')
                cursor.execute(qry, val)
                conn.commit()
                response_object['message'] = 'User added!'
                # return render_template('user.html', users=users, message="User added!")
                return redirect(url_for('users'))
            elif request.method == 'GET':
                users = get_user()
                msg = response_object["message"]
                response_object["message"] = None
                return render_template('user.html', users=users, message=msg)
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object['message'] = "error"
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object['message'] = "error"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

@app.route("/cycle_update", methods=['POST'])
def cycle_update():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                status = request.form.get('status')
                barcode_id = request.form.get('barcode_id')
                cycle_id = request.form.get('cycle_id')
                qry = f"UPDATE cycles SET barcode_id='{barcode_id}', status='{status}' where cycle_id={cycle_id}"
                print(qry)
                cursor.execute(qry)
                conn.commit()
                response_object['message'] = "Cycle updated!"
                return redirect(url_for('cycles'))
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object['message'] = "error"
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object['message'] = "error"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

@app.route("/cycle_delete/<cycle_id>")
def cycle_delete(cycle_id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            qry = f"UPDATE cycles SET status='Deactived' where cycle_id={cycle_id}"
            cursor.execute(qry)
            conn.commit()
            print("cycle--------------------->",cycle_id)
            response_object['message'] = "Cycle deleted!"
            return redirect(url_for('cycles'))
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object['message'] = "error"
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object['message'] = "error"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

@app.route('/cycles', methods=['GET', 'POST'])
def cycles():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                reference_id = request.form.get('reference_id')
                status = request.form.get('status')
                barcode_id = request.form.get('barcode_id')
                qry = "INSERT INTO cycles (reference_id, barcode_id, status) VALUES (%s, %s, %s)"
                val = (reference_id, barcode_id, status)
                cursor.execute(qry, val)
                conn.commit()
                response_object['message'] = 'Cycle added!'
                # return render_template('user.html', users=users, message="User added!")
                return redirect(url_for('cycles'))
            elif request.method == 'GET':
                cycles = get_cycle()
                msg = response_object["message"]
                response_object["message"] = None
                return render_template('cycle.html', cycles=cycles, message=msg)
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object['message'] = "error"
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object['message'] = "error"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

@app.route('/rent', methods=['GET','POST'])
def rent():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                cycle_id = request.form.get('cycle_id')
                user_id = request.form.get('user_id')
                rented_date = datetime.now()
                qry = "INSERT INTO rental_transactions (cycle_id, user_id, rent_start_date, transaction_status) VALUES (%s, %s, %s, %s)"
                val = (cycle_id, user_id, rented_date, 'Rented')
                cursor.execute(qry, val)
                conn.commit()
                cycle_qry = f"UPDATE cycles SET status='On-Rent' where cycle_id={cycle_id}"
                cursor.execute(cycle_qry)
                conn.commit()
                response_object['message'] = 'Successfully Rented!'
                # return render_template('user.html', users=users, message="User added!")
                return redirect(url_for('rent'))
            elif request.method == 'GET':
                transactions = get_transaction()
                cycles = available_cycle()
                msg = response_object["message"]
                response_object["message"] = None
                return render_template('transactions.html', cycles=cycles, transactions=transactions, message=msg)
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object['message'] = "error"
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object['message'] = "error"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

@app.route('/cycle_return/<transaction_id>/<user_id>/<cycle_id>')
def rent_return(transaction_id,user_id,cycle_id):
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            date = datetime.now()
            trans_qry = f"UPDATE rental_transactions SET transaction_status='Returned', rent_end_date='{date}' where transaction_id={transaction_id}"
            print(trans_qry)
            cursor.execute(trans_qry)
            conn.commit()
            cycle_qry = f"UPDATE cycles SET status='Available' where cycle_id={cycle_id}"
            cursor.execute(cycle_qry)
            conn.commit()
            user_qry = f"UPDATE users SET rented_history={transaction_id} where user_id={user_id}"
            cursor.execute(user_qry)
            conn.commit()
            # print(cursor.rowcount, "record inserted.")
            response_object['message'] = "Successfully Returned!"
            return redirect(url_for('rent'))
        else:
            response_object['status'] = "failed"
            response_object['status_code'] = 500
            response_object["error"] = "Database connection failed"
    except Exception as e:
        response_object['status'] = "error"
        response_object['status_code'] = 404
        response_object["error"] = str(e)
    return jsonify(response_object)

@app.route("/getuser/<barcode_id>")
def getuser(barcode_id):
    try:
        user = getuser_barcode(barcode_id)
        if len(user) == 1:
            response_object["message"] = None
            response_object["user"] = user
        elif len(user) == 0:
            response_object["message"] = "User doesn't exit in the system. Please add the user."
            response_object["user"] = []
        else:
            response_object["message"] = "Please check the user barcode....!"
            print(user)
            response_object["user"] = []
    except Exception as e:
        response_object["message"] = "Error..!"
        response_object["error"] = str(e)
        print(e)
    return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True)
