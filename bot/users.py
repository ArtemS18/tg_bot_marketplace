class User:
    def __init__(self):
        self.data_user = {}

    def get_user_data(self, user_id):
        if user_id not in self.data_user:
            self.create_data(user_id)
        return self.data_user[user_id]

    def create_data(self, user_id):
        if user_id not in self.data_user:
            self.data_user[user_id] = {
                'prev_state':'START',
                'id':0,
                'page':0,
                'filters':{
                    'min_price_filter':0,
                    'max_price_filter':None,
                    'order_by':'id',
                    'order_direction':'ASC'#'DESC'
                }
            }
    def get_prev_state(self, user_id):
        return self.get_user_data(user_id)['prev_state']

    def set_data(self, user_id, key, value):
        self.get_user_data(user_id)[key] = value

    def set_data_filters(self, user_id, key, value):
        self.get_user_data(user_id)['filters'][key] = value

    def get_data_filters(self, user_id):
        return self.get_user_data(user_id)['filters']

    def set_id(self, user_id, id_value):
        self.get_user_data(user_id)['id'] = id_value

    def set_prev_state(self, user_id, prev_state):
        self.get_user_data(user_id)['prev_state'] = prev_state
