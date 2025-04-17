import pygame
import os

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

# Define the game functions before calling them
def start_game():
    print("Welcome to the Escape Room!")
    play_room(game_state["current_room"])

def play_room(room):
    print(f"You are now in {room['name']}")

# Initialize Pygame's mixer
pygame.mixer.init()

# Set working directory (if needed)
os.chdir("/Users/candela/Desktop/DATA ESCAPE/")

# Load and play background music
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Now, start the game properly AFTER everything is defined
game_state = INIT_GAME_STATE.copy()
start_game()  # This now works without errors!


# define rooms and items

window = {
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
    "office": [window,laptop_bag, door_a],
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

INIT_GAME_STATE = {
    "current_room": office,
    "keys_collected": [],
    "target_room": outside
}


def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("Well Hello!How did you end up here? Was it a mistake? A setup? Or did you willingly step into the depths of this high-security Data Facility thinking you had an escape plan? This high-security vault was not built to be broken into… or out of, GOOD LUCK!")


    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in the " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

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
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")

    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)

    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()
