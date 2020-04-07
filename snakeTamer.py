import os
import json
import numpy as np
from snake import snake


# add useful comment
class snakeTamer:
    commands = ['about', 'wetter', 'mysnakes', 'catchasnake', 'snake [name] [action]']
    snakes = []
    last_action = ""
    
    
    def __init__(self, userID):
        self.userID = userID
        self.loadProfile()
    
    def __del__(self):
        self.saveProfile(0)
        self.snakes.clear()
        
    def __getitem__(self,key):
        return getattr(self,key)
    
    
    def setLastAction(self, action):
        self.last_action = action
    
    
    def mySnakes(self):
        if len(self.snakes) != 0:
            return self.snakes
        else:
            return 0
    
    def catchSnake(self):
    
        if len(self.snakes) >= 5:
            print("Tamer can't have more then 5 Snakes at the same time")
            return -1
        
        
        weight_base = 0.1 # 10% base chance of catching a snake
        weight_right_answer = 0.1 # placeholder weight for a possible question/answer game
        
        
        # Snakes like warm Temperetures ~32°C (Source: google.com)
        cW = self.currentWeatherCondition()
        if cW == 1 or cW == 2:
            weight_weather = 0.35 # additional 50% chatch chance when its clear outside
        elif cW == 3:
            weight_weather = 0.2 # additional 30% chatch chance when its clear outside
        elif cW == 4 or cW == 5 or cW == 6:
            weight_weather = 0.1 # additional 10% chatch chance when its Stormy outside
        else:
            weight_weather = 0.2
        
        allWeights = weight_base + weight_weather + weight_right_answer
        
        if allWeights > 1.0:
            allWeights = 1.0
 
        choices = [0, 1]
        weights = [round(1.0-allWeights, 3), allWeights]

        # weighted_random
        rnd = np.random.choice(choices, p=weights)

        if rnd == 1:
            s = snake.getRandomSnake()
            self.snakes.append(s)
            return s["name"]
        else:
            return -2
    
    
    # release a Snake into the Wildness
    def releaseSnake(self, snake_name):
        for snake in self.snakes:
            if snake.name.lower() == snake_name.lower():
                print("snake removed")
                self.snakes.remove(snake)
    
    
    # feed a snake
    def feedSnake(self, snake_name):
        for snake in self.snakes:
            if snake.name.lower() == snake_name.lower():
                    snake.eat()
                    return snake.hunger
    
    # heals a snake
    def healSnake(self, snake_name):
        for snake in self.snakes:
            if snake.name.lower() == snake_name.lower():
                    snake.heal()
                    return snake.health
    
    # return the whole snake object
    def getSnake(self, snake_name):
        for snake in self.snakes:
            if snake.name.lower() == snake_name.lower():
                return snake
    
    
    # write profile to a .snaketamer file in json format
    def saveProfile(self, new):
        if new == 1:
            t = {
                "tamer_id": self.userID,
                "snakes": [],
                "last_action" : "created"
            }
            
        else:
            t = {
                "tamer_id": self.userID,
                "snakes": [sn.__dict__ for sn in self.snakes], # self.snakes
                "last_action" : self.last_action
            }
            
        file = open("SnakeTamer/"+self.userID+".snaketamer", "w+")
        file.write(json.dumps(t))
        file.close()
        return t
    
    
    # read User / Tamer Profile from a .snaketamer File
    def loadProfile(self):
        if not os.path.exists('SnakeTamer/'+self.userID+'.snaketamer'):
            if not os.path.exists('SnakeTamer'):
                os.mkdir("SnakeTamer")
            
            # if there was no profile found create one
            self.saveProfile(1)
            
        else:
            if len(self.snakes) < 1:
                f = open("SnakeTamer/"+self.userID+".snaketamer", "r")
                if f.mode == 'r':
                    content = json.loads(f.read())
                    self.last_action = content["last_action"]
                    for sn in content["snakes"]:
                        self.snakes.append(snake(str(sn["name"]), int(sn["level"]), int(sn["health"]), int(sn["hunger"]), int(sn["happiness"]), int(sn["last_eaten"]), int(sn["last_levelUp"])))
            else:
                print("Profil konnte nicht geladen werden.")
            return
    
    
    # returns weather condition as integer
    def currentWeatherCondition(self):
        # There is no need to call the OpenWeather api every time this method gets called since the
        # Api/Weather only get updated every 10 minutes
        # Thats the reason why i used the get_weather.py script
        
        if not os.path.exists('SnakeTamer/weather-data.json'):
            return -1 # no weather data available
        
        f = open("SnakeTamer/weather-data.json", "r")
        if f.mode == 'r':
            c = json.loads(f.read())
            weatherID = c["weather"][0]["id"]
            
            # Translate weather Conditions to my own ids
            # 2xx Thunderstorm
            if weatherID > 199 and weatherID < 300:
                condition = 6
            
            # 3xx Drizzle
            elif weatherID > 299 and weatherID < 400:
                condition = 3
            
            # 5xx Rain
            elif weatherID > 499 and weatherID < 600:
                condition = 4
            
            # 6xx Snow
            elif weatherID > 599 and weatherID < 700:
                condition = 5
            
            # Clear Sky
            elif weatherID == 800:
                condition = 1
            
            # Sky is Cloudy
            elif weatherID > 800:
                condition = 2
                
            else:
                condition = 0
            
            return condition
            
            
    # returns weather condition text with an emoji
    def weatherCondToText(self, condID):
        ret = " "
        # condID = 6 # for debugging
        
        if condID == 1:
            ret = "klar \U00002600"
        elif condID == 2:
            ret = "bewölkt \U000026C5" #\U00002601
        elif condID == 3:
            ret = "nieselt \U0001F4A7"
        elif condID == 4:
            ret = "regnerisch \U0001F327"
        elif condID == 5:
            ret = "schneit \U00002744"
        elif condID == 6:
            ret = "gewitter \U0001F329"
        else:
            ret = "unbekant \U0001F4A9"
        
        return ret
    
    
    # get current Temperetures
    def getTemperature(self):
        if not os.path.exists('SnakeTamer/weather-data.json'):
            return -1 # no weather data available
        
        f = open("SnakeTamer/weather-data.json", "r")
        if f.mode == 'r':
            c = json.loads(f.read())
            return {"temp": c["main"]["temp"], "feels_like": c["main"]["feels_like"]}