class Points:
    def __init__(self, value, date, category):
        self.value = value
        self.date = date
        self.category = category

    def get_value(self):
        return self.value

    def get_date(self):
        return self.date

    def get_category(self):
        return self.category

    def set_value(self, value):
        self.value = value

    def set_date(self, date):
        self.date = date

    def set_category(self, category):
        self.category = category