import pygame
import os
import sys
import time

# Set working directory
# os.chdir("/Users/candela/Desktop/DATA ESCAPE copy/")
os.chdir(os.path.dirname(os.path.abspath(__file__)))



# Initialize Pygame and mixer
# Create a game window
#screen = pygame.display.set_mode((800, 600))
#pygame.display.set_caption("Game Window")
pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height ))
ASSET_PATH = os.path.dirname(os.path.abspath(__file__))  # Caminho da pasta onde está o .py
pygame.display.set_caption("Escape from Data")

# this function will show the images of the rooms
def show_room(room):
    try:
        path_ = f"{room['name']}.jpg" or f"{room['name']}.jpeg"
        if not os.path.isfile(path_):
            print(f"Image not found: {path_}")
            return
        
        image = pygame.image.load(path_)
        image = pygame.transform.scale(image, (width, height ))
        window.blit(image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(1000)
    except Exception as e:
        print(f"Error showing image of '{room}': {e}")

# this funcition will show the images of the items
def show_object(item_name):
    try:
        path2 = f"{item_name}.jpg" or f"{item_name}.jpeg"
        if not os.path.isfile(path2):
            print(f"Image not found: {path2}")

        image = pygame.image.load(path2)
        image = pygame.transform.scale(image, (width, height ))
        window.blit(image, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.delay(2000)
    except Exception as e:
        print(f"Error showing image of the object '{item_name}': {e}")

pygame.mixer.init()

# Load and play background music
try:
    # pygame.mixer.music.load("/Users/candela/Desktop/DATA ESCAPE copy/office.mp3")  # Use an absolute path
    pygame.mixer.music.load("office.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)  # Loop indefinitely
    
except pygame.error as e:
    print(f"Error loading music: {e}")
    sys.exit(1)

# Debugging mixer initialization
if not pygame.mixer.get_init():
    print("Error: Pygame mixer did not initialize properly!")
else:
    print("Mixer initialized successfully!")


# Define rooms and game state first
office = {
    "name": "office",
    "type": "room",
}

outside = {
  "name": "outside",
  "type": "room",
}

INIT_GAME_STATE = {
    "current_room": office,
    "keys_collected": [],
    "target_room": outside
}

# Function to suppress output
#def suppress_output():
#    sys.stdout = open(os.devnull, 'w')
#    sys.stderr = sys.stdout

# Function to restore output
#def restore_output():
#    sys.stdout = sys.__stdout__
##    sys.stderr = sys.__stderr__

# Initialize pygame (suppress unnecessary output here)


# Let pygame settle in
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Restore output to show only game-related messages
#restore_output()

#Now, start the game properly AFTER everything is defined

def start_game():
    """
    Start the game
    """
    global game_state  # Declare it as global so Python knows it's accessible
    game_state = INIT_GAME_STATE.copy()  # Initialize before usage

    print("Well Hello! How did you end up here? Was it a mistake? A setup? Or did you willingly step into the depths of this high-security Data Facility thinking you had an escape plan? This high-security vault was not built to be broken into… or out of, GOOD LUCK!")

    play_room(game_state["current_room"])  # Now, `game_state` should be properly defined!


# define rooms and items

object_window = {
    "name": "window",
    "type": "object",
}

door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}


laptop_bag = {
    "name": "laptop bag",
    "type": "object",
}

office = {
    "name": "office",
    "type": "room",
}
door_b = {
    "name": "door b",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

door_c = {
    "name": "door c",
    "type": "door"
}

computer_desk = {
    "name": "computer desk",
    "type": "object",
}

operations_room = {
    "name": "operations room",
    "type": "room",
}

server_room = {
    "name": "server room",
    "type": "room",
}



door_d = {
    "name": "door d",
    "type": "door",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

server_rack = {
    "name": "server rack",
    "type": "object",
}

safe = {
    "name": "safe",
    "type": "object",
    "password": "Data"
}

lobby = {
    "name": "lobby",
    "type": "room",
}

cabinet = {
    "name": "cabinet",
    "type": "object",
}


outside = {
  "name": "outside",
  "type": "room",
}


all_rooms = [office,operations_room, server_room, lobby, outside]

all_doors = [door_a,door_b, door_c, door_d]


# Initialize object_relations as an empty dictionary first
object_relations = {}

# To update the dictionary with room-object relationships
object_relations.update({
    "office": [object_window,laptop_bag, door_a],
    "laptop bag": [key_a],
    "operations room": [computer_desk, door_a, door_b, door_c],
    "computer desk": [key_b],
    "door a": [office, operations_room],
    "door b": [operations_room, server_room],
    "door c": [operations_room, lobby],
    "server room": [door_b, server_rack, safe],
    "server rack": [key_c],
    "safe": [key_d],
    "lobby": [door_c, cabinet, door_d],
    "door d": [outside],
    "outside": [door_d],
})


# define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.


# Game state
# game_state = INIT_GAME_STATE.copy()
#game_state = INIT_GAME_STATE.copy()
current_music_file = ""  # Initialize globally

#Define functions

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

#def update_music(room_name):
#    global current_music_file

#    music_file = f"/Users/candela/Desktop/DATA ESCAPE copy/{room_name.replace(' ', '_')}.mp3"


#    if os.path.exists(music_file):
#        if current_music_file != music_file:  # Ensure only changes when needed
#            pygame.mixer.music.stop()
#            pygame.mixer.music.unload()
#            pygame.mixer.music.load(music_file)
#            pygame.mixer.music.set_volume(1.0)
#            pygame.mixer.music.play(-1)
#            current_music_file = music_file  # Update the currently playing track

#import time  # ✅ Import time module

def update_music(room_name):
    global current_music_file

    music_file = f"{room_name.replace(' ', '_')}.mp3"
    music_file_ = os.path.join(ASSET_PATH, music_file)

    if os.path.exists(music_file) and current_music_file != music_file:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        
        time.sleep(3)  # ✅ Pause execution for 3 seconds

        pygame.mixer.quit()  # ✅ Completely stop mixer before restarting
        pygame.mixer.init()  # ✅ Reinitialize mixer (this clears buffers)

        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        current_music_file = music_file

def play_sound_effect(music_file):
    path2 = os.path.join(ASSET_PATH, music_file)
    if os.path.exists(path2):
        try:
            sound = pygame.mixer.Sound(path2)
            sound.set_volume(1.0)
            sound.play()
        except Exception as e:
            print(f"Error playing the sound: {e}")
    else:
        print(f"Sound effect not found: {path2}")


def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here. Updates music in each room
    """
    game_state["current_room"] = room
    show_room(room) # this shows the image of the room
    if game_state["current_room"] == game_state["target_room"]:
        update_music(room['name'])  # Only update music once
        print("Congrats! You escaped the terrible Data Center!")
        return  # End the game properly
    
    print(f"You are now in {room['name']}")
    update_music(room['name'])  # Only update music once

    while True:  # Keep running in a loop instead of recursion
        intended_action = input("What would you like to do? Type 'explore' or 'examine': ").strip().lower()

        if intended_action == "explore":
            explore_room(room)  # Call function normally
        elif intended_action == "examine":
            examine_item(input("What would you like to examine? ").strip())  
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
        
        # Ensure the player can move rooms
        if game_state["current_room"] != room:
            play_room(game_state["current_room"])  # Move rooms and break loop
            break
def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is the " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            show_object(item_name) #this shows the object
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
           
                else:
                    output += "It is locked but you don't have the key."
            else:
                if item["name"] == "safe":
                    entered_password = input("The safe requires a password. Enter password (Hint: I am not an integer nor I am a float, I am your favorite 4-letter word…): ").strip()
                    if entered_password == item.get("password"):
                        if item["name"] in object_relations and len(object_relations[item["name"]]) > 0:
                            item_found = object_relations[item["name"]].pop()
                            game_state["keys_collected"].append(item_found)
                            output += "Correct password! You open the safe and find " + item_found["name"] + "."
                        else:
                            output += "You open the safe, but it's empty."
                    else:
                        output += "Incorrect password. The safe remains locked."

                elif(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    # Play key unlock sound effect
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        linebreak()
        play_sound_effect("key_unlock.mp3")
        
        play_room(next_room)
        return #Ensures only one call to 'play_room()'
    
    else:
        linebreak()
        play_room(current_room)

if __name__ == "__main__":
    game_state = INIT_GAME_STATE.copy()
    start_game()


   