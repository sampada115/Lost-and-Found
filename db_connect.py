import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",        
        user="root",             
        password="Sampada_1104", 
        database="lost_and_found"
    )
    return connection
