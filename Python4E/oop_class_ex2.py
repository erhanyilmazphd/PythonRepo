class PartyAnimal:
    def __init__(self, an_name):
        self.x = 0
        self.name = an_name
        print(self.name, "Constructed.")
    def party(self):
        self.x = self.x + 1
        print(self.name, "So far", self.x)
    def __del__(self):
        print(self.name, "Destructed.", "x ", self.x)


s = PartyAnimal("Sally")
j = PartyAnimal("Joy")

j.party()
s.party()
j.party()