from mysql.connector import Error
from model.db_connection import get_connection
from datetime import datetime, timedelta

class Card:
    '''
        Allow us to do crud operation in cards table
    '''

    # Read
    @staticmethod
    def get_card(id) -> dict:

        query = "SELECT * FROM cards WHERE card_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, (id,))
            card = cursor.fetchone()
            return {
                "message" : "Card fetch successful!",
                "status" : "success",
                "card" : card
            }
        except Error as e:
            print(f"Error occured while fetching card error:\n{e}")

        finally:
            cursor.close()
            con.close()
        return {
            "message" : "Card fetch failed!",
            "status" : "success"
        }
    

        

    # Create
    @staticmethod
    def create_card(user_id, category_id, front, back ) -> dict:

        query = """
            INSERT INTO cards (user_id, category_id, card_front, card_back) 
            VALUES (%s, %s, %s, %s)
        """

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_id, category_id, front, back))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message": "Card creation Successful!",
                    "status": "success"
                }
            
            
            return {
                "message": "Card creation failed!",
                "status": "failed"
            }

        except Error as e:
            print(f"Error occurred while creating card: {e}")
            return {
                "message": "Error creating card!",
                "status": "failed"
            }

        finally:
                cursor.close()
                con.close()

    # Delete  
    @staticmethod 
    def delete_card(card_id) -> dict:

        query = "DELETE FROM cards WHERE card_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (card_id,)) 
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "Card deletion Successful!",
                    "status" : "success"
                }

        except Error as e:
            print(f"Error occured while deleting Card error:\n{e}")
            return {
                "message" : "Error Deleting Card!",
                "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
                "message" : "Card deletion failed!",
                "status" : "failed"
            }
    # Delete  
    @staticmethod 
    def delete_all_card(user_id) -> dict:

        query = "DELETE FROM cards WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_id,)) 
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "All Card deletion Successful!",
                    "status" : "success"
                }
            return {
                "message" : "No records!",
                "status" : "success"
            }

        except Error as e:
            print(f"Error occured while deleting All Card error:\n{e}")
            return {
                "message" : "Error Deleting All Card!",
                "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        
    
    # Update
    @staticmethod
    def update_card(category_id, front, back, card_id) -> dict:
        query = "UPDATE cards SET category_id = %s, card_front = %s, card_back = %s WHERE card_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, ( category_id, front, back, card_id))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "Card updation successful!",
                    "status" : "success"
                }
        
        except Error as e:
            print(f"Error while updating Card details: {e}")
            return {
            "message" : "Error updating card!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()
            
        return {
            "message" : "Card updation failed!",
            "status" : "failed"
        }
    
    # Read  
    @staticmethod
    def fetch_all_card(user_id) -> dict:
        query = "SELECT * FROM cards WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True, buffered=True) 
            cursor.execute(query, (user_id,))
            cards = cursor.fetchall()

            if cards:
                return {
                    "message": "All Card fetch Successful!",
                    "status": "success",
                    "cards": cards,
                }
            return {
                "message": "No records!",
                "status": "success",
                "cards": {},
            }

        except Error as e:
            print(f"Error occurred while fetching All Cards:\n{e}")
            return {
                "message": "Error Fetching All Cards!",
                "status": "failed",
                "cards": {},
            }

        finally:
                cursor.close()
                con.close()

    # Read  
    @staticmethod
    def fetch_all_unread(user_id) -> dict:

        current_datetime_ist = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')

        query = "SELECT * FROM cards WHERE user_id = %s AND card_id in (SELECT card_id FROM progress WHERE reminder < %s )"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True, buffered=True) 
            cursor.execute(query, (user_id,current_datetime_ist))
            cards = cursor.fetchall()

            if cards:
                return {
                    "message": "All Card fetch Successful!",
                    "status": "success",
                    "cards": cards,
                }
            return {
                "message": "No records!",
                "status": "success",
                "cards": {},
            }

        except Error as e:
            print(f"Error occurred while fetching All Cards:\n{e}")
            return {
                "message": "Error Fetching All Cards!",
                "status": "failed",
                "cards": {},
            }

        finally:
                cursor.close()
                con.close()
    