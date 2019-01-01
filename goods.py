class Goods:                        #Eşya nesnesi, her bir eşyanın ağırlığı ve pahasi bulunmaktadır.
    def set_weight(self,weights):
        self.weight=weights

    def get_weight(self):
        return self.weight

    def set_valuable(self,valuables):
        self.valuable=valuables
     
    def get_valuable(self):
        return self.valuable
    
    def get_lenght(self):
        if len(self.weight) > 0:
            return len(self.weight)
        elif len(self.valuable) > 0:
            return len(self.valuable)
        else:
            return 0