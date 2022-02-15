from flask import Flask, render_template, request, json, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

t_host = "localhost"
t_port = "5432"
t_dbname = "Api_testing"
t_user = "postgres"
t_pw = "root"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

db_conn.autocommit = True


# sql1 = '''CREATE TABLE Countries1 (id int NOT NULL,Country varchar(200),Alpha2_code char(30),Alpha3_code char(30),Numeric_code int,Latitude float,Longitude float);'''

# db_cursor.execute(sql1)
# print("DB created")

@app.route('/import-csv')
def import_csv():
    sql2 = '''copy countries1(id,Country,Alpha2_code,Alpha3_code,Numeric_code,Latitude,Longitude) FROM 'C://countries.csv' DELIMITER ',' CSV HEADER;'''
    db_cursor.execute(sql2)
    print("Successfully Imported CSV")

@app.route('/home')
def home():
    return "Welcome home page"

@app.route('/get-countries', methods = ['GET'])
def get_countries():
    try:
        sql1 = '''Select * from countries1;'''
        db_cursor.execute(sql1)
        country = db_cursor.fetchall()
        countries = []
        for row in country:
            # print(row)
            countries.append(dict(row))
        return jsonify(countries)
    except psycopg2.Error as e:
        return render_template("error.html", t_message = e)
    
@app.route('/get-country/<id>', methods = ['GET'])
def get_countries_by_id(id):
    try:
        query2 = '''Select * from countries1 where id=%s;'''
        db_cursor.execute(query2,(id,))
        country_by_id = db_cursor.fetchone()
        country1 = []

        country1.append(dict(country_by_id))
        return jsonify(country1)
    except psycopg2.Error as e:
        return render_template("error.html", t_message = e)

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)