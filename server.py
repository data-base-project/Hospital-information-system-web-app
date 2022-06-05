from datetime import date
import email
from werkzeug.utils import secure_filename
import os
import mysql.connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
from random import randint
import random
import string
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="2560065belal",
    database="project"
)
session=""
mycursor = mydb.cursor()

app = Flask(__name__)

session = ""
@app.route('/' , methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        p_username= request.form['p_username']
        p_email = request.form ['p_email']
        p_phone = request.form ['p_phone']
        message= request.form ['message']
        print(p_username)
        print(p_email)
        print(p_phone)

        sql='INSERT INTO contactus (p_username , p_email , p_phone , message) VAlUES (%s,%s,%s,%s)'
        val=(p_username, p_email , p_phone , message)
        mycursor.execute(sql , val)
        mydb.commit()
        return render_template('index.html')
    else:
        return render_template('index.html')


# log in page
@app.route('/sign in', methods=['POST', 'GET'])
def signin():
    if request.method=='POST':
        uname = request.form ['uname']
        psw= request.form['psw']
        mycursor.execute( 'SELECT id from users where username= %s and p_word=%s ',(uname, psw,))
        account = mycursor.fetchone()
        if account :
            global session
            session=''.join(account)
            mycursor.execute ('SELECT category FROM users where username=%s ',(uname,))
            category= mycursor.fetchone()
            if category==('p',):
                return render_template('W_patient.html')
            elif category==('d',):
                return render_template('W_doctor.html')
            elif category ==('a',):
                return render_template('W_admin.html')
        else: 
            return render_template('sign in.html', msg="account not found ")
    else:     
        return render_template('sign in.html')
    
#admin page {
@app.route('/adddoctor', methods =['POST','GET'])
def adddoctor():
    if request.method == 'POST':
        length = 3
        id = ''.join(random.sample(string.ascii_letters+string.digits, length))
        category = "d"
        f_name = request.form['f_name']
        m_name = request.form['m_name']
        l_name = request.form['l_name']
        username = request.form['username']
        age = request.form['age']
        phone = request.form['phone']
        gender = "Male"
        D_birth = request.form['date']
        email = request.form['email']
        p_word = request.form['p_word']
        psw = request.form['psw-repeat']
        if p_word != psw:
            return render_template('adddoctor.html', msg="pass word doesn't match , please resign")
        else:
            mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = mycursor.fetchone()
            if user:    
                return render_template('adddoctor.html', msg="username already exist")
            else:
                mycursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                em = mycursor.fetchone()
                if em:
                    return render_template('adddoctor.html', msg="email already exist")
                else:
                    sql = "INSERT INTO users (id ,f_name,m_name ,l_name , username, age , phone , gender , D_birth, email , p_word , category) VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (category+id, f_name, m_name, l_name, username,age, phone, gender, D_birth, email, p_word, category)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return render_template('W_admin.html')
    else:
        return render_template('adddoctor.html')


@app.route('/W_admin', methods =['POST','GET'])
def W_adddmin():
    return render_template('W_admin.html')


@app.route('/a_viewappoin', methods =['POST','GET'])
def a_viewappoin():
    if request.method == 'POST':
        appointment_id= request.form ['appointment_id']
        mycursor.execute ("DELETE FROM appointment WHERE appointment_id = %s", (appointment_id,))
        mydb.commit()
        return render_template ('W_admin.html')
    else:
        mycursor.execute('SELECT * FROM appointment')
        result = mycursor.fetchall()
        return render_template('a_viewappoin.html',data=result)



@app.route('/a_viewpatient', methods =['POST','GET'])
def a_viewpatient():
    if request.method == 'POST':
        patient_id= request.form ['patient_id']
        mycursor.execute ("DELETE FROM users WHERE id = %s", (patient_id,))
        mydb.commit()
        return render_template ('W_admin.html')
    else:
        mycursor.execute('SELECT * FROM users where category="p" ')
        result = mycursor.fetchall()
        return render_template('a_viewpatient.html',data=result)

@app.route('/a_viewdoctor', methods =['POST','GET'])
def a_viewdoctor():
    if request.method == 'POST':
        doctor_id= request.form ['doctor_id']
        mycursor.execute ("DELETE FROM users WHERE id = %s", (doctor_id,))
        mydb.commit()
        return render_template ('W_admin.html')
    else:
        mycursor.execute('SELECT * FROM users where category="d" ')
        result = mycursor.fetchall()
        return render_template('a_viewdoctor.html',data=result)
    
@app.route('/a_viewprescription', methods =['POST','GET'])
def a_viewprescription():
    if request.method == 'POST':
        prescription_id= request.form ['prescription_id']
        mycursor.execute ("DELETE FROM followup WHERE examination_id = %s", (prescription_id,))
        mydb.commit()
        return render_template ('W_admin.html')
    else:
        mycursor.execute('SELECT * FROM followup ')
        result = mycursor.fetchall()
        return render_template('a_viewprescription.html',data=result)

@app.route('/contactform', methods =['POST','GET'])
def contactform():
    if request.method == 'POST':
        contact_id= request.form ['contact_id']
        mycursor.execute ("DELETE FROM contactus WHERE incdecies = %s", (contact_id,))
        mydb.commit()
        return render_template ('W_admin.html')
    else:
        mycursor.execute('SELECT * FROM contactus  ')
        result = mycursor.fetchall()
        return render_template('contactform.html',data=result)
    
#}
# patient Page {
@app.route('/W_patient', methods =['POST','GET'])
def W_patient():
    return render_template('W_patient.html')


@app.route('/bookappointment', methods =['POST','GET'])
def bookappointment():
    
    sql = "SELECT users.id, users.f_name  from users where category='d' and id not in ( SELECT \
        users.id  AS user \
        FROM users \
        JOIN appointment ON id = doctor_id \
        where category='d')"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    if data :
        if request.method=='POST':
            patient_id= session
            doctor_name = request.form['doctorname']
            address = request.form['address']
            appointment_date = request.form['date']
            p_description = request.form['message']
            doctorid= request.form['doctorid']
            sql = "INSERT INTO appointment (patient_id ,doctor_id , doctor_name , address , p_description , appointment_date )VALUES(%s,%s,%s,%s,%s,%s)"
            val=(patient_id  ,doctorid , doctor_name , address, p_description , appointment_date )
            mycursor.execute(sql ,val)
            mydb.commit()
            return render_template('W_patient.html')
        else:
            return render_template('bookappointment.html',data=data)
    else:
        return render_template('bookappointment.html',msg = "No Avaliable Doctors")
        

@app.route('/appointment', methods =['POST','GET'])
def appointment():
    if request.method == 'POST':
        appointmentid= request.form ['appointmentid']
        mycursor.execute ("DELETE FROM appointment WHERE appointment_id = %s", (appointmentid,))
        mydb.commit()
        result= mycursor.fetchall()
        return render_template ('W_patient.html')
    else :
        sql = "SELECT \
        appointment.appointment_id , users.f_name , appointment.doctor_name , appointment.address , users.phone, appointment.appointment_date, appointment.p_description AS user \
        FROM users \
        JOIN appointment ON id = patient_id \
        where patient_id=%s"
        val=(session,)
        mycursor.execute(sql, val)
        myresult= mycursor.fetchall()
        return render_template ('appointment.html',data=myresult)



@app.route('/prescription1', methods =['POST','GET'])
def prescription():
    if request.method == 'POST':
        examination_id= request.form ['examination_id']
        mycursor.execute ("DELETE FROM followup WHERE examination_id= %s", (examination_id,))
        mydb.commit()
        result= mycursor.fetchall()
        return render_template ('W_patient.html')
    else :
        mycursor.execute("SELECT * FROM followup where patient_id=%s",(session,))
        result= mycursor.fetchall()
        return render_template ('prescription1.html',data=result)

# }

#doctor pages{
@app.route('/W_doctor', methods=['POST', 'GET'])
def W_doctor():

    return render_template('W_doctor.html')   
    
    
    
@app.route('/view scan', methods=['POST', 'GET'])
def viewscan():
    if request.method == 'POST':
        patient_id=request.form['patient_id']
        doctor_id= session
        print (patient_id)
        print (doctor_id)
        mycursor.execute('SELECT doctor_name FROM followup where doctor_id=%s and patient_id=%s',(doctor_id,patient_id,))
        photo_n=mycursor.fetchone()
        if photo_n :
            image = ""
            image=''.join(photo_n)
            print(type(image))
            print(image)
            return render_template('view scan.html',photo = image)
        else:
            return render_template('view scan.html', msg="No Scans exist")
    else :
        return render_template('view scan.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    mycursor.execute('SELECT  patient_name, patient_id FROM followup WHERE doctor_id=%s',(session,))
    data = mycursor.fetchall()
    if request.method== "POST":
        patient_id=request.form['patient_id']
        f = request.files['photo']
        f.save(os.path.join(secure_filename(f.filename)))
        # print("true")
        scan_photo = f.filename
        print (scan_photo)
        sql= ("update followup set doctor_name =%s where doctor_id=%s and patient_id=%s")
        val=(scan_photo ,session , patient_id )
        mycursor.execute(sql,val)
        mydb.commit()
        return render_template('W_doctor.html')
    else:
        return render_template('upload.html', data=data)


@app.route('/examination', methods=['POST','GET'])
def examination():
    sql = "SELECT \
        users.f_name , users.id  AS user \
        FROM users \
        JOIN appointment ON id = patient_id \
        where doctor_id=%s"
    val=(session,)
    mycursor.execute(sql, val)
    # myresult= mycursor.fetchall()
    # mycursor.execute('SELECT patient_id, patient_name FROM appointment WHERE doctor_id=%s',(session,))
    data = mycursor.fetchall()
    if request.method =='POST':
        doctor_id=session
        patient_id=request.form['patient_id']
        patient_name=request.form['patient_name']
        examination_date=request.form['examination_date']
        d_diagnosis=request.form['d_diagnosis']
        d_prescription=request.form['d_prescription']
        sql1="INSERT INTO followup (doctor_id , patient_id , patient_name , examination_date , d_diagnosis , d_prescription)VALUES (%s,%s,%s,%s,%s,%s)"
        val1=(doctor_id,patient_id,patient_name,examination_date,d_diagnosis,d_prescription)
        mycursor.execute(sql1,val1)
        mycursor.execute ("DELETE FROM appointment WHERE patient_id = %s", (patient_id,))
        mydb.commit()
        return render_template('W_doctor.html')
    else :
        
        return render_template('examination.html',data=data)


@app.route('/my patients', methods=['POST', 'GET'])
def mypatients():
    if request.method == 'POST':
        mycursor.execute('Select * from followup where doctor_id = %s ',(session ,))
        result= mycursor.fetchall()
        if result:
            return render_template('my patients.html', data =result)
        else:
            return render_template('my patients.html', msg="you have no patients with this username")

    else:
        return render_template('my patients.html')

@app.route('/doctorappoin', methods =['POST','GET'])
def doctorappoin():
    if request.method == 'POST':
        appointmentid= request.form ['appointmentid']
        mycursor.execute ("DELETE FROM appointment WHERE appointment_id = %s", (appointmentid,))
        mydb.commit()
        return render_template ('W_doctor.html')
    else:
        # sql = "SELECT \
        # appointment.appointment_id , appointment_name , appointment.doctor_name , appointment.address , users.phone, appointment.appointment_date, appointment.p_description AS user \
        # FROM followup \
        # JOIN appointment ON patient_id = patient_id \
        # where doctor_id=%s  and patient_id not in(select patient_id from followup) "
        # val=(session,)
        # mycursor.execute(sql, val)
        # myresult= mycursor.fetchall()
        mycursor.execute("SELECT * FROM appointment where doctor_id=%s",(session,))
        result= mycursor.fetchall()
        # if  result:
        #     return render_template ('doctorappoin.html', data = result)
        # else:
        return render_template ('doctorappoin.html', data= result)


@app.route('/sign up', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        length = 3
        id = ''.join(random.sample(string.ascii_letters+string.digits, length))
        category = "p"
        f_name = request.form['f_name']
        m_name = request.form['m_name']
        l_name = request.form['l_name']
        username = request.form['username']
        age = request.form['age']
        phone = request.form['phone']
        gender = request.form['gender']
        D_birth = request.form['date']
        email = request.form['email']
        p_word = request.form['p_word']
        psw = request.form['psw-repeat']
        if p_word != psw:
            return render_template('sign up.html', msg="pass word doesn't match , please resign")
        else:
            mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = mycursor.fetchone()
            if user:    
                return render_template('sign up.html', msg="username already exist")
            else:
                mycursor.execute('SELECT * FROM users WHERE email = %s', (email,))
                em = mycursor.fetchone()
                if em:
                    return render_template('sign up.html', msg="email already exist")
                else:
                    sql = "INSERT INTO users (id ,f_name,m_name ,l_name , username, age , phone , gender , D_birth, email , p_word , category) VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (category+id, f_name, m_name, l_name, username,age, phone, gender, D_birth, email, p_word, category)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return render_template('sign in.html')
    else:
        
        return render_template('sign up.html')


if __name__ == '__main__':
    app.run()
