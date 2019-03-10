# ===========================================================================
# Notes
# ===========================================================================
"""
(*) This class generates the data for the rooms in Happy Day Hotel
"""
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Imports
# ===========================================================================
import numpy as np
import datetime
# ===========================================================================
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ===========================================================================
# Construct the class StochasticPro
# ===========================================================================


class StochasticPro:

    def __init__(self, seed=42):
        self.room_process = {}
        np.random.seed(seed=seed)
        self.room_description = {}
        self.room_type = {1: {'params': (7, 1), 'success': 0.7},
                          2: {'params': (10, 10), 'success': 0.6},
                          3: {'params': (12, 20), 'success': 0.5}}
        self.sim_n = 1000
        self.months = {6: {'boost': 0.3},
                       7: {'boost': 0.4},
                       8: {'boost': 0.3},
                       11: {'boost': 0.5},
                       12: {'boost': 1}}

        self.general_dict = {}
        self.cluster_dict = {}

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Initialize the dictionary of rooms
    # ----------------------------------------------------------------------
    def initialize_room_dict(self, limits=(9, 17), total=20):
        for i in range(total):
            if i <= limits[0]:
                self.room_description.update({i: {'type': 1}})
            elif i <= limits[1]:
                self.room_description.update({i: {'type': 2}})
            else:
                self.room_description.update({i: {'type': 3}})
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Add blocks
    # ----------------------------------------------------------------------
    def add_reservation_periods(self):
        for k in self.room_description.keys():
            t = self.room_description[k]['type']
            mu = self.room_type[t]['params'][0]
            r = self.room_type[t]['params'][1]
            success = self.room_type[t]['success']
            p = r / (mu + r)
            sims = np.random.negative_binomial(n=r, p=p, size=self.sim_n)
            stop = (np.cumsum(sims) < 365) & (sims > 0)
            sub_sims = sims[stop]
            process_list = []
            start_date = datetime.date(2018, 1, 1)
            m = sub_sims.shape[0]
            for i in range(m):
                days = int(sub_sims[i])
                period = datetime.timedelta(days=days)
                end_date = start_date + period
                used = self.used_or_not(success=success,
                                        month=start_date.month)
                process_dict = {'date_from': start_date.isoformat(),
                                'date_to': end_date.isoformat(),
                                'duration': days,
                                'used': used,
                                'client_id': -1,
                                'dog_id': -1}
                process_list.append(process_dict)
                start_date = end_date

            self.room_process.update({k: process_list})
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Determine month usability
    # ----------------------------------------------------------------------
    def used_or_not(self, success, month):
        selected_months = [month for month in self.months.keys()]
        if month in selected_months:
            a = success + self.months[month]['boost']
            b = 1.0
            p = np.min(np.array([a, b]))
            return int(np.random.binomial(n=1, p=p, size=1))
        else:
            return int(np.random.binomial(n=1, p=success, size=1))
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Generate general lists
    # ----------------------------------------------------------------------
    def fill_in_general(self):
        self.general_dict = {
            'first_name': ['Michael', 'David', 'John', 'Robert', 'James',
                           'William', 'Richard', 'Christopher', 'Peter',
                           'Ted', 'Lisa', 'Mary', 'Maria', 'Susan', 'Karen',
                           'Patricia', 'Linda', 'Donna', 'Sophia', 'Anna'],
            'last_name': ['Smith', 'Johnson', 'Jones', 'Brown', 'Miller',
                          'Wilson', 'Moore', 'Cooper', 'Carter', 'Perez',
                          'Garcia', 'Lee', 'Lewis', 'Evans', 'Diaz',
                          'Butler', 'Flores', 'Long', 'Powell', 'Ross',
                          'Gray', 'Ramirez', 'Turner', 'Adams', 'King',
                          'Collins', 'Sanders', 'Kelly', 'Froning',
                          'Murphy', 'Xi', 'Chi', 'Pi', 'Tensor'],
            'address': ['170 W 96th ST', '145 E 39th ST', '207 12th Ave',
                        '214 E 10th ST', '1433 Bedford Ave', '60 Grand ST',
                        '181 E 111th ST', '81 E 45th ST', '65th 4th Ave',
                        '99 Gansevoort ST', '529 Broome ST',
                        '287 Hudson ST'],
            'phone': ['212-866-8000', '212-865-5700', '212-989-6363',
                      '212-777-7018', '347-305-3233', '718-285-6180',
                      '212-828-3647', '646-747-0801', '212-388-0088',
                      '212-570-3670', '917-639-3089', '646-666-5096'],
            'color': ['white', 'black', 'tan', 'grey', 'brindle'],
            'dog_name': [('Bella', 'F'), ('Lucy', 'F'), ('Daisy', 'F'),
                         ('Luna', 'F'), ('Sadie', 'F'), ('Molly', 'F'),
                         ('Kiki', 'F'), ('Lili', 'F'), ('Bootie', 'F'),
                         ('Max', 'M'), ('Charlie', 'F'), ('Tucker', 'M'),
                         ('Buddy', 'M'), ('Oliver', 'M'), ('Bear', 'M'),
                         ('Duke', 'M'), ('Dog', 'M'), ('Tupac', 'M')],
            'country': ['US'],
            'csz': [('Queens', 'NY', '11433'), ('Bronx', 'NY', '10701'),
                    ('Bronx', 'NY', '10461'), ('Brooklyn', 'NY', '11216'),
                    ('Stamford', 'CT', '06901'), ('NYC', 'NYC', '10027'),
                    ('Hoboken', 'NJ', '07030'), ('Jersey City', 'NJ', '07302'),
                    ('Long Island', 'NY', '11101'), ('Staten Island', 'NY', '10306'),
                    ('Brooklyn', 'NY', '11249'), ('NYC', 'NY', '10024'),
                    ('NYC', 'NY', '10014'), ('NYC', 'NY', '10009'),
                    ('Brooklyn', 'NY', '11201'), ('NYC', 'NY', '10014'),
                    ('NYC', 'NY', '10012'), ('NYC', 'NY', '10013')]}

    def fill_in_cluster(self):
        self.cluster_dict = {
            1: {'prob': 0.25,
                'breeds': ['Pug', 'Chihuahua', 'Bulldog', 'Pitbull',
                           'Border Terrier', 'Pomeranian', 'Maltese'],
                'dog_age': (8, 5 ** 2),
                'brands': ['Eukanuba', 'Purina', 'WholeHearted']},
            2: {'prob': 0.5,
                'breeds': ['Labrador', 'Pug', 'Pitbull',
                           'German Shepherd', 'Beagle',
                           'Rottweiler', 'Chow chow'],
                'dog_age': (8, 1 ** 2),
                'brands': ['WholeHearted', 'Hills',
                           'Acana', 'Instinct']},
            3: {'prob': 0.65,
                'breeds': ['Husky', 'Boxer', 'Bull terrier',
                           'Malinois', 'Golden', 'Irish terrier',
                           'Dalmatian', 'Pitbull', 'Pug'],
                'dog_age': (7, 5 ** 2),
                'brands': ['Royal Canin', 'WholeHearted', 'Hills',
                           'Acana', 'Instinct']},
            4: {'prob': 0.85,
                'breeds': ['Doberman', 'Shiba Inu', 'Malinois',
                           'Cane Corso', 'Bloodhound', 'Salukis',
                           'Dogo Argentino', 'Bulldog'],
                'dog_age': (10, 2 ** 2),
                'brands': ['Raw Diet', 'WholeHearted', 'Orijen', 'Hills']}}
    # ----------------------------------------------------------------------

# ===========================================================================
