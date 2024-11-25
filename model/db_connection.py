from configuration.config import get_config
import mysql.connector

def get_connection():
    '''
        Gets the database connection
    '''
    return mysql.connector.connect(**get_config("db_config"))

