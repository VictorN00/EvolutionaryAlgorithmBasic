import random

class Runner(object):
    
    def __init__(self, speed):
        self.speed = speed
        self.fitness = self.calculate_fitness()
    
    @classmethod
    def random_speed(self):
        return random.random() * 2
    
    @classmethod
    def create(self):
        return Runner(self.random_speed())
    
    def mate(self, parent2):
        rand = random.random()
        if rand < 0.45:
            return Runner(self.speed + random.random() / 2- 0.25)
        elif rand < 0.9:
            return Runner(parent2.speed + random.random() / 2 - 0.25)
        else:
            return Runner.create()
    
    def calculate_fitness(self):
        return self.speed
    
    def __repr__(self):
        return '{:.2f}'.format(self.speed)

def main():
    gen = 1
    POPULATION_SIZE = 10
    pop = [Runner.create() for _ in range(POPULATION_SIZE)]
    while gen < 50:
        pop = sorted(pop, key=lambda x: x.fitness)
        pop.reverse()
        print('Generation {}: {} - Max Fitness: {:.4f}'.format(gen, str(pop), pop[0].fitness))
        new_pop = []
        s = int(0.1 * POPULATION_SIZE)
        new_pop.extend(pop[:s])
        s = int(0.9 * POPULATION_SIZE)
        for _ in range(s):
            p1 = random.randrange(0, s)
            p2 = random.randrange(0, s)
            if POPULATION_SIZE >= 3:
                while p1 == p2:
                    p2 = random.randrange(0, s)
            child = pop[p1].mate(pop[p2])
            new_pop.append(child)
        pop = new_pop
        gen += 1
    
    pop = sorted(pop, key=lambda x: x.fitness)
    pop.reverse()    
    print('Generation {}: {} - Max Fitness: {:.4f}'.format(gen, pop, pop[0].fitness))

if __name__ == '__main__':
    main()