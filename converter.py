
class converter:
    def __init__(self):
        self.currencies = {}
    def convert(self, amount, currency_1, currency_2):
        if amount <= 0:
            return "Invalid Amount"
        if currency_1 == currency_2:
            return round(float(amount),4)
        if not self.currencies:
            return "No Currencies Loaded"
        if currency_1 not in self.currencies:
            return f"{currency_1} is not a valid currency"
        if currency_2 not in self.currencies:
            return f"{currency_2} is not a valid currency"

        result = round(float(amount) * self.currencies[currency_1] / self.currencies[currency_2],4)
        return result

