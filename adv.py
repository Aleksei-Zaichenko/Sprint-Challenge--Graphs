from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# visited = {}
visited = set()



def get_the_opposite(direction):
    result = ''

    if direction == 'n':
        result = 's'
    elif direction == 's':
        result = 'n'
    elif direction == 'w':
        result = 'e'
    else:
        result = 'w'

    return result


def mark_room_as_visited(roomId):
    if roomId not in visited:
        visited.add(roomId)


def checkAllRooms(room):
    paths = []   #need to store path that we take

    for direction in player.current_room.get_exits():

        player.travel(direction)    #move to where it`s possible to move
        if player.current_room.get_room_id() not in visited: #check if we ever visited that room before
            paths.append(direction)      #save the direction
            mark_room_as_visited(player.current_room.get_room_id())     #mark the current room as visited
            paths += checkAllRooms(player.current_room)     # add next directions to current path
            player.travel(get_the_opposite(direction))      #step one room back
            paths.append(get_the_opposite(direction))       #save that we step back to our current path
        else:
            player.travel(get_the_opposite(direction))      #go one step back

    return paths   #return the result

traversal_path = checkAllRooms(player.current_room)     #for the test

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#         print('room',player.current_room)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
