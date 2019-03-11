# ===========================================================================
# Notes
# ===========================================================================
"""
(*) This class connects to the PostgrSQL dbs
"""
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Imports
# ===========================================================================
import psycopg2
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Construct the class
# ===========================================================================


class DBConnection:

    def __init__(self,
                 host='localhost',
                 database='andpotap',
                 user='andpotap',
                 port='5432'):
        self.connection = psycopg2.connect(host=host,
                                           database=database,
                                           user=user,
                                           port=port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Create the booking table
    # ----------------------------------------------------------------------
    def create_booking_table(self):
        drop = "DROP TABLE IF EXISTS booking"
        booking = """CREATE TABLE booking (
                        date_from date,
                        date_to date,
                        room_id int,
                        client_id int,
                        dog_id int,
                        PRIMARY KEY (date_from, date_to, room_id, dog_id))"""
        self.cursor.execute(query=drop)
        self.cursor.execute(query=booking)
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Create users and dogs tables
    # ----------------------------------------------------------------------
    def create_users_dogs_table(self):
        drop_u = "DROP TABLE IF EXISTS users"
        drop_d = "DROP TABLE IF EXISTS dogs"
        users = """CREATE TABLE users (
                        client_id int,
                        first_name text,
                        last_name text,
                        address text,
                        city text,
                        state text,
                        zipcode text,
                        phone text,
                        birthdate date,
                        PRIMARY KEY (client_id))"""

        dogs = """CREATE TABLE dogs (
                            client_id int,
                            dog_id int,
                            dog_name text,
                            breed text,
                            gender text,
                            color text,
                            d_birthdate date,
                            brand text,
                            PRIMARY KEY (client_id, dog_id))"""
        self.cursor.execute(query=drop_u)
        self.cursor.execute(query=drop_d)
        self.cursor.execute(query=users)
        self.cursor.execute(query=dogs)
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Insert into the booking table
    # ----------------------------------------------------------------------
    def insert_into_booking(self, room_dict, room_id):
        # Pass the values into strings
        room_id = str(room_id)
        date_from = room_dict['date_from']
        date_to = room_dict['date_to']
        client_id = str(room_dict['client_id'])
        dog_id = str(room_dict['dog_id'])

        # Create the command
        tup = "(" + "'" + date_from + "'" + ', ' + "'" + date_to + "'" + \
              ', ' + room_id + ', ' + client_id + ', ' + dog_id + ")"
        insert = "INSERT INTO booking VALUES " + tup

        # Execute
        self.cursor.execute(insert)
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Insert into users
    # ----------------------------------------------------------------------
    def insert_into_users(self, user_dict, user_id):
        # Pass the values into strings
        rubrics = ['first_name', 'last_name', 'address',
                   'city', 'state', 'zipcode', 'phone',
                   'birthdate']

        # Create the values
        tup = self.generate_tuple(content=user_dict[user_id],
                                  rubrics=rubrics,
                                  idx=[user_id])

        # Create the command
        insert = "INSERT INTO users VALUES " + tup

        # Execute
        self.cursor.execute(insert)
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Insert into dogs
    # ----------------------------------------------------------------------
    def insert_into_dogs(self, dog_dict, dog_id):
        # Pass the values into strings
        rubrics = ['dog_name', 'breed', 'gender', 'color',
                   'd_birthdate', 'brand']

        # Create the values
        tup = self.generate_tuple(content=dog_dict[dog_id],
                                  rubrics=rubrics,
                                  idx=[dog_id, dog_id])

        # Create the command
        insert = "INSERT INTO dogs VALUES " + tup

        # Execute
        self.cursor.execute(insert)
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Close the connection
    # ----------------------------------------------------------------------
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Create insertion tuple
    # ----------------------------------------------------------------------
    @staticmethod
    def generate_tuple(content, rubrics, idx):
        tup = "("
        for i in range(len(idx)):
            tup += str(idx[i]) + ', '

        tup = tup[:-2]
        for rub in rubrics:
            a = content[rub]
            a = "'" + a + "'"
            tup += ', ' + a

        tup += ")"
        return tup
    # ----------------------------------------------------------------------
# ===========================================================================
