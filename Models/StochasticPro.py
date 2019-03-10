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

# ===========================================================================
