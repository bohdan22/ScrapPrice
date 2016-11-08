from flask import render_template, flash, redirect, session, url_for, request, g
from flaskext.mysql import MySQL
from app import app,db
from flask.ext.admin import Admin, BaseView, expose
from models import User
import glob
from PIL import Image
 
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

page = 1
@app.route("/index/<int:page>",methods = ['POST', 'GET'])
def index(page):
    start = 15
    perpage = page*start
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT a.id , a.laptop , a.price , a.image , a.sale ,"
                   "GROUP_CONCAT(b.price  ORDER BY b.price ASC SEPARATOR ', '), "
                   "GROUP_CONCAT(b.site  ORDER BY b.site ASC SEPARATOR ', '),AVG(b.price),MIN(b.price),MAX(b.price) "
                   "AS data_prices FROM prices a LEFT JOIN data_prices b "
                   "ON a.id = b.price_id GROUP BY a.id  LIMIT %s offset %s;",(start,perpage))
    data = cursor.fetchall()
    print data
    return render_template('index.html', page=page, data=data)

@app.route("/search",methods = ['POST', 'GET'])
def search():
    if request.method == "POST":
        conn = mysql.connect()
        cursor = conn.cursor()
        froms = request.form.get('froms')
        to = request.form.get('to')
        checkbox = request.form.get('check')
        query = "SELECT * FROM prices WHERE 1 "
        if request.form.get('search') != '':
            query += " AND laptop LIKE '%s'" % ('%'+request.form.get('search')+'%')
            print query
        if froms != '' and to != '':
            query += " AND price BETWEEN %s AND %s" % (froms,to)
            print query
        if checkbox == '1':
            query += " AND sale = '1'"
            print query
        cursor.execute(query)
        result = cursor.fetchall()
    return render_template('search.html', result = result)