class Medicine:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class MedicalShop:
    def __init__(self):
        self.inventory = []

    def add_medicine(self, name, quantity):
        self.inventory.append(Medicine(name, quantity))

    def update_quantity(self, name, quantity):
        for med in self.inventory:
            if med.name == name:
                med.quantity += quantity
                return True
        return False

    def regularly_sold(self):
        return [med.name for med in self.inventory if med.quantity > 10]

    def not_sold(self):
        return [med.name for med in self.inventory if med.quantity == 0]

    def medium_sold(self):
        return [med.name for med in self.inventory if 0 < med.quantity <= 10]


pharmacy = MedicalShop()
pharmacy.add_medicine("Paracetamol", 20)
pharmacy.add_medicine("Amoxicillin", 5)
pharmacy.add_medicine("Ibuprofen", 0)

print("Regularly Sold Medicines:", pharmacy.regularly_sold())
print("Not Sold Medicines:", pharmacy.not_sold())
print("Medium Sold Medicines:", pharmacy.medium_sold())