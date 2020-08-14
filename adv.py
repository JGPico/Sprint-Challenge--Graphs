from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


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

# for room in world.rooms:
#     print("world room ", room)

my_graph = {}

for i in room_graph:
    my_graph[i] = room_graph[i][1]
    # # this loop will change all the cardinal directions to '?' marks
    # for neighbors in my_graph[i]:
    #     my_graph[i][neighbors] = '?'

# print("My graph ", my_graph)

# for room_bit in my_graph[1]:
#     print("room_bit ", room_bit)
#     print("Neighboring room id ", my_graph[1][room_bit])
#     print("Individual room ", room_bit[0],
#           player.current_room.get_room_in_direction(room_bit[0]).id)


def get_neighboring_rooms(graph, current_room):
    list_of_neighbors = []
    for room_bit in graph[current_room]:
        list_of_neighbors.append(graph[current_room][room_bit])

    return list_of_neighbors


def get_travel_path(current_room, target_room, s_graph):
    q = Queue()
    q.enqueue([current_room])
    # create a set to store search_visited vertices
    search_visited = set()

    # while the queue is not empty
    while q.size() > 0:
        # dequeue the first PATH
        path = q.dequeue()
        # grab the last vertex from the Path
        v = path[-1]
        # check if the vertex has not been search_visited
        if v not in search_visited:
            # is this vertex the target?
            if v == target_room:
                # return the path (ability to break out)
                return path
            # else it is not the target, so mark it as search_visited

            search_visited.add(v)

            # then add a path to its neighbors in the back of the queue
            for next_vertex in get_neighboring_rooms(s_graph, v):
                # make a copy of the path
                path_copy = list(path)
                # append neighbor to the back of the path
                path_copy.append(next_vertex)
                # enqueue out new path
                q.enqueue(path_copy)

    # return None if can't find thing.
    return None


# my_travel = get_travel_path(0, 9, my_graph)
# print("travel path ", my_travel)
# print()

# print("Player current room ", player.current_room.id)
# player.travel("w")


# expects a path of room id's, travel's the player from the start room to the end room
# returns a travel_path_list
def travel_along_path(travel_array):
    if player.current_room.id != travel_array[0]:
        print("The player didn't start at the first room of the travel array ")
        return

    mini_travel_path = []

    for room in travel_array:
        # print("room in travel path ", room)
        # print("Player's current room ", player.current_room.id)

        if player.current_room.id != room:
            cardinal_exits = player.current_room.get_exits()
            for one_exit in cardinal_exits:

                # print("room in travel path is " + str(room) + " room in direction " + one_exit + " is " +
                #       str(player.current_room.get_room_in_direction(one_exit).id))

                if player.current_room.get_room_in_direction(one_exit).id == room:
                    # print("The player traveled " +
                    #       one_exit + " to " + str(room))
                    mini_travel_path.append(one_exit)
                    player.travel(one_exit)
                    break

    return mini_travel_path


def explore(graph):
    s = Stack()
    visited = {}
    traveled_path = []

    # set up initial rooms to explore
    visited[player.current_room.id] = 1
    for neighbor in graph[player.current_room.id]:
        cardinal_direction = neighbor[0]

        neighboring_room = player.current_room.get_room_in_direction(
            neighbor[0]).id

        # add neighboring room ids to stack, if they are not in visited
        if neighboring_room not in visited:
            s.push(neighboring_room)

    s.push(player.current_room.id)
    # print("s at the start ", s.stack)

    while s.size() > 0:
        # path = s.pop()
        next_room_in_stack = s.pop()
        # print("next room in stack at start of while loop ", next_room_in_stack)

        if next_room_in_stack not in visited:
            # visited[next_room_in_stack] = 1

            # print("visited ", visited)

            # this loop looks to see if the next room in the stack is adjacent
            found_adjacent_unexplored = False
            for neighbor in graph[player.current_room.id]:

                cardinal_direction = neighbor[0]

                neighboring_room = player.current_room.get_room_in_direction(
                    neighbor[0]).id

                # print("the next room in stack is ", next_room_in_stack)
                # print("player in ", player.current_room.id)
                # print("room id in cardinal direction " +
                #       cardinal_direction + " is ", neighboring_room)

                if neighboring_room == next_room_in_stack:
                    found_adjacent_unexplored = True
                    traveled_path.append(cardinal_direction)
                    player.travel(cardinal_direction)
                    visited[player.current_room.id] = 1
                    break

            if found_adjacent_unexplored == False:
                route_back = get_travel_path(
                    player.current_room.id, next_room_in_stack, graph)

                # print("s ", next_room_in_stack)
                # print("current player room ", player.current_room.id)
                # print("route back ", route_back)
                mini_path = travel_along_path(route_back)
                traveled_path = traveled_path + mini_path

            # This loop adds neighboring rooms to the stack
            for neighbor in graph[player.current_room.id]:
                cardinal_direction = neighbor[0]

                neighboring_room = player.current_room.get_room_in_direction(
                    neighbor[0]).id

                # add neighboring room ids to stack, if they are not in visited
                if neighboring_room not in visited:
                    # print("Room " + str(neighboring_room) +
                    #       " got pushed to the stack")
                    s.push(neighboring_room)

    return traveled_path

# traversal_path = []


traversal_path = explore(my_graph)

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
