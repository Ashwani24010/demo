#importing Flask class from the flask package .
from flask import Flask,request,jsonify
import sqlite3 

#initializing an application sever and passing the name of the current module by __name__ .
app = Flask(__name__) 

# $env:FLASK_ENV="development" : - this is used to set the env varible so that we should not start server again
# and again on changes .

#making databse connection 

def db_connection():
    con = None 
    try:
        con = sqlite3.Connection("books.sqlite")
    except sqlite3.Error as e:
        print(e)
    
    return con 



@app.route('/getBooks')
def hello():
    con = db_connection() 
    cursor = con.cursor()

    cursor.execute('select * from products;')

#this is a dynamic route whatever we write after the / it takes it as a route for this endpoint .
#In order to access it we should have declare the variable in the function .
@app.route('/createBook', methods='POST')
def home():
    name = request.form['name'] 
    con = db_connection() 
    cursor = con.cursor()

    query = """create table products (
        name varchar 
    )""" 

    cursor.execute(query)
    cursor.execute(f'insert into products values({name})')



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