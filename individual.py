class Individual:                   #Birey nesnesi, her bir bireyin 0-1 lerden oluşan valueleri ve fitnessleri vardır
    def set_value(self,values):
        self.values=values
        
    def get_value(self):
        return self.values
    
    def set_fitness(self,fitness):
        self.fitness=fitness
    
    def get_fitness(self):
        return self.fitness