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
        # conn = "dbname='andpotap' user='andpotap' host='localhost' port='5432'"
        # self.connection = psycopg2.connect(conn)
        self.connection = psycopg2.connect(host=host,
                                           database=database,
                                           user=user,
                                           port=port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

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

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
# ===========================================================================
