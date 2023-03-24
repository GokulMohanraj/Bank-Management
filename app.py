from flask import Flask, request, render_template, redirect
import re
from datetime import datetime
from database import my_cursor, text

app = Flask(__name__)


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template("main.html")


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        req = request.form
        userid = req['userid']
        password = req['password']
        if not userid.islower():
            return 'user-id must be in lowercase'
        query = text("SELECT user_id FROM customer_details WHERE user_id = :userid")
        value = [{'userid': userid}]
        data = my_cursor.execute(query, value)
        stored_userid = data.fetchone()
        if stored_userid is None:
            return 'User id not found'
        elif userid != str(stored_userid[0]):
            return 'User id is incorrect!!'
        query = text("SELECT password FROM customer_details WHERE user_id = :userid")
        value = [{'userid': userid}]
        data = my_cursor.execute(query, value)
        database_password = data.fetchone()
        password_comparing = str(database_password[0])
        if password != password_comparing:
            return 'Password is incorrect!!'
        else:
            return redirect("/signin.html")
    else:
        return 'something problem'


@app.route('/signup.html', methods=['POST', 'GET'])
def signup():
    return render_template("signup.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        req = request.form.to_dict()
        name = req['name']
        userid = req['userid']
        password = req['password']
        conform_password = req['conform_password']
        dob = req['dob']
        address = req['address']
        email = req['email']
        number = req['number']
        balance = req['balance']
        if not name.strip():
            return "Input is empty."
        elif re.search(r'\d', name):
            return "Name contains numeric characters."
        if userid.islower():
            query = text('SELECT user_id FROM customer_details WHERE user_id = :userid')
            value = [{'userid': userid}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return 'User_id is already exist'
        else:
            return 'user-id must be in lowercase letter'

        if len(password) < 8:
            return "Not valid ! Total characters should be grater than 8"
        elif not re.search("[A-Z]", password):
            return "Not valid ! It should contain at least one uppercase letter"
        elif not re.search("[a-z]", password):
            return "Not valid ! It should contain at least one lowercase letter"
        elif not re.search("[1-9]", password):
            return "Not valid ! It should contain at least one number"
        elif not re.search("[~!@#$%^&*]", password):
            return "Not valid ! It should contain at least one special character"
        elif re.search(r"\s", password):
            return "Not valid ! It should not contain any space"
        elif password != conform_password:
            return 'Your password is mismatch'

        birthdate = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if not age >= 18:
            return 'Age must be 18 or above'

        if not address.strip():
            return 'Please fill the address'

        if not email.endswith('.com'):
            return 'E-mail_id format is not correct'
        elif email.islower():
            query = text('SELECT email FROM customer_details WHERE email = :email')
            value = [{'email': email}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return 'Email-id already exist'
        else:
            return 'E-mail_id should not contain any uppercase letter'

        if len(number) < 10 or len(number) > 10:
            return 'Mobile number is not valid (Enter a 10 digit number)'
        elif re.search(r"\s", number):
            return "Not valid ! It should not contain any space"
        elif number.isnumeric():
            query = text('SELECT number FROM customer_details WHERE number = :number')
            value = [{'number': number}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return 'Mobile number already exist'
        else:
            return 'Number is not valid (A number should not contain any characters)'

        try:
            if int(balance) < 500:
                return 'Amount should be greater than 500'
        except ValueError:
            return 'Not valid ! Input should be number'

        try:
            insert_value = text("insert into customer_details (name, user_id, password, age, address,  number, email,"
                                "opening_balance) VALUES (:name,:userid,:password,:age,:address,:number,:email,"
                                ":balance)")
            values = [
                {'name': name, 'userid': userid, 'password': password, 'age': age, 'address': address, 'number': number,
                 'email': email, 'balance': balance},
            ]
            my_cursor.execute(insert_value, values)
            my_cursor.commit()
            return redirect('/success')
        except ValueError:
            return 'Something problem your data is not stored in database.. Please try again..'

    else:
        return 'something problem'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
