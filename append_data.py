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
total_users = 10
user_proportions = np.array([0.4, 0.3, 0.2, 0.1])
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Load the data
# ===========================================================================
# Initialize the connection to the database
conn = DBConnection()
conn.create_booking_table()
conn.create_users_dogs_table()

# Initialize the stochastic process class

ins = StochasticPro(total_users=total_users,
                    user_proportions=user_proportions)
ins.initialize_room_dict()
ins.add_reservation_periods()
ins.fill_in_general()
ins.fill_in_cluster()
ins.generate_users()
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Insert into users
# ===========================================================================
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
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Close the connection
# ===========================================================================
conn.close_connection()
# ===========================================================================
