from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk

# possible solution -

# grab my_graph of pre-neighbor'd rooms
# grab length of total number of rooms

# make a visited dictionary of rooms

# depth first traversal
# make a stack

# loop through while length of visited rooms is less than total number of rooms
# add current room to visited

# grab all neighboring rooms
# for each neighboring room:
# if neighboring room is not in visited
# add all neighbors to stack
# pop from stack and make current room that room.
# Also add direction traveled to travel_path


###

# build graph of visited rooms

# Goal - get graph of rooms with only the neighbors, not the coordinates.

my_graph = {}

for i in room_graph:
    my_graph[i] = room_graph[i][1]


print("My graph ", my_graph)


def explore():

    print("room graph ", room_graph[1][1])

    visited = []
    visited.append(player.current_room.id)

    room_exits = player.current_room.get_exits()
    print("player ", room_exits)

    for exit in room_exits:
        print("Room directions ", player.current_room.get_room_in_direction(exit).id)

    traversal_path = ['n', 'n']
    return traversal_path
# traversal_path = []


traversal_path = explore()

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
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
