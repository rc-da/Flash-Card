from mysql.connector import Error
from model.db_connection import get_connection

class User_Profile:
    '''
        Allow us to do crud operation in users table
    '''

    # Read
    @staticmethod
    def get_user(id) -> dict:
        ''' 
            Fetches user info from users table  
            Parameter (id)
            Returns a dictionary with a status, message, user(dict)
        '''

        query = "SELECT * FROM users WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor(dictionary=True)
            cursor.execute(query, (id,))
            user = cursor.fetchone()
            return {
                "message" : "User fetch successful!",
                "status" : "success",
                "user" : user
            }
        except Error as e:
            print(f"Error occured while fetching user error:\n{e}")

        finally:
            cursor.close()
            con.close()
        return {
            "message" : "User fetch failed!",
            "status" : "success"
        }
    
    # Read
    @staticmethod
    def check_new_user(user_mail) ->bool:
        '''
            Check whether the new user exists in the users
            Parameter (user_mail)
            Returns boolean
        '''

        query = "SELECT * FROM users WHERE user_mail = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_mail,))
            if cursor.fetchone():
                return False
            
            return True
            
        except Error as e:
            print(f"Error occured while checking user error:\n{e}")
            return True

        finally:
            cursor.close()
            con.close()
        

    # Create
    @staticmethod
    def create_user(name, email, password) -> dict:
        '''
            Adds user to users 
            Parameters (name, email, password)
            Returns a dictionary with a message and status.
        '''
        
        if not User_Profile.check_new_user(email):
            return {
                "message": "User already exists!",
                "status": "failed"
            }

        query = """
            INSERT INTO users (user_name, user_mail, user_password) 
            VALUES (%s, %s, %s)
        """

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (name, email, password))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message": "User signup Successful!",
                    "status": "success"
                }
            
            
            return {
                "message": "User signup failed!",
                "status": "failed"
            }

        except Error as e:
            print(f"Error occurred while adding user: {e}")
            return {
                "message": "Error signing up!",
                "status": "failed"
            }

        finally:
                cursor.close()
                con.close()

    # Delete  
    @staticmethod 
    def delete_user(user_mail) -> dict:
        '''
            Deletes the user from the users table
            Parameter (user_mail)
            Returns a dictionary with a message, status
        '''

        if User_Profile.check_new_user(user_mail):
            return {
                "message" : "User doesn't exist!",
                "status" : "failed"
            }
        

        query = "DELETE FROM users WHERE user_mail = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_mail,)) 
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "User deletion Successful!",
                    "status" : "success"
                }

        except Error as e:
            print(f"Error occured while deleting user error:\n{e}")
            return {
                "message" : "Error Deleting User!",
                "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()

        return {
                "message" : "User deletion failed!",
                "status" : "failed"
            }
    
    # Update
    @staticmethod
    def update_user(user_id, name, mail, password) -> dict:
        '''
            Updates user details in users table
            Parameters (user_id, name, mail, password)
            Returns a dictionary with a message, status
        '''

        query = "UPDATE users SET user_name = %s, user_mail = %s, user_password = %s WHERE user_id = %s"
        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (name, mail, password, user_id))
            con.commit()

            if cursor.rowcount > 0:
                return {
                    "message" : "User updation successful!",
                    "status" : "success"
                }
        
        except Error as e:
            print(f"Error while updating user details: {e}")
            return {
            "message" : "Error updating user!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()
            
        return {
            "message" : "User updation failed!",
            "status" : "failed"
        }
    
    # Read
    @staticmethod
    def authenticate_user(user_mail, password) -> dict:
        '''
            Authenticates user
            Parameter (user_mail, password)
            Returns a dictionary witha message, status, user_name, user_id
        '''

        new_user = User_Profile.check_new_user(user_mail)

        if new_user:
            return {
                "message" : "User Doesn't Exist in the System!",
                "status" : "failed"
                }
        
        query = "SELECT user_id, user_name FROM users WHERE user_mail = %s and user_password = %s"

        try:
            con = get_connection()
            cursor = con.cursor()
            cursor.execute(query, (user_mail, password))
            aunthenticated = cursor.fetchone()

            if aunthenticated:
                return {
                    "message" : "Login successful!",
                    "status" : "success",
                    "user_id" : aunthenticated[0],
                    "user_name" : aunthenticated[1]
                    }
            
        except Error as e:
            print(f"Error occured when authenticating the User error is \n{e}")
            return {
            "message" : "Error authenticating user!",
            "status" : "failed"
            }

        finally:
            cursor.close()
            con.close()
        
        return {
        "message" : "Wrong Password!",
        "status" : "failed"
        }
