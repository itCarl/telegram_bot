import random
import time

# a simple snake class
class snake:
    
    def __init__(self, name, level, health, hunger, happiness, last_eaten, last_levelUp):
        currentTimestamp = int(str(time.time()).split('.')[0])

        #self.id = random.randrange(0, sys.maxint)
        self.name = name
        self.level = level
        self.health = health
        self.hunger = hunger 
        self.happiness = happiness
        self.last_eaten = last_eaten
        self.last_levelUp = last_levelUp
        
        # if a snake is alive for more then 1 Week it gets an level up
        if last_levelUp > (currentTimestamp+(60*60*24*7)):
            self.levelUp()         
    
    def __getitem__(self,key):
        return getattr(self,key)
        
    def getRandomSnake():
        # there is the possibility of snakes having the same name
        rand_names = ["Peter", "Susanne", "Siru", "Logi", "Locki", "Axel", "Robert", "Anton", "Felix", "Patrick", "Katrin", "Susi", "Antonia", "Jack", "Captian" "Ulrich", "Harald", "theSnake", "Nils", "Ben", "Gunnar", "Fiete", "Kimi", "Luca", "Fynn", "Hauke", "Aaron", "Kai","Karl", "Helger", "Hannes", "Frank", "Richard", "Martin", "Raik", "Lennard", "Caspar", "Axel", "Johan", "Falk", "Dieter-Riko", "Alberto-Horst", "Lenny-Reinmund", "Legolas", "Picasso", "Onassis", "Casanova", "Wolfgang"]
        name = rand_names[random.randrange(0, (len(rand_names)-1))]
        currentTimestamp = int(str(time.time()).split('.')[0])
        return snake(name, 1, random.randrange(50, 90), random.randrange(20, 80), random.randrange(10, 40), currentTimestamp, currentTimestamp)
        
        
    def eat(self):
        self.hunger += random.randrange(5, 40)
        if self.hunger > 100:
            self.hunger = 100
        self.last_eaten = int(str(time.time()).split('.')[0])
                
    def heal(self):
        self.health += random.randrange(10, 35)
        if self.health > 100:
            self.health = 100
        
    def takeDamage(self, amt):
        self.health -= amt
        if self.health < 0: # TODO: if snake is dead delete from player
            self.health = 0
    
    def levelUp(self):
        self.level += 1
        
    def isAlive(self):
        # calculate the lost hunger
        DiffSec = int(str(time.time()).split('.')[0]) - int(self.last_eaten)
        deathTime = round((DiffSec / 60) / (3*60))
        lostHunger = round((DiffSec / 60) / 30)        # every 30 Minutes a Snake loses 1 Hunger point
        
        # when the lost hunger is greater then last saved hunger AND the snake asn't ate for 3 hours
        # then the snake is dead
        if lostHunger > self.hunger and deathTime >= 1:
            self.health = 0
            return 0
            
        self.hunger -= lostHunger
        return 1