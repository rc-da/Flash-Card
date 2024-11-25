from mysql.connector import Error
from model.db_connection import get_connection
from datetime import datetime

class Progress:

    @staticmethod
    def update_progress(card_id, rating, reminder):
        
        query = "UPDATE progress SET rating = %s, reminder = %s WHERE card_id = %s"
        
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (rating, reminder, card_id))
            con.commit()
            
            if cursor.rowcount > 0:
                return {"message": "Progress updated successfully!", "status": "success"}
            else:
                return {"message": "No changes made to the progress.", "status": "failed"}
        
        except Exception as e:
            print("Error updating progress:", e)
            return {"message": "Error updating progress!", "status": "failed"}
        
        finally:
            cursor.close()
            con.close()


    @staticmethod
    def get_reminder(card_id):
        query = "SELECT reminder FROM progress WHERE card_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (card_id,))
            result = cursor.fetchone()
            if result:
                return {"message": "Fetching reminder successful!", "status": "success", "reminder": result[0]}
        except Error:
            return {"message": "Error fetching reminder!", "status": "failed"}
        finally:
            cursor.close()
            con.close()
        return {"message": "Fetching reminder failed!", "status": "failed"}

    @staticmethod
    def delete_progress(card_id):
        query = "DELETE FROM progress WHERE card_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (card_id,))
            con.commit()
            if cursor.rowcount > 0:
                print("done")
                return {"message": "Progress deleted successfully!", "status": "success"}
        except Error:
            print("error deleting progress")
            return {"message": "Error deleting progress!", "status": "failed"}
        finally:
            cursor.close()
            con.close()
        print("not done")
        return {"message": "Deleting progress failed!", "status": "failed"}

    @staticmethod
    def delete_all_progress(user_id):
        query = "DELETE FROM progress WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_id,))
            con.commit()
            if cursor.rowcount > 0:
                return {"message": "All progress deleted successfully!", "status": "success"}
            return {"message": "No records found!", "status": "success"}
        except Error:
            return {"message": "Error deleting all progress!", "status": "failed"}
        finally:
            cursor.close()
            con.close()

    @staticmethod
    def get_progress(card_id):
        query = "SELECT * FROM progress WHERE card_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, (card_id,))
            progress = cursor.fetchone()
            if progress:
                return {"message": "Fetching progress successful!", "status": "success", "progress": progress}
        except Error:
            print("error in progress when getting it")
            return {"message": "Error fetching progress!", "status": "failed"}
        finally:
            cursor.close()
            con.close()
        return {"message": "Fetching progress failed!", "status": "failed"}

    @staticmethod
    def create_progress(card_id, user_id):
        query = "INSERT INTO progress (card_id, user_id) VALUES (%s, %s)"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (card_id, user_id))
            con.commit()
            if cursor.lastrowid:
                return {"message": "Progress created successfully!", "status": "success", "progress_id": cursor.lastrowid}
        except Error:
            return {"message": "Error creating progress!", "status": "failed"}
        finally:
            cursor.close()
            con.close()
        return {"message": "Creating progress failed!", "status": "failed"}
