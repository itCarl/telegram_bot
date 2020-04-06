import requests
from dotenv import load_dotenv
import os
from snakeTamer import snakeTamer

load_dotenv()
TOKEN = os.getenv('TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


# get last update_id
if os.path.exists('SnakeTamer/update_id.txt'):
    with open('SnakeTamer/update_id.txt') as file:
        update_id = int(file.readline()) + 1

    API_PARAM = f"?offset={update_id}"

else:
    API_PARAM = ""
    

# Build full api URL
reply = requests.get(f'{BASE_URL}/getupdates{API_PARAM}')

    
for data in reply.json().get('result'):
    try:
        # My first attempt solving the problem with "recieving old messages", but then i saw the update_id in the Api Doc
        # and from there on i changed my strategie
        #
        #currentTimestampMinus30 = int(str(time.time()).split('.')[0])-30   # get current unix Timestamp and subtract by 30 seconds
        #msgTimestamp = int(data["message"]["date"])                        # get Timestamp from json reply
        # if msgTimestamp > currentTimestampMinus30:
        # only respond to messages what aren't older than 30 seconds
        
        # Hole den Nachrichtentext, den Vornamen, den Usernamen, die ChatID und die update_id
        message = str(data["message"]["text"])
        first_name = str(data["message"]["from"]["first_name"])
        userID = str(data["message"]["from"]["id"])
        chat_id = data["message"]["chat"]["id"]
        update_id = data["update_id"]
        
        tamer = snakeTamer(userID)
        
        response = {"chat_id": chat_id, }

        # store last update id
        file = open("SnakeTamer/update_id.txt", "w")
        file.write(str(update_id))
        file.close()
        
        
        # Reagiere auf die Eingabe
        # Fallunterscheidung
        if message.startswith('/start'):
            response['text'] = f"Hello {first_name}\n\n".encode("utf8")
            response['text'] += f"Die Folgenden Kommandos stehen dir zu verfügung: \n".encode("utf8")
            
            # list all Available commands
            for item in tamer.commands:
                response['text'] += "/".encode("utf8") + str(item).encode("utf8") + "\n".encode("utf8")
            
            response['text'] += "\n\n" .encode("utf8")
            
            # list dead all Snakes
            for snake in tamer.snakes:
                if not snake.isAlive():
                    response['text'] += "Schlange ".encode("utf8") + snake.name.encode("utf8") + " ist verstorben. \n".encode("utf8")
            
            requests.post(f"{BASE_URL}/sendMessage", response)
        
        elif message.startswith('/about'):
            response['text'] = "Dieser Bot wurde erstellt für das Komplexpraktikum \n(Bachlor Informatik 4. Semester) an der Technischen Hochschule Brandenburg\n\n".encode("utf8")            
            response['text'] += "Was kannst du nun mit dem 'THB-Schlangenbändiger' Bot alles tun?\n".encode("utf8")
            response['text'] += "Im Grunde nicht sehr viel Außer Schlangen zu : \n\U00002022 bändigen,                                  /catchasnake \n\U00002022 füttern,                                       /snake [name] feed \n\U00002022 heilen,                                         /snake [name] heal \n\U00002022 in die Freiheit zu entlassen  /snake [name] release \n und Das Wetter zu sehen.".encode("utf8")
            response['text'] += "\n\n\n Tipp: Bei guten Wetter hast du eine Größere Chance eine Schlange zu bändigen".encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)
        
        elif message.startswith('/mysnakes'):
            # check if tamer has snakes
            print(tamer.mySnakes())
            if tamer.mySnakes() != 0:
                response['text'] = f"Hier sind alle deine Schlangen \U0001F40D \n\n".encode("utf8")
                
                for snake in tamer.mySnakes():
                    snake_name = snake.name
                    #snake_feel = snake_happinessToEmoji()
                    response['text'] += f"\U00002022 {snake_name}\n".encode("utf8")
                
                response['text'] += f"\n\nInteragiere mit einer Schlage\n".encode("utf8")
                response['text'] += f"Beispiel: /snake ".encode("utf8") + tamer.mySnakes()[0]["name"].encode("utf8") + " feed".encode("utf8") 
            else:
                response['text'] = f"Du hast zur zeit keine Schlage.\nBenutze /catchasnake um eine \U0001F40D zu fangen.".encode("utf8")
                
            requests.post(f"{BASE_URL}/sendMessage", response)
        
        elif message.startswith('/catchasnake'):
            catchSnake = tamer.catchSnake()
            
            if catchSnake == -1:
                response['text'] = f"Du kannst nicht mehr als 5 Schlangen gleichzeitig haben.".encode("utf8")
            elif catchSnake == -2:
                response['text'] = f"Keine Schlange wollte sich von dir bändigen lassen. \U0001F40D \U0001F40D \U0001F40D".encode("utf8")
            else:
                response['text'] = f"Super! Du hast {catchSnake} gebändigt.".encode("utf8")
            
            tamer.setLastAction("catch")
            requests.post(f"{BASE_URL}/sendMessage", response)
            
        elif message.startswith('/snake'):
            param = message.split()
            if len(param) > 2:
                snake_name = param[1]
                snake_action = param[2]
            else:
                snake_action = "unkown"
 
            if snake_action.startswith('release'):
                tamer.releaseSnake(snake_name)
                response['text'] = f"{snake_name} wurde in die freie Wildbahn entlassen".encode("utf8")
            elif snake_action.startswith('stats'):
                snake = tamer.getSnake(snake_name)
                snake_level = snake.level
                snake_health = snake.health
                snake_hunger = snake.hunger
                snake_happiness = snake.happiness
                response['text'] = f"{snake_name} \U0001F40D    level: {snake_level} \n\n".encode("utf8")
                response['text'] += f"\U00002764 \U000027f6   {snake_health} \n".encode("utf8") 
                response['text'] += f"\U0001F357 \U000027f6   {snake_hunger} \n".encode("utf8") 
                response['text'] += f"\U0001F600 \U000027f6   {snake_happiness} \n".encode("utf8")               
            elif snake_action.startswith('feed'):
                amt = tamer.feedSnake(snake_name)
                response['text'] = f"{snake_name} wurde gefüttern und hat jetzt weniger Hunger {amt}".encode("utf8")
            elif snake_action.startswith('heal'):
                amt = tamer.healSnake(snake_name)
                response['text'] = f"{snake_name} wurde geheilt und hat nun {amt} Gesungheit".encode("utf8")
            else:
                response['text'] = "Beispiel: /snake [name] stats \nDu kannst alle deine Schlangen mit /mysnakes sehen.".encode("utf8")
            #response['text'] = f"Ausgewählte Schlange: {snake_name}".encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)
        
        elif message.startswith('/wetter'):
            response['text'] = "Das Wetter:\nAktuell ist es ".encode("utf8") + tamer.weatherCondToText(tamer.currentWeatherCondition()).encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)
            
        else:
            response['text'] = f"Hast du dich vertippt?".encode("utf8")
            requests.post(f"{BASE_URL}/sendMessage", response)
        
    except Exception as e:
        print(e)
