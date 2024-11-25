from model.db_connection import get_connection
from mysql.connector import Error
class Category:
    '''
        R opertation on category table
    '''
    @staticmethod
    def fetch_all_category():
        query = "SELECT * FROM category"

        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query)
            category = cursor.fetchall()
            if category:
                return {
                    "status" : "success",
                    "message" : "All Category fetch successful",
                    "category" : category
                }
            return {
                "status" : "failed",
                "message" : "No Records in the table",
                "category" : {}
            }
        
        except Error as e:
            print(f"Error occured when Fetching all Category error : ", e)
            return {
                "status" : "failed",
                "message" : "Error occured when fetching all Category"
            }
        
        finally:
            con.close()
            cursor.close()

        
    @staticmethod
    def fetch_category(id):
        query = "SELECT * FROM category WHERE category_id = %s"

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (id,))
            category = cursor.fetchone()
            if category:
                return {
                    "status" : "success",
                    "message" : "Category fetch successful",
                    "category" : category
                }
            return {
                "status" : "failed",
                "message" : "No Records in the table"
            }
        
        except Error as e:
            print(f"Error occured when Fetching Category error : ", e)
            return {
                "status" : "failed",
                "message" : "Error occured when fetching Category"
            }
        
        finally:
            con.close()
            cursor.close()
