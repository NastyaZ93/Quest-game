# -*- coding: utf-8 -*-
"""
Converted from IPYNB to PY
"""

# %% [code] Cell 1
game_room = {
    "name": "game room",
    "type": "room",
}

piano = {
    "name": "piano",
    "type": "furniture",
}
couch = {
    "name": "couch",
    "type": "furniture",
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

bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
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

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

door_c = {
    "name": "door c",
    "type": "door",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

door_d = {
    "name": "door d",
    "type": "door",
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

living_room = {
    "name": "living room",
    "type": "room",
}

dining_table = {
    "name": "dining table",
    "type": "furniture",
}

outside = {
  "name": "outside",
  "type": "room",
} 

# %% [code] Cell 2
all_rooms = [game_room,bedroom_1,bedroom_2,living_room, outside] #to add all rooms here

all_doors = [door_a,door_b,door_c,door_d] #to add all doors here

# %% [code] Cell 3
object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "key for door a": [door_a],
    "door a": [game_room, bedroom_1],
    "bedroom 1": [door_a, queen_bed, door_b, door_c],
    "queen bed": [key_b],
    "key for door b": [door_b],
    "door b": [bedroom_1, bedroom_2],
    "bedroom 2": [door_b, double_bed, dresser],
    "double bed": [key_c],
    "dresser": [key_d],
    "key for door c": [door_c],
    "door c": [bedroom_1, living_room],
    "living room": [door_c, dining_table, door_d],
    "key for door d": [door_d],
    "door d": [living_room, outside],
    "outside": [door_d]
}

# %% [code] Cell 4
INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

game_state = INIT_GAME_STATE.copy()

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items)) ##.join(items)  # Combines with commas!

def get_next_room_of_door(door, current_room): #Loop through both rooms connected to door#If room is NOT the current room#Return that room!
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

    for item in object_relations[current_room["name"]]:   ##Logic:Loop through keys player has #Check if any key matches this door#If yes: unlock and get next room#If no: tell player door is locked
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
            else: #Check if item has anything hidden (using object_relations)#If yes: take the key and add to inventory# If no: nothing to find
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0): 
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None): #If item wasn't found in room, tell player.
        print("The item you requested is not found in the current room.")

    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'): #If unlocked a door: ask if they want to go to next roomIf yes: call play_room(next_room)If no: call play_room(current_room) (stay in room)
        play_room(next_room)
    else:
        play_room(current_room)

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
        print("You are now in " + room["name"])
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



def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])



# %% [code] Cell 5
start_game()
