class InitialModelFeatures:

    # MGR: TODO: Make this class generic
    def __init__(self, impute_dict, initial_data, discrete_data):
        for key in initial_data.keys():
            if initial_data[key] is None:
                initial_data[key] = impute_dict[key]

        self.initial_data = initial_data

        self.device_categories = discrete_data["device_categories"]
        self.browsers = discrete_data["browsers"]
        self.countries = discrete_data["countries"]

    def to_dict(self):
        return self.initial_data

    def get_model_input(self):
        model_input = {}
        model_input["day_of_week"] = [self.initial_data["day_of_week"]]

        for device_category in self.device_categories:
            model_input["device_category_" + device_category] = [self.__device_category_binary(device_category)]

        for browser in self.browsers:
            model_input["browser_" + browser] = [self.__browser_binary(browser)]

        model_input["country_(not set)"] = [float(0)]
        for country in self.countries:
            model_input["country_" + country] = [self.__country_binary(country)]

        return model_input

    def __device_category_binary(self, device_category):
        if self.initial_data["device_category"] == device_category:
            return float(1)
        else:
            return float(0)

    def __browser_binary(self, browser):
        if self.initial_data["browser"] == browser:
            return float(1)
        else:
            return float(0)

    def __country_binary(self, country):
        if self.initial_data["country"] == country:
            return float(1)
        else:
            return float(0)
