import sqlite3


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # parameters need to be passed in as a tuple (value,)
        result = cursor.execute(query, (username,))

        row = result.fetchone()
        if row:
            user = cls(*row)# we can use #row since row[0] is the id, row[1] is the username and #row[2] is the password
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    # tested with POSTMAN where the Header contains a key: Authorization
    # and a value: JWT <token>
    # <token> is retrieved from /auth where we pass the u/p