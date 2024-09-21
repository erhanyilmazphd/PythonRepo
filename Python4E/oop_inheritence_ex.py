class PartyAnimal:
    def __init__(self, an_name):
        self.x = 0
        self.name = an_name
        print(self.name, "Constructed.")
    def party(self):
        self.x = self.x + 1
        print(self.name, "So far", self.x)

class FootballFan(PartyAnimal):
    def __init__(self, an_name):
        super().__init__(an_name)
        self.points = 0
    def touchdown(self):
        self.points = self.points + 7
        self.party()
        print(self.name, "points", self.points)


s = PartyAnimal("Sally")
s.party()

j = FootballFan("Joy")
j.party()
j.touchdown()