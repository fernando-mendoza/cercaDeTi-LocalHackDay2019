from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'edificios'
mysql = MySQL(app)


app.secret_key = "mysecretkey"


@app.route('/')
def Index1():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM edificios')
    data = cur.fetchall()
    cur.close()
    return render_template('/index.html', contacts = data)


@app.route('/admin')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM edificios')
    data = cur.fetchall()
    cur.close()
    return render_template('/admin/index.html', contacts = data)

@app.route('/add_place', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO inscripciones (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('Edifico Agregado Correctamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM inscripciones WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE inscripciones
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Edificio Actualizado Correctamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM inscripciones WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Edificio eliminado correctamente')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
