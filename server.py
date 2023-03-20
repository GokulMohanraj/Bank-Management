from flask import Flask, render_template, request
import re
from database import connection, engine
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def new_customer():
    if request.method == "GET":
        customer_name = request.form.get('name')
        input_age = request.form.get('age')
        email_id = request.form.get('email')
        userid = request.form.get('userid')
        password = request.form.get('password')
        customer_address = request.form.get('address')
        number = request.form.get('number')
        open_balance = request.form.get('balance')

        insert_value = "insert into customer_details (Name, user_id, age, mobile_number, email, address, " \
                       "password, opening_balance) values (%s, %s, %s, %s, %s, %s, %s, %s )"
        values = [
            (customer_name, userid, input_age, number, email_id, customer_address, password, open_balance)]
        connection.executemany(insert_value, values)
        engine.commit()
        return 'successfully created'
    return render_template("signup.html")
