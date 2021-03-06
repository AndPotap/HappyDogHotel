# ===========================================================================
# Notes
# ===========================================================================
"""
(*) This script appends the data generated from the Stochastic Process
    into the PostgreSQL data base
"""
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Imports
# ===========================================================================
import numpy as np
from Models.StochasticPro import StochasticPro
from Utils.DBConnection import DBConnection
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Set parameters
# ===========================================================================
total_users = 250
user_proportions = np.array([0.4, 0.3, 0.2, 0.1])
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Load the data
# ===========================================================================
# Initialize the connection to the database
run_on_instance = input('Run on instance?')
if run_on_instance == 'yes':
    password_db = input('Provide Password')
    instance = True
    conn = DBConnection(instance=instance, password=password_db)
else:
    instance = False
    conn = DBConnection()
conn.drop_all()
conn.create_all()

# Initialize the stochastic process class

ins = StochasticPro(total_users=total_users,
                    user_proportions=user_proportions)
ins.add_reservation_periods()
ins.generate_users()
ins.generate_employees()
ins.determine_who_when()
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Insert into tables
# ===========================================================================
for j in ins.employees.keys():
    conn.insert_into_employees(employee_dict=ins.employees, employee_id=j)

for r in ins.room_description.keys():
    conn.insert_into_rooms(room_dict=ins.room_description, room_id=r)

for i in ins.users.keys():
    conn.insert_into_users(user_dict=ins.users, user_id=i)
    conn.insert_into_dogs(dog_dict=ins.dogs, dog_id=i)
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Append the data into the database
# ===========================================================================
for k in ins.room_process.keys():
    for i in range(len(ins.room_process[k])):
        room_dict = ins.room_process[k][i]
        if room_dict['used'] == 1:
            conn.insert_into_booking(room_dict=room_dict, room_id=k)
            dog_id = room_dict['dog_id']
            employee_id = room_dict['employee_id']
            conn.insert_into_assigned(room_dict=room_dict)
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Check queries for form
# ===========================================================================
print(conn.allocate_room_based_on_type(room_type=2, date_from='2018-04-01'))
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Close the connection
# ===========================================================================
conn.close_connection()
# ===========================================================================
