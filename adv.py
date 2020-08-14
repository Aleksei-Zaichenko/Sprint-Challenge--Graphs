from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue
from graph import Graph
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
visited = {}


def mark_room_as_visited(roomId):
    if roomId not in visited:
        visited[roomId] = {}

        for direction in player.current_room.get_exits():
            visited[roomId][direction] = '?'

def checkAllRooms():

    stack = Stack()

    while len(visited) <len(room_graph):
        # path = stack.pop()
        # currentRoom = path[-1]

        mark_room_as_visited(player.current_room.get_room_id())
        directionChoice = None

        for direction in visited[player.current_room.get_room_id()].keys():
            if visited[player.current_room.get_room_id()][direction] == '?':
                directionChoice = direction

        if directionChoice != None:
            old_room_id = player.current_room.get_room_id()
            # pathCopy = path.copy()
            traversal_path.append(directionChoice)

            player.travel(directionChoice)

            mark_room_as_visited(player.current_room.get_room_id())

            # pathCopy.append(player.current_room)

            visited[old_room_id][directionChoice] = player.current_room.get_room_id()
            # stack.push(pathCopy)
        else:
            directions = list(visited[player.current_room.get_room_id()].keys())
            directionChoice = directions[random.randint(0,len(directions ) -1)]
            traversal_path.append(directionChoice)
            player.travel(directionChoice)

    print('trav', traversal_path)
    print(visited)
    # end of checkAllRooms method

checkAllRooms()

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
