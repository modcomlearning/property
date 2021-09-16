from flask import *
from connection import conn
from crypt import verify_password, hash_password
from test import password_generator
app =  Flask(__name__)
app.secret_key = 'Ar%*7_Xg4TQOo@#5'
import pymysql
con = pymysql.connect(host='localhost', user='root', password='',
                                               database='property')


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




@app.route('/addagency', methods = ['POST','GET'])
def addagency():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        tel_office = request.form['tel_office']
        tel_personal = request.form['tel_personal']
        company_name = request.form['company_name']
        password = password_generator()
        admin_id = session['admin_id']
        cursor = con.cursor()
        # check if phone exists
        sql0 = 'select * from agency where tel_personal = %s'
        cursor.execute(sql0, (tel_personal))
        if cursor.rowcount > 0:
            flash('Personal Phone already in use','warning')
            return render_template('addagency.html')
        else:
            sql = "insert into agency(fname, lname, email, password, tel_office, tel_personal,company_name,admin_id)  values(%s, %s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(sql, (fname, lname, email, hash_password(password), tel_office,
                                         tel_personal, company_name, admin_id))
                con.commit()
                # send sms
                flash('Agency Add successful','info')
                from sms import sending
                sending(tel_personal, password, fname)
                return render_template('addagency.html')

            except:
                 flash('Failed', 'danger')
                 return render_template('addagency.html')



    else:
        return render_template('addagency.html')





@app.route('/search_agencies', methods = ['POST','GET'])
def search_agencies():
    if request.method == 'POST':
        email = request.form['email']
        sql = 'select * from agency where email = %s'
        cursor = conn().cursor()
        cursor.execute(sql, (email))
        # check if no agency found
        if cursor.rowcount == 0:
            return render_template('search_agencies.html', msg='No Records')
        else:
            rows = cursor.fetchall()
            return render_template('search_agencies.html', rows=rows)

    else:
        sql = 'select * from agency order by reg_date DESC'
        cursor = conn().cursor()
        cursor.execute(sql)
        # check if no agency found
        if cursor.rowcount == 0:
            return render_template('search_agencies.html', msg = 'No Records')
        else:
            rows = cursor.fetchall()
            return render_template('search_agencies.html', rows = rows)



@app.route('/delete_agency/<agency_id>')
def delete_agency(agency_id):
    sql = 'delete from agency where agency_id = %s'
    cursor = con.cursor()
    cursor.execute(sql,(agency_id))
    con.commit()
    flash('Deleted successful', 'info')
    return redirect('/search_agencies')








if __name__ == '__main__':
    app.run(debug=True)