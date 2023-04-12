from flask import Flask, request, render_template, redirect, session
import re
from datetime import datetime
from database import my_cursor, text

app = Flask(__name__)
app.secret_key = "mysecretkey"


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template("main.html")


@app.route('/signin.html', methods=['POST', 'GET'])
def signin():
    userid = session['userid']
    query = text("SELECT name FROM customer_details WHERE user_id = :userid")
    value = [{'userid': userid}]
    data = my_cursor.execute(query, value)
    username = data.fetchone()
    name = username[0]
    return render_template('signin.html', name=name)


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        req = request.form
        userid = req['userid']
        session['userid'] = userid
        password = req['password']
        if not userid.islower():
            return 'user-id must be in lowercase'
        query = text("SELECT user_id FROM customer_details WHERE user_id = :userid")
        value = [{'userid': userid}]
        data = my_cursor.execute(query, value)
        stored_userid = data.fetchone()
        if stored_userid is None:
            return_message = 'User id not found'
            return render_template("/main.html", return_message=return_message)
        elif userid != str(stored_userid[0]):
            return_message = 'User id is incorrect!!'
            return render_template("/main.html", return_message=return_message)
        query = text("SELECT password FROM customer_details WHERE user_id = :userid")
        value = [{'userid': userid}]
        data = my_cursor.execute(query, value)
        database_password = data.fetchone()
        password_comparing = str(database_password[0])
        if password != password_comparing:
            return_message = 'Password is incorrect!!'
            return render_template("/main.html", return_message=return_message)
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
        answer = req['answer']
        dob = req['dob']
        address = req['address']
        email = req['email']
        number = req['number']
        balance = req['balance']
        if not name.strip():
            return_message = "Input is empty."
            return render_template("/signup.html", return_message=return_message)
        elif re.search(r'\d', name):
            return_message = "Name contains numeric characters."
            return render_template("/signup.html", return_message=return_message)
        if userid.islower():
            query = text('SELECT user_id FROM customer_details WHERE user_id = :userid')
            value = [{'userid': userid}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return_message = 'User_id is already exist'
                return render_template("/signup.html", return_message=return_message)
        else:
            return_message = 'user-id must be in lowercase letter'
            return render_template("/signup.html", return_message=return_message)

        if len(password) < 8:
            return_message = "Not valid ! Total characters should be grater than 8"
            return render_template("/signup.html", return_message=return_message)
        elif not re.search("[A-Z]", password):
            return_message = "Not valid ! It should contain at least one uppercase letter"
            return render_template("/signup.html", return_message=return_message)
        elif not re.search("[a-z]", password):
            return_message = "Not valid ! It should contain at least one lowercase letter"
            return render_template("/signup.html", return_message=return_message)
        elif not re.search("[1-9]", password):
            return_message = "Not valid ! It should contain at least one number"
            return render_template("/signup.html", return_message=return_message)
        elif not re.search("[~!@#$%^&*]", password):
            return_message = "Not valid ! It should contain at least one special character"
            return render_template("/signup.html", return_message=return_message)
        elif re.search(r"\s", password):
            return_message = "Not valid ! It should not contain any space"
            return render_template("/signup.html", return_message=return_message)
        elif password != conform_password:
            return_message = 'Your password is mismatch'
            return render_template("/signup.html", return_message=return_message)

        if not answer.strip():
            return_message = 'Enter your security answer'
            return render_template("/signup.html", return_message=return_message)

        birthdate = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        if not age >= 18:
            return_message = 'Age must be 18 or above'
            return render_template("/signup.html", return_message=return_message)

        if not address.strip():
            return_message = 'Please fill the address'
            return render_template("/signup.html", return_message=return_message)

        if not email.endswith('.com'):
            return_message = 'E-mail_id format is not correct'
            return render_template("/signup.html", return_message=return_message)
        elif email.islower():
            query = text('SELECT email FROM customer_details WHERE email = :email')
            value = [{'email': email}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return_message = 'Email-id already exist'
                return render_template("/signup.html", return_message=return_message)
        else:
            return_message = 'E-mail_id should not contain any uppercase letter'
            return render_template("/signup.html", return_message=return_message)

        if len(number) < 10 or len(number) > 10:
            return_message = 'Mobile number is not valid (Enter a 10 digit number)'
            return render_template("/signup.html", return_message=return_message)
        elif re.search(r"\s", number):
            return_message = "Not valid ! It should not contain any space"
            return render_template("/signup.html", return_message=return_message)
        elif number.isnumeric():
            query = text('SELECT number FROM customer_details WHERE number = :number')
            value = [{'number': number}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return_message = 'Mobile number already exist'
                return render_template("/signup.html", return_message=return_message)
        else:
            return_message = 'Number is not valid (A number should not contain any characters)'
            return render_template("/signup.html", return_message=return_message)

        try:
            if int(balance) < 500:
                return_message = 'Amount should be greater than 500'
                return render_template("/signup.html", return_message=return_message)
        except ValueError:
            return_message = 'Not valid ! Input should be number'
            return render_template("/signup.html", return_message=return_message)

        try:
            insert_value = text("insert into customer_details (name, user_id, password, age, address,  number, email,"
                                "opening_balance, answer) VALUES (:name,:userid,:password,:age,:address,"
                                ":number,:email,:balance,:answer)")
            values = [
                {'name': name, 'userid': userid, 'password': password, 'age': age, 'address': address,
                 'number': number, 'email': email, 'balance': balance, 'answer': answer}]
            my_cursor.execute(insert_value, values)
            my_cursor.commit()
            return redirect('/main.html')
        except ConnectionResetError:
            my_cursor.rollback()
            return_message = 'Something problem your data is not stored in database.. Please try again..'
            return render_template("/signup.html", return_message=return_message)

    else:
        return_message = 'something problem'
        return render_template("/signup.html", return_message=return_message)


@app.route('/forgotpassword.html', methods=['POST', 'GET'])
def forgot_password():
    return render_template("forgotpassword.html")


@app.route('/forgot_pass', methods=['POST', 'GET'])
def forgot_pass():
    if request.method == "POST":
        req = request.form.to_dict()
        userid = req['userid']
        answer = req['answer']
        if userid.islower():
            query = text('SELECT user_id FROM customer_details WHERE user_id = :userid')
            value = [{'userid': userid}]
            data = my_cursor.execute(query, value)
            if not data.fetchone():
                return_message = 'Incorrect User-id..'
                return render_template("/forgotpassword.html", return_message=return_message)
        else:
            return_message = 'User-id must be in lowercase..'
            return render_template("/forgotpassword.html", return_message=return_message)

        try:
            query = text('SELECT answer FROM customer_details WHERE user_id = :userid')
            value = [{'userid': userid}]
            data = my_cursor.execute(query, value)
            stored_answer = data.fetchone()
            ans = stored_answer[0]
            if ans != answer:
                return_message = 'Your security question or answer are incorrect....'
                return render_template("/forgotpassword.html", return_message=return_message)
        except ConnectionRefusedError:
            return_message = 'Something problem try again'
            return render_template("/forgotpassword.html", return_message=return_message)
        return redirect('/create_new_password.html')
    else:
        return_message = 'Something problem try again after some time'
        return render_template("/forgotpassword.html", return_message=return_message)


@app.route('/create_new_password.html', methods=['POST', 'GET'])
def create_new_password():
    return render_template('create_new_password.html')


@app.route('/new_pass', methods=['POST', 'GET'])
def new_pass():
    if request.method == 'POST':
        req = request.form.to_dict()
        email = req['email']
        password = req['password']
        conform_pass = req['conform_pass']

        if not email.endswith('.com'):
            return_message = 'E-mail_id format is not correct'
            return render_template("/create_new_password.html", return_message=return_message)
        elif email.islower():
            query = text('SELECT email FROM customer_details WHERE email = :email')
            value = [{'email': email}]
            data = my_cursor.execute(query, value)
            stored_email = data.fetchone()
            mail = stored_email[0]
            if mail != email:
                return_message = 'Invalid Email-id'
                return render_template("/create_new_password.html", return_message=return_message)
        else:
            return 'E-mail_id should not contain any uppercase letter'

        if len(password) < 8:
            return_message = "Not valid ! Total characters should be grater than 8"
            return render_template("/create_new_password.html", return_message=return_message)
        elif not re.search("[A-Z]", password):
            return_message = "Not valid ! It should contain at least one uppercase letter"
            return render_template("/create_new_password.html", return_message=return_message)
        elif not re.search("[a-z]", password):
            return_message = "Not valid ! It should contain at least one lowercase letter"
            return render_template("/create_new_password.html", return_message=return_message)
        elif not re.search("[1-9]", password):
            return_message = "Not valid ! It should contain at least one number"
            return render_template("/create_new_password.html", return_message=return_message)
        elif not re.search("[~!@#$%^&*]", password):
            return_message = "Not valid ! It should contain at least one special character"
            return render_template("/create_new_password.html", return_message=return_message)
        elif re.search(r"\s", password):
            return_message = "Not valid ! It should not contain any space"
            return render_template("/create_new_password.html", return_message=return_message)
        elif password != conform_pass:
            return_message = 'Your password is mismatch'
            return render_template("/create_new_password.html", return_message=return_message)

        try:
            query = text("UPDATE customer_details SET password = :password WHERE email = :email")
            value = [{'password': password, 'email': email}]
            my_cursor.execute(query, value)
            my_cursor.commit()
            return redirect('/main.html')
        except NotImplemented:
            my_cursor.rollback()
            return_message = 'Something problem try again after some time'
            return render_template("/create_new_password.html", return_message=return_message)
    else:
        return_message = 'Something problem try again after some time'
        return render_template("/create_new_password.html", return_message=return_message)


@app.route('/change_number.html', methods=['POST', 'GET'])
def change_number():
    return render_template('change_number.html')


@app.route('/change_number', methods=['POST', 'GET'])
def change_num():
    if request.method == 'POST':
        req = request.form
        userid = session['userid']
        number = req['number']
        if len(number) < 10 or len(number) > 10:
            return_message = 'Mobile number is not valid (Enter a 10 digit number)'
            return render_template("/change_number.html", return_message=return_message)
        elif re.search(r"\s", number):
            return_message = "Not valid ! It should not contain any space"
            return render_template("/change_number.html", return_message=return_message)
        elif number.isnumeric():
            query = text('SELECT number FROM customer_details WHERE number = :number')
            value = [{'number': number}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return_message = 'Mobile number already exist'
                return render_template("/change_number.html", return_message=return_message)
        else:
            return_message = 'Number is not valid (A number should not contain any characters)'
            return render_template("/change_number.html", return_message=return_message)
        try:
            query = text("UPDATE customer_details SET number = :number WHERE user_id = :userid")
            value = [{'number': number, 'userid': userid}]
            my_cursor.execute(query, value)
            my_cursor.commit()
            return redirect('/update_profile.html')
        except NotImplemented:
            my_cursor.rollback()
            return_message = 'Something problem try again after some time'
            return render_template("/change_number.html", return_message=return_message)
    else:
        return_message = 'something problem'
        return render_template("/change_number.html", return_message=return_message)


@app.route('/change_mail.html', methods=['POST', 'GET'])
def change_mail():
    return render_template('change_mail.html')


@app.route('/change_mail', methods=['POST', 'GET'])
def change_mail_id():
    if request.method == 'POST':
        req = request.form
        userid = session['userid']
        mail = req['mail']
        if not mail.endswith('.com'):
            return_message = 'E-mail_id format is not correct'
            return render_template("/change_mail.html", return_message=return_message)
        elif mail.islower():
            query = text('SELECT email FROM customer_details WHERE email = :email')
            value = [{'email': mail}]
            data = my_cursor.execute(query, value)
            if data.fetchone():
                return_message = 'Email-id already exist'
                return render_template("/change_mail.html", return_message=return_message)
        else:
            return_message = 'E-mail_id should not contain any uppercase letter'
            return render_template("/change_mail.html", return_message=return_message)
        try:
            query = text("UPDATE customer_details SET email = :mail WHERE user_id = :userid")
            value = [{'mail': mail, 'userid': userid}]
            my_cursor.execute(query, value)
            my_cursor.commit()
            return redirect('/update_profile.html')
        except NotImplemented:
            my_cursor.rollback()
            return_message = 'Something problem try again after some time'
            return render_template("/change_mail.html", return_message=return_message)
    else:
        return_message = 'something problem'
        return render_template("/change_mail.html", return_message=return_message)


@app.route('/change_address.html', methods=['POST', 'GET'])
def change_address():
    return render_template('change_address.html')


@app.route('/change_address', methods=['POST', 'GET'])
def change_add():
    if request.method == 'POST':
        req = request.form
        userid = session['userid']
        address = req['address']
        if not address.strip():
            return_message = 'Please fill the address'
            return render_template("/change_address.html", return_message=return_message)
        try:
            query = text("UPDATE customer_details SET address = :address WHERE user_id = :userid")
            value = [{'address': address, 'userid': userid}]
            my_cursor.execute(query, value)
            my_cursor.commit()
            return redirect('/update_profile.html')
        except NotImplemented:
            my_cursor.rollback()
            return_message = 'Something problem try again after some time'
            return render_template("/change_address.html", return_message=return_message)
    else:
        return_message = 'something problem'
        return render_template("/change_address.html", return_message=return_message)


@app.route('/withdraw.html', methods=['POST', 'GET'])
def withdraw():
    return render_template('withdraw.html')


@app.route('/withdraw', methods=['POST', 'GET'])
def draw():
    if request.method == 'POST':
        req = request.form
        userid = session['userid']
        input_amount = req['amount']
        amount = int(input_amount)
        query = text("SELECT opening_balance FROM customer_details WHERE user_id = :userid")
        values = [{'userid': userid}]
        data = my_cursor.execute(query, values)
        acc_balance = data.fetchone()
        balance = int(acc_balance[0])
        update_balance = balance - amount
        if update_balance < 0:
            return_message = 'Insufficient balance'
            return render_template("/withdraw.html", return_message=return_message)
        else:
            query = text("UPDATE customer_details SET opening_balance = :balance WHERE user_id = :userid")
            values = ({'balance': balance, 'userid': userid})
            my_cursor.execute(query, values)
            my_cursor.commit()
            return redirect("/signin.html")


@app.route('/deposit.html', methods=['POST', 'GET'])
def deposit():
    return render_template('deposit.html')


@app.route('/deposit', methods=['POST', 'GET'])
def deposit_amount():
    if request.method == 'POST':
        req = request.form
        userid = session['userid']
        input_amount = req['amount']
        amount = int(input_amount)
        if amount <= 2500:
            query = text("SELECT opening_balance FROM customer_details WHERE user_id = :userid")
            values = [{'userid': userid}]
            data = my_cursor.execute(query, values)
            acc_balance = data.fetchone()
            balance = int(acc_balance[0])
            update_balance = balance + amount
            query = text("UPDATE customer_details SET opening_balance = :balance WHERE user_id = :userid")
            values = [{'userid': userid, 'balance': update_balance}]
            my_cursor.execute(query, values)
            my_cursor.commit()
            return redirect("/signin.html")
        else:
            return_message = 'Max limit of deposit will be 2500-/'
            return render_template("/deposit.html", return_message=return_message)


@app.route('/pin.html', methods=['POST', 'GET'])
def pin():
    return render_template('pin.html')


@app.route('/pin', methods=['POST', 'GET'])
def m_pin():
    if request.method == 'POST':
        req = request.form
        userid = session['userid']
        pin1 = req['pin']
        pin2 = req['m_pin']
        new_pin = int(pin1)
        conform_pin = int(pin2)
        if new_pin == conform_pin:
            query = text("UPDATE customer_details SET pin = :pin WHERE user_id = :userid")
            values = [{'userid': userid, 'pin': pin}]
            my_cursor.execute(query, values)
            my_cursor.commit()
            return redirect("/amount_transfer.html")
        else:
            return_message = 'Entered pin is not match'
            return render_template("/pin.html", return_message=return_message)


@app.route('/logout.html', methods=['POST', 'GET'])
def logout():
    userid = session['userid']
    query = text("SELECT name FROM customer_details WHERE user_id = :userid")
    value = [{'userid': userid}]
    data = my_cursor.execute(query, value)
    username = data.fetchone()
    name = username[0]
    session['userid'] = None
    return render_template('logout.html', name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
