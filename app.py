from flask import *
from connection import conn
from crypt import verify_password, hash_password
app =  Flask(__name__)
app.secret_key = 'Ar%*7_Xg4TQOo@#5'



@app.route('/')
def index():
    if 'admin_id' in session:
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('admin_id')
    session.pop('email')
    session.pop('fname')
    session.pop('lname')
    return redirect('/login')


@app.route('/profile')
def profile():
    if 'admin_id' in session:
        sql = 'select * from admin where admin_id = %s'
        cursor = conn().cursor()
        session_key = session['admin_id']
        cursor.execute(sql, (session_key))
        row = cursor.fetchone()
        return render_template('profile.html', row = row)
    else:
        return redirect('/login')



@app.route('/changepassword', methods = ['POST','GET'])
def changepassword():
    if 'admin_id' in session:
        if request.method == 'POST':
            session_key = session['admin_id']
            currentpassword = request.form['currentpassword']
            newpassword = request.form['newpassword']
            confirmpassword = request.form['confirmpassword']

            sql = 'select * from admin where admin_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (session_key))
            if cursor.rowcount ==0:
                return redirect('/logout')
            else:
                row = cursor.fetchone()
                hashedpassword = row[4]
                status = verify_password(hashedpassword, currentpassword)
                if status == True:
                    if newpassword !=confirmpassword:
                        return render_template('changepassword.html', msg='Not Matching - New and Confirm')
                    else:
                        import pymysql
                        con = pymysql.connect(host='localhost', user='root', password='',
                                               database='property')
                        sql ='UPDATE admin SET password = %s where admin_id = %s'
                        cursor = con.cursor()
                        cursor.execute(sql, (hash_password(newpassword), session_key))

                        con.commit()
                        return render_template('changepassword.html', msg = 'Changed.')

                else:
                    return render_template('changepassword.html', msg = 'Current Password Incorrent')

        else:
            return render_template('changepassword.html')

    else:
        return redirect('/login')


@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # check if email exists
        sql = "select * from admin where email = %s"
        cursor = conn().cursor()
        cursor.execute(sql,(email))

        if cursor.rowcount == 0:
            return render_template('login.html', error = 'Email does not exist')
        else:
            row = cursor.fetchone()
            hashed_password = row[4]
            # verify
            status = verify_password(hashed_password, password)
            if status == True:
                # create  sessions
                session['email'] = row[3]
                session['admin_id'] = row[0]
                session['fname'] = row[1]
                session['lname'] = row[2]
                return redirect('/')

            elif status == False:
                return render_template('login.html', error = 'Login Failed')
            else:
                return render_template('login.html', error = 'Something went wrong,')
    else:
        return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)