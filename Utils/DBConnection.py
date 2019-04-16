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
import numpy as np
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
                        email text,
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
        room_dict[room_id].update({'room_id': room_id})
        self.cursor.execute(
            """
            INSERT INTO rooms VALUES
            (%(room_id)s, %(type)s, %(price)s)
            """, room_dict[room_id])

    def insert_into_booking(self, room_dict, room_id):
        room_dict.update({'room_id': room_id})
        self.cursor.execute(
            """
            INSERT INTO bookings VALUES 
            (%(date_from)s, %(date_to)s, %(room_id)s, %(client_id)s, %(dog_id)s)
            """, room_dict)

    def insert_booking_from_form(self, form):
        client_id = self.find_client_id_from_email_and_password(email=form.email.data,
                                                                password=form.password.data)
        dog_id = self.find_dog_id_by_name_and_owner(client_id=client_id,
                                                    dog_name=form.dog_name.data)
        room_id = self.allocate_room_based_on_type(room_type=form.room_type.data)
        employee_id = self.allocate_to_employee()
        booking = {'date_from': form.date_from.data,
                   'date_to': form.date_to.data,
                   'room_id': room_id,
                   'client_id': client_id,
                   'dog_id': dog_id}
        assigned = {'date_from': form.date_from.data,
                    'date_to': form.date_to.data,
                    'employee_id': employee_id,
                    'dog_id': dog_id}
        self.cursor.execute(
            """
            INSERT INTO bookings VALUES 
            (%(date_from)s, %(date_to)s, %(room_id)s, %(client_id)s, %(dog_id)s)
            """, booking)
        self.cursor.execute(
            """
            INSERT INTO assigned VALUES 
            (%(employee_id)s, %(dog_id)s, %(date_from)s, %(date_to)s)
            """, assigned)

    def insert_into_assigned(self, room_dict):
        self.cursor.execute(
            """
            INSERT INTO assigned VALUES
            (%(employee_id)s, %(dog_id)s, %(date_from)s, %(date_to)s)
            """, room_dict)

    def insert_into_employees(self, employee_dict, employee_id):
        employee_dict[employee_id].update({'employee_id': employee_id})
        self.cursor.execute(
            """
            INSERT INTO employees VALUES 
            (%(employee_id)s, %(first_name)s, %(last_name)s, %(address)s, 
            %(city)s, %(state)s, %(zipcode)s, %(country)s, 
            %(phone)s, %(hired_date)s)
            """, employee_dict[employee_id])

    def insert_employee_from_form(self, form):
        self.cursor.execute(
            """
            SELECT MAX(employee_id)
            FROM employees
        """)
        employee_id = self.cursor.fetchone()[0] + 1
        employee_dict = {'first_name': form.first_name.data,
                         'last_name': form.last_name.data,
                         'address': form.address.data,
                         'city': form.city.data,
                         'state': form.state.data,
                         'zipcode': form.zipcode.data,
                         'country': 'US',
                         'phone': form.phone.data,
                         'hired_date': form.hired_date.data,
                         'employee_id': employee_id}
        self.cursor.execute(
            """
            INSERT INTO employees VALUES 
            (%(employee_id)s, %(first_name)s, %(last_name)s, %(address)s, 
            %(city)s, %(state)s, %(zipcode)s, %(country)s, 
            %(phone)s, %(hired_date)s)
            """, employee_dict)

    def insert_into_users(self, user_dict, user_id):
        user_dict[user_id].update({'client_id': user_id})

        self.cursor.execute(
            """
            INSERT INTO users VALUES 
            (%(client_id)s, %(first_name)s, %(last_name)s, %(address)s, 
            %(city)s, %(state)s, %(zipcode)s, %(country)s, 
            %(phone)s, %(birthdate)s, %(email)s, %(password)s);
            """,
            user_dict[user_id])

    def insert_into_users_from_form(self, form):
        self.cursor.execute(
            """
            SELECT MAX(client_id)
            FROM users
        """)
        client_id = self.cursor.fetchone()[0] + 1
        user_dict = {'first_name': form.first_name.data,
                     'last_name': form.last_name.data,
                     'address': form.address.data,
                     'city': form.city.data,
                     'state': form.state.data,
                     'zipcode': form.zipcode.data,
                     'country': 'US',
                     'phone': form.phone.data,
                     'birthdate': form.birth_date.data,
                     'email': form.email.data,
                     'password': form.password.data,
                     'client_id': client_id}
        self.cursor.execute(
            """
            INSERT INTO users VALUES 
            (%(client_id)s, %(first_name)s, %(last_name)s, %(address)s, 
            %(city)s, %(state)s, %(zipcode)s, %(country)s, 
            %(phone)s, %(birthdate)s, %(email)s, %(password)s);
            """, user_dict)

    def insert_into_dogs(self, dog_dict, dog_id):
        dog_dict[dog_id].update({'dog_id': dog_id, 'client_id': dog_id})
        self.cursor.execute(
            """
            INSERT INTO dogs VALUES 
            (%(client_id)s, %(dog_id)s, %(dog_name)s, %(breed)s, 
            %(gender)s, %(color)s, %(d_birthdate)s, %(brand)s);
            """, dog_dict[dog_id])

    def insert_into_dogs_from_form(self, form):
        # Update the dog id
        self.cursor.execute(
            """
            SELECT MAX(dog_id)
            FROM dogs
        """)
        dog_id = self.cursor.fetchone()[0] + 1

        # Find dog owner
        self.cursor.execute(
            """
            SELECT client_id
            FROM users
            WHERE users.email = %s AND users.password = %s
            """, (form.email.data, form.password.data))
        client_id = self.cursor.fetchone()[0]
        dog_dict = {'dog_name': str(form.dog_name.data).capitalize(),
                    'breed': str(form.breed.data).capitalize(),
                    'gender': str(form.gender.data).capitalize(),
                    'color': str(form.color.data).capitalize(),
                    'd_birthdate': form.birth_date.data,
                    'brand': str(form.brand.data).capitalize(),
                    'dog_id': dog_id,
                    'client_id': client_id}
        self.cursor.execute(
            """
            INSERT INTO dogs VALUES 
            (%(client_id)s, %(dog_id)s, %(dog_name)s, %(breed)s, 
            %(gender)s, %(color)s, %(d_birthdate)s, %(brand)s);
            """, dog_dict)
    # ----------------------------------------------------------------------
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Table updates
    # ----------------------------------------------------------------------

    def update_room_type_price_with_form(self, form):
        room_type = form.room_type.data
        room_new_price = form.room_price.data
        self.cursor.execute(
            """
            UPDATE rooms
            SET price = %s
            WHERE room_type = %s
            """, (room_new_price, room_type))
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
    def find_client_id_from_email_and_password(self, email: str, password: str):
        self.cursor.execute(
            """
            SELECT client_id
            FROM users
            WHERE email = %s AND password = %s
            """, (email, password))
        client_id = self.cursor.fetchone()[0]
        return client_id

    def find_dog_id_by_name_and_owner(self, client_id: int, dog_name: str):
        self.cursor.execute(
            """
            SELECT dog_id
            FROM dogs
            WHERE client_id = %s AND dog_name = %s
            """, (client_id, dog_name))
        dog_id = self.cursor.fetchone()[0]
        return dog_id

    def allocate_to_employee(self) -> int:
        self.cursor.execute(
            """
            SELECT MAX(employee_id)
            FROM employees
            """)
        max_number = self.cursor.fetchone()[0]
        sample_employee = np.random.choice(a=max_number, size=1)
        return int(sample_employee)

    def allocate_room_based_on_type(self, room_type: int):
        # TODO: define the logic for allocating rooms
        self.cursor.execute(
            """
            SELECT room_id
            FROM rooms
            WHERE room_type = %s
            """, (room_type,))
        room_id = self.cursor.fetchone()[0]
        return room_id
    # ----------------------------------------------------------------------
# ===========================================================================
