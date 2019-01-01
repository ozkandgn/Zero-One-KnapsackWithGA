from matplotlib import pyplot as plt
from copy import deepcopy
from random import shuffle
from individual import Individual
from goods import Goods
import read 

class GeneticAlgorithm(Individual,Goods):               #işlemlerin yapıldığı sınıf
    
    def __init__(self,path="/"):        #nesne tanımlandığı an çaışacak fonksiyon
                                    #verinin alındığı ve değişlenlerin oluşturulduğu fonksiyon        
        values=read.read_values(path)
        self.random_list = list(map(float,values[0].split(",")))
        self.random_value = 0
        self.population_length = int(values[1])
        self.k_value = int(values[2])
        self.mutation_probility = float(values[3])
        self.iteration_length = int(values[4])
        self.bag_size = int(values[5])
        self.weight = list(map(int,values[6].split(",")))
        self.valuables = list(map(int,values[7].split(",")))
        self.individual_size = len(self.weight)
        self.generation = 0
        self.all_fitness=[[],[],[]]

    def get_random(self):               #random değer üreten fonksiyon
        self.random_value = (self.random_value + 1) % len(self.random_list)
        return self.random_list[self.random_value - 1]
    
    def create_populations(self):       #initialise                  #ilk populasyonu üretmeye yarayan fonksiyon
        populations=[]
        for i in range(self.population_length):
            populations.append(Individual())
            values=[]
            for j in range(self.individual_size):
                values.append(0 if self.get_random() < 0.5 else 1)
            populations[i].set_value(values)
        self.populations=populations

    def create_model(self):                     #arayüz fonksiyonu
        self.create_populations()
        self.get_weight_and_valuable()
        self.generation=0
        
    def print_population(self):                 #nesil ve popülasyonu yazdıran fonksiyon
        print("Generation: ",self.generation,"\n")
        self.generation+=1
        print("Population: ",end="")
        for i in self.populations:
            print("(",i.get_value(),",",i.get_fitness(),")",end="")
        print("")
        
    def get_weight_and_valuable(self):
        goods=[]
        for i in range(self.individual_size):
            goods.append(Goods())
            goods[i].set_weight(self.weight[i])
            goods[i].set_valuable(self.valuables[i])
        self.goods=goods

    def calculate_fitness(self): #Evaluate
        for i in range(self.population_length):
            population=self.populations[i].get_value()
            fitness=0
            bag_size=self.bag_size
            for j in range(len(population)):
                if population[j] == 1:
                    bag_size-=self.goods[j].get_weight()
                    if bag_size < 0:
                        fitness=0
                        break
                    fitness+=self.goods[j].get_valuable()
            self.populations[i].set_fitness(fitness)   
    
    def calculate(self):                        #işlemlerin başlatıldığı fonksiyon
        self.calculate_fitness()
        self.print_population()
        avg=lambda x: sum(x)/float(len(x))
        all_fitness=[]
        for i in self.populations:
            all_fitness.append(i.get_fitness())
        self.all_fitness[0].append(min(all_fitness))    #grafik oluşturmak için
        self.all_fitness[1].append(max(all_fitness))
        self.all_fitness[2].append(avg(all_fitness))
        self.tournament_selection()
        self.one_point_crossover()
        self.bit_flipping_mutation()
        self.survival_select()         
        
    def tournament_selection(self): #Parent Select          #turnuva seçim ile ebeveyn seçimi
        ceil=lambda x: round(x+0.5)
        get_point=lambda : ceil(self.get_random()*(self.population_length))-1
        populations=[]
        for i in range(self.population_length):
            populations.append(Individual())    #sıfırdan bireyler oluşuyor
            max_point=get_point()
            for j in range(self.k_value-1):     #k tane value arasından en iyisi seçiliyor
                rand_point=get_point()
                if self.populations[rand_point].get_fitness() >\
                                        self.populations[max_point].get_fitness():
                    max_point=rand_point      
            populations[i]=self.populations[max_point]

        self.parents=deepcopy(self.populations)
        self.parent_lenght=self.population_length       #parent ve childler dağıtılıyor
        self.populations=populations                    #artık yeni popülasyon childler
        self.population_length=len(populations)
        
    def one_point_crossover(self): #Recombine           #tek noktalı çaprazlama fonksiyonu
        swap=lambda x,y,k:((x[0:k]+y[k:]),(y[0:k]+x[k:])) #swap
        ceil=lambda x: round(x+0.5) #üste yuvarlama
        get_point=lambda : ceil(self.get_random()*(self.individual_size))  #random yer veren lambda
        values=[]
        for i in range(0,self.population_length,2):
            print("Applying Crossover")
            try:
                self.populations[i+1]
                point=get_point()
                
                #yazdırma
                print("Parents: [",self.populations[i].get_value(), " , ",\
                                 self.populations[i+1].get_value(),"] at point:",point)
                #yazdırma
                
                ind_one,ind_two=swap(self.populations[i].get_value(),\
                                     self.populations[i+1].get_value(),\
                                     point)#crossover
                values.append(Individual()) #deepcopy
                values[i].set_value(ind_one)
                values.append(Individual())
                values[i+1].set_value(ind_two)
                
                print("Children: [",ind_one," , ",ind_two,"]")
            except:
                print("Parent: ",self.populations[i].get_value())
                print("Child: ",self.populations[i].get_value())
                values.append(Individual())
                values[i].set_value(ind_one)

        self.populations=values
                
    def bit_flipping_mutation(self): #Mutation          #mutasyon işlemi
        #print
        print("Applying mutation to: ",end="")
        for i in self.populations:
            print(i.get_value(),end="")
        print("\n")
        print("Mutated offspring: ",end="")
        #
        change=lambda x:1 if x == 0 else 0          #mutasyon yapan lambda
        for i in range(self.population_length):
            values=[]
            val=self.populations[i].get_value()
            for j in val:
                values.append(change(j) if self.get_random() <\
                              self.mutation_probility else j)   #kontrol
            self.populations[i].set_value(values)
            print(self.populations[i].get_value(),end="")
            
            
    def quick_sort(self,popuation):          #sort() fonksiyonu yerine yazılmış quickSort foknksiyonu
        less,equal,greater = ([],[],[])
        if len(popuation) > 1:
            pivot = popuation[0].get_fitness()
            for i in popuation:
                temp_fitness=i.get_fitness()
                if temp_fitness < pivot:
                    less.append(i)
                if temp_fitness == pivot:
                    equal.append(i)
                if temp_fitness > pivot:
                    greater.append(i)
            return self.quick_sort(greater)+equal+self.quick_sort(less)
        else:
            return popuation
    
    def survival_select(self):#en iyilerin seçildiği fonksiyon
        self.calculate_fitness()

        self.populations=self.quick_sort(self.parents+self.populations)[0:self.population_length]

        shuffle(self.populations)#aynı fitness'e sahip değerlerin yeri değişsin diye shuffle yapılmıştır.
        self.calculate_fitness()
        
    def fit_model(self,iteration=-1): #modelin çağrıldığı ve grafiğin çizildiği arayüz 
        if iteration == -1:
            iteration=self.iteration_length
        for i in range(iteration):
            #print("İteration ",i+1)
            self.calculate()
        plt.scatter(range(0,iteration),self.all_fitness[0],c="blue")
        plt.scatter(range(0,iteration),self.all_fitness[1],c="brown") # yardırma ekranı
        plt.scatter(range(0,iteration),self.all_fitness[2],c="red")
        plt.plot(range(0,iteration),self.all_fitness[0],"blue"\
                 ,range(0,iteration),self.all_fitness[1],"brown"\
                 ,range(0,iteration),self.all_fitness[2],"red")
        plt.legend(["Min","Max","Avg"])
        plt.xlabel("iteration")
        plt.ylabel("fitness")
        plt.show()