from app.domain import ClientData


class DBPopulator:

    def __init__(self, client_data_dao, user_service):
        self.client_data_dao = client_data_dao
        self.user_service = user_service

    def populate_one_client_data(self):
        name = "test_client"
        password = "test_password"
        auth_token = self.user_service.register_new_user(name, password)
        user = self.user_service.authenticate(auth_token)
        user_id = user.get_user_id()

        initial_data = ["day_of_week", "device_category", "browser", "country"]
        device_categories = ["desktop", "mobile", "tablet"]
        browsers = ['Opera', 'Safari']
        countries = ['Austria', 'Belgium', 'Brazil', 'France', 'Germany', 'India', 'Ireland', 'Latvia', 'Montenegro',
                     'Netherlands', 'Norway', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Slovakia', 'Ukraine',
                     'United Arab Emirates', 'United Kingdom', 'United States']
        impute_dict = {
            "day_of_week": 1.0,
            "device_category": "desktop",
            "browser": "Chrome",
            "country": "Poland"
        }
        client_data = ClientData({
            "initial_data": initial_data,
            "discrete_data": {
                "device_categories": device_categories,
                "browsers": browsers,
                "countries": countries
            },
            "impute_dict": impute_dict
        })
        self.client_data_dao.add_for_user(user_id, client_data)
        return auth_token
