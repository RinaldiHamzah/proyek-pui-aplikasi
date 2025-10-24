from flask_mysqldb import MySQL
from flask_app import app

mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_sentimen'

mysql.init_app(app)

class MySQLDB:
    def __init__(self):
        pass

    def select_data(self):
        with app.app_context():
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            data = cursor.fetchall()
            return data