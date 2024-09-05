#importing Flask class from the flask package .
from flask import Flask,request,jsonify
import sqlite3 
import psycopg2

#initializing an application sever and passing the name of the current module by __name__ .
app = Flask(__name__)  

# $env:FLASK_ENV="development" : - this is used to set the env varible so that we should not start server again
# and again on changes .

#making databse connection 

def db_connection():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="root",
        host="localhost" , port="5432"
    )

    return con 


@app.route("/",methods = ['GET'])
def create():
    con = db_connection() 

    if con is None :
        return "Connection established"

    cur = con.cursor() 


    try :
        query = """ CREATE TABLE IF NOT EXISTS products (id int PRIMARY KEY, price int);"""
        
        cur.execute(query=query) 
        print(cur) 
    except Exception as e:
        print(e) 

    con.commit() 
    if cur is not None :
        return "Table is created " 
    else :
        return "Table not created" 


@app.route('/getProducts')
def hello():
    con = db_connection() 
    cursor = con.cursor()

    cursor.execute('select * from products;')

    books = [
        dict(id=row[0] ,price = row[1])
        for row in cursor.fetchall()
    ]

    # books = cursor.fetchall() 

    if books is not None :
        return jsonify(books)


#this is a dynamic route whatever we write after the / it takes it as a route for this endpoint .
#In order to access it we should have declare the variable in the function .
@app.route('/createProduct', methods=['POST'])
def home():

    con = db_connection()  

    prod_id = request.form['id'] 
    prod_price = request.form['price']
    

    if con is None :
        print("Connection not established ")

    cursor = con.cursor() 
    data = (prod_id,prod_price)
    cursor.execute('insert into products (id,price) values(%s,%s);',data) 
    
    con.commit()

    return f"Books with the id:{cursor.lastrowid} crreated successfully" 



if(__name__ == '__main__'):
    app.run(debug=True)  
    # here degub = true will on debug mode in and it run two process inside it i.e reloader and debugger .
    #Reloader : - it wataches over all the files in the app and as changes detected it reloads the server .
    #debugger :- this is basically used for the debbuging process , once an error comes then it shows the error 
    #stack tree which is helpful, in error handling .

# Command line options of flask : 

# flask --help : - it will provide all the option and command and description of flask .
# flask shell :- this command is used to run python shell in order to testing works .
# --host : - this is helpful to see what network interface we are using to interact with client , we can procide IP address to listen on particular IP .
# flask run --reload : - use to on the reload mode in changes .