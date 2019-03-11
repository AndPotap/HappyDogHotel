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

    def __init__(self, total_users, user_proportions, seed=42):
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
        self.total_users = total_users
        self.user_proportions = user_proportions
        self.user_clusters = {}
        self.users = {}
        self.dogs = {}

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Determine who-when
    # ----------------------------------------------------------------------
    def determine_who_when(self):
        for k, values in self.room_process.items():
            room_type = self.room_description[k]['type']
            for v in values:
                duration = v['duration']

                p = self.determine_p(room_type=room_type,
                                     duration=duration)

                m = self.user_proportions.shape[0]
                cluster = np.random.choice(a=m,
                                           size=1,
                                           p=p)
                cluster = cluster + 1
                user, dog = self.tell_user_dog(cluster=cluster[0])
                v['client_id'] = user
                v['dog_id'] = dog
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Tell user and dog
    # ----------------------------------------------------------------------
    def tell_user_dog(self, cluster):
        users = self.user_clusters[cluster]
        users_n = len(users)
        idx = np.random.choice(a=users_n, size=1)[0]
        user = int(users[idx])
        return user, user
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Determine cluster probabilities
    # ----------------------------------------------------------------------
    @staticmethod
    def determine_p(room_type, duration):
        if room_type == 3:
            p = np.array([0., 0., 0.1, 0.9])
        elif (room_type == 2) and (duration > 15):
            p = np.array([0., 0.5, 0.3, 0.2])
        elif (room_type == 2) and (duration <= 15):
            p = np.array([0.5, 0.3, 0.1, 0.1])
        elif (room_type == 1) and (duration > 20):
            p = np.array([0., 0.4, 0.4, 0.2])
        else:
            p = np.array([0.7, 0.2, 0.1, 0.])
        return p
    # ----------------------------------------------------------------------

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

        self.initialize_room_dict()

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
    # Generate users
    # ----------------------------------------------------------------------
    def generate_users(self):

        self.fill_in_general()
        self.fill_in_cluster()

        user_n = self.user_proportions.shape[0]
        user_types = np.random.choice(a=user_n,
                                      size=self.total_users,
                                      replace=True,
                                      p=self.user_proportions)
        user_types = user_types + 1
        for r in range(user_n):
            aux = list(np.where(user_types == r + 1)[0])
            self.user_clusters.update({r + 1: aux})

        # Append the placeholders
        for i in range(self.total_users):
            update = {i: {'first_name': '',
                          'last_name': '',
                          'address': '',
                          'city': '',
                          'state': '',
                          'zipcode': '',
                          'country': '',
                          'phone': '',
                          'birthdate': ''}}
            update_2 = {i: {'dog_name': '',
                            'breed': '',
                            'gender': '',
                            'color': '',
                            'd_birthdate': '',
                            'brand': ''}}
            self.users.update(update)
            self.dogs.update(update_2)

        # Input the general information
        self.input_general()

        # Input the cluster information
        for j in range(user_n):
            aux = self.user_clusters[j + 1]
            self.input_cluster(cluster=j + 1, user_list=aux)
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Inputs the general information
    # ----------------------------------------------------------------------
    def input_general(self):
        for k in self.general_dict.keys():
            if k == 'csz':
                for i in range(self.total_users):
                    self.users[i]['country'] = 'US'

            elif k == 'dog_name':
                working = self.general_dict[k]
                working_n = len(working)
                sample = np.random.choice(a=working_n,
                                          size=self.total_users)
                for i in range(self.total_users):
                    name_gender = working[sample[i]]
                    self.dogs[i]['dog_name'] = name_gender[0]
                    self.dogs[i]['gender'] = name_gender[1]
            elif k == 'color':
                working = self.general_dict[k]
                working_n = len(working)
                sample = np.random.choice(a=working_n,
                                          size=self.total_users)
                for i in range(self.total_users):
                    color = working[sample[i]]
                    self.dogs[i]['color'] = color
            else:
                working = self.general_dict[k]
                working_n = len(working)
                sample = np.random.choice(a=working_n,
                                          size=self.total_users)
                for i in range(self.total_users):
                    self.users[i][k] = working[sample[i]]
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Input the specifics
    # ----------------------------------------------------------------------
    def input_cluster(self, cluster, user_list):
        # Load-off the specific cluster variables
        prob = self.cluster_dict[cluster]['prob']
        breeds = self.cluster_dict[cluster]['breeds']
        dog_age = self.cluster_dict[cluster]['dog_age']
        age = self.cluster_dict[cluster]['age']
        brands = self.cluster_dict[cluster]['brands']
        user_n = len(user_list)
        csz = self.general_dict['csz']
        csz_n = len(csz)

        # Generate the samples
        sample_breeds = np.random.choice(a=len(breeds),
                                         size=user_n)
        sample_brands = np.random.choice(a=len(brands),
                                         size=user_n)

        # Sample the ages and correct
        sample_dog_ages = np.random.normal(loc=dog_age[0],
                                           scale=dog_age[1],
                                           size=user_n)
        mask = sample_dog_ages <= 0
        sample_dog_ages[mask] = 0.05

        sample_ages = np.random.normal(loc=age[0],
                                       scale=age[1],
                                       size=user_n)
        mask = sample_ages <= 0
        sample_ages[mask] = np.abs(sample_ages[mask])

        sample_csz = np.random.binomial(n=csz_n,
                                        p=prob,
                                        size=user_n)
        sample_csz = sample_csz - 1

        for i in range(user_n):
            user_id = user_list[i]
            dog_id = user_list[i]
            csz_i = csz[sample_csz[i]]
            self.users[user_id]['city'] = csz_i[0]
            self.users[user_id]['state'] = csz_i[1]
            self.users[user_id]['zipcode'] = csz_i[2]
            self.dogs[dog_id]['breed'] = breeds[sample_breeds[i]]
            self.dogs[dog_id]['brand'] = brands[sample_brands[i]]
            today = datetime.date(2019, 1, 1)
            days = int(round((365 * sample_dog_ages[i])))
            birth = today - datetime.timedelta(days=days)
            self.dogs[dog_id]['d_birthdate'] = birth.isoformat()

            days = int(round((365 * sample_ages[i])))
            birth = today - datetime.timedelta(days=days)
            self.users[user_id]['birthdate'] = birth.isoformat()
    # ----------------------------------------------------------------------

    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # ----------------------------------------------------------------------
    # Generate general lists
    # ----------------------------------------------------------------------
    def fill_in_general(self):
        self.general_dict = {
            'first_name': ['Michael', 'David', 'John', 'Robert', 'James',
                           'William', 'Richard', 'Christopher', 'Peter',
                           'Ted', 'Lisa', 'Mary', 'Maria', 'Susan',
                           'Karen', 'Patricia',
                           'Linda', 'Donna', 'Sophia', 'Anna'],
            'last_name': ['Smith', 'Johnson', 'Jones', 'Brown', 'Miller',
                          'Wilson', 'Moore', 'Cooper', 'Carter', 'Perez',
                          'Garcia', 'Lee', 'Lewis', 'Evans', 'Diaz',
                          'Butler', 'Flores', 'Long', 'Powell', 'Ross',
                          'Gray', 'Ramirez', 'Turner', 'Adams', 'King',
                          'Collins', 'Sanders', 'Kelly', 'Froning',
                          'Murphy', 'Xi', 'Chi', 'Pi', 'Tensor'],
            'address': ['170 W 96th ST', '145 E 39th ST', '207 12th Ave',
                        '214 E 10th ST', '1433 Bedford Ave',
                        '60 Grand ST', '181 E 111th ST',
                        '81 E 45th ST', '65th 4th Ave',
                        '99 Gansevoort ST', '529 Broome ST',
                        '287 Hudson ST'],
            'phone': ['212-866-8000', '212-865-5700', '212-989-6363',
                      '212-777-7018', '347-305-3233', '718-285-6180',
                      '212-828-3647', '646-747-0801', '212-388-0088',
                      '212-570-3670', '917-639-3089', '646-666-5096'],
            'color': ['White', 'Black', 'Tan', 'Grey', 'Brindle'],
            'dog_name': [('Bella', 'F'), ('Lucy', 'F'), ('Daisy', 'F'),
                         ('Luna', 'F'), ('Sadie', 'F'), ('Molly', 'F'),
                         ('Kiki', 'F'), ('Lili', 'F'), ('Bootie', 'F'),
                         ('Max', 'M'), ('Charlie', 'F'),
                         ('Tucker', 'M'), ('Chloe', 'F'),
                         ('Buster', 'M'), ('Maggie', 'F'),
                         ('Lucky', 'M'), ('Abby', 'F'),
                         ('Oscar', 'M'), ('Gracie', 'F'),
                         ('Winston', 'M'), ('Angel', 'F'),
                         ('Sam', 'M'), ('Ruby', 'F'),
                         ('Buddy', 'M'), ('Oliver', 'M'),
                         ('Bear', 'M'), ('Rosie', 'F'),
                         ('Duke', 'M'), ('Dog', 'M'), ('Tupac', 'M')],
            'csz': [('Queens', 'NY', '11433'),
                    ('Bronx', 'NY', '10701'),
                    ('Bronx', 'NY', '10461'),
                    ('Brooklyn', 'NY', '11216'),
                    ('Stamford', 'CT', '06901'), ('NYC', 'NY', '10027'),
                    ('Hoboken', 'NJ', '07030'),
                    ('Jersey City', 'NJ', '07302'),
                    ('Long Island', 'NY', '11101'),
                    ('Staten Island', 'NY', '10306'),
                    ('Brooklyn', 'NY', '11249'), ('NYC', 'NY', '10024'),
                    ('NYC', 'NY', '10014'), ('NYC', 'NY', '10009'),
                    ('Brooklyn', 'NY', '11201'), ('NYC', 'NY', '10014'),
                    ('NYC', 'NY', '10012'), ('NYC', 'NY', '10013')]}

    def fill_in_cluster(self):
        self.cluster_dict = {
            1: {'prob': 0.25,
                'breeds': ['Pug', 'Chihuahua', 'Bulldog', 'Pitbull',
                           'Border Terrier', 'Pomeranian', 'Maltese',
                           'Poodles', 'Pointers', 'Schnauzers',
                           'Shih Tzu'],
                'dog_age': (8, 5),
                'age': (25, 5),
                'brands': ['Eukanuba', 'Purina', 'WholeHearted']},
            2: {'prob': 0.5,
                'breeds': ['Labrador', 'Pug', 'Pitbull',
                           'German Shepherd', 'Beagle',
                           'Rottweiler', 'Chow chow', 'Corgi',
                           'Australian Shepherds', 'Shar Pei'],
                'dog_age': (8, 1),
                'age': (40, 5),
                'brands': ['WholeHearted', 'Hills',
                           'Acana', 'Instinct']},
            3: {'prob': 0.65,
                'breeds': ['Husky', 'Boxer', 'Bull terrier',
                           'Malinois', 'Golden', 'Irish terrier',
                           'Dalmatian', 'Pitbull', 'Pug', 'Bergamasco',
                           'St Bernard', 'Malamute', 'Dachshunds',
                           'Great Dane'],
                'dog_age': (7, 5),
                'age': (50, 10),
                'brands': ['Royal Canin', 'WholeHearted', 'Hills',
                           'Acana', 'Instinct']},
            4: {'prob': 0.85,
                'breeds': ['Doberman', 'Shiba Inu', 'Malinois',
                           'Cane Corso', 'Bloodhound', 'Salukis',
                           'Dogo Argentino', 'Catalburun',
                           'Xoloitzcuintli', 'Tibetian Mastiff',
                           'Presa Canario', 'Afghan Hound'],
                'dog_age': (10, 2),
                'age': (40, 10),
                'brands': ['Raw Diet', 'WholeHearted', 'Orijen', 'Hills']}}
    # ----------------------------------------------------------------------

# ===========================================================================
