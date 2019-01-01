from genetic_algorithm import GeneticAlgorithm

genetic=GeneticAlgorithm(path="tests/test2.txt") #dosyaın yolu verilerek çağrılabilir
genetic.create_model()  
genetic.fit_model()