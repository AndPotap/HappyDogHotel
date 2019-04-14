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
                 password='',
                 host='localhost',
                 database='andpotap',
                 user='andpotap',
                 port='5432',
                 instance=False):
        if instance:
            host = 'w4111.cisxo09blonu.us-east-1.rds.amazonaws.com'
            database = 'w4111'
            user = 'ap3635'
            password = password
            self.connection = psycopg2.connect(host=host,
                                               database=database,
                                               user=user,
                                               password=password)
        else:
            self.connection = psycopg2.connect(host=host,
                                               database=database,
                                               user=user,
                                               port=port)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Drop all the tables!
    # ----------------------------------------------------------------------
    def drop_all(self):
        drops = ["assigned", "bookings", "employees",
                 "rooms", "users", "dogs"]
        for drop in drops:
            query = "DROP TABLE IF EXISTS " + drop
            self.cursor.execute(query=query)
    # ----------------------------------------------------------------------
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Create tables
    # ----------------------------------------------------------------------
    def create_all(self):
        self.create_users_dogs_table()
        self.create_rooms_table()
        self.create_bookings_table()
        self.create_employees_table()
        self.create_assigned_table()

    def create_users_dogs_table(self):
        users = """CREATE TABLE users (
                        client_id int,
                        first_name text,
                        last_name text,
                        address text,
                        city text,
                        state text,
                        zipcode text,
                        country text,
                        phone text,
                        birthdate date,
                        password text,
                        PRIMARY KEY (client_id))"""

        dogs = """CREATE TABLE dogs (
                            client_id int,
                            dog_id int UNIQUE,
                            dog_name text,
                            breed text,
                            gender text,
                            color text,
                            d_birthdate date,
                            brand text,
                            PRIMARY KEY (client_id, dog_id))"""
        self.cursor.execute(query=users)
        self.cursor.execute(query=dogs)

    def create_rooms_table(self):
        rooms = """CREATE TABLE rooms (
                        room_id int,
                        room_type int,
                        price float,
                        PRIMARY KEY (room_id))"""
        self.cursor.execute(query=rooms)

    def create_bookings_table(self):
        bookings = """CREATE TABLE bookings (
                        date_from date,
                        date_to date,
                        room_id int,
                        client_id int NOT NULL,
                        dog_id int,
                        FOREIGN KEY (room_id) REFERENCES rooms (room_id),
                        FOREIGN KEY (client_id, dog_id) 
                            REFERENCES dogs (client_id, dog_id),
                        PRIMARY KEY (date_from, date_to, room_id, dog_id)
                        )"""
        self.cursor.execute(query=bookings)

    def create_employees_table(self):
        employees = """CREATE TABLE employees (
                        employee_id int,
                        first_name text,
                        last_name text,
                        address text,
                        city text,
                        state text,
                        zipcode text,
                        country text,
                        phone text,
                        hired_date date,
                        PRIMARY KEY (employee_id))"""
        self.cursor.execute(query=employees)

    def create_assigned_table(self):
        assigned = """CREATE TABLE assigned (
                        employee_id int,
                        dog_id int,
                        date_from date,
                        date_to date,
                        FOREIGN KEY (employee_id) 
                            REFERENCES employees(employee_id),
                        FOREIGN KEY (dog_id) REFERENCES dogs(dog_id),
                        PRIMARY KEY (employee_id, dog_id, 
                                     date_to, date_from))"""
        self.cursor.execute(query=assigned)
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Table insertions
    # ----------------------------------------------------------------------
    def insert_into_rooms(self, room_dict, room_id):
        # Pass the rubrics
        rubrics = ['type', 'price']

        # Create the values
        tup = self.generate_tuple(content=room_dict[room_id],
                                  rubrics=rubrics,
                                  idx=[room_id],
                                  room=True)

        # Create the command
        insert = "INSERT INTO rooms VALUES " + tup

        # Execute
        self.cursor.execute(insert)

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
        insert = "INSERT INTO bookings VALUES " + tup

        # Execute
        self.cursor.execute(insert)

    def insert_into_assigned(self, room_dict, idx):
        # Pass the values into strings
        rubrics = ['date_from', 'date_to']

        # Create the values
        tup = self.generate_tuple(content=room_dict,
                                  rubrics=rubrics,
                                  idx=idx)

        # Create the command
        insert = "INSERT INTO assigned VALUES " + tup

        # Execute
        self.cursor.execute(insert)

    def insert_into_employees(self, employee_dict, employee_id):
        # Pass the values into strings
        rubrics = ['first_name', 'last_name', 'address',
                   'city', 'state', 'zipcode', 'country', 'phone',
                   'hired_date']

        # Create the values
        tup = self.generate_tuple(content=employee_dict[employee_id],
                                  rubrics=rubrics,
                                  idx=[employee_id])

        # Create the command
        insert = "INSERT INTO employees VALUES " + tup

        # Execute
        self.cursor.execute(insert)

    def insert_into_users(self, user_dict, user_id):
        user_dict[user_id].update({'client_id': user_id,
                                   'password': '123'})
        # TODO: pass the password creation to the stochastic class

        self.cursor.execute(
            """
            INSERT INTO users VALUES 
            (%(client_id)s, %(first_name)s, %(last_name)s, %(address)s, 
            %(city)s, %(state)s, %(zipcode)s, %(country)s, 
            %(phone)s, %(birthdate)s, %(password)s);
            """,
            user_dict[user_id])

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
    # Utils
    # ----------------------------------------------------------------------
    @staticmethod
    def generate_tuple(content, rubrics, idx, room=False):
        tup = "("
        for i in range(len(idx)):
            tup += str(idx[i]) + ', '

        tup = tup[:-2]
        for rub in rubrics:
            a = content[rub]
            if room:
                a = str(a)
            else:
                a = "'" + a + "'"
            tup += ', ' + a

        tup += ")"
        return tup
    # ----------------------------------------------------------------------
# ===========================================================================
