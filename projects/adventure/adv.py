from room import Room
from player import Player
from world import World
from graph import Graph
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

graph = Graph()
traversal_path = []

def get_reverse(direction):
    if direction is 's':
        return 'n'
    elif direction is 'n':
        return 's'
    elif direction is 'e':
        return 'w'
    elif direction is 'w':
        return 'e'
    else:
        print(f"Error, direction {direction} is not valid")

def generate_graph(room, visited=set()):
    visited.add(room.id)
    rooms = room.get_exits()

    for direction in rooms:
        neighbor = room.get_room_in_direction(direction)
        if neighbor.id not in visited:
            visited.add(neighbor.id)
            graph.add_vertex(neighbor.id)
            graph.add_undirected_edge(room.id, neighbor.id)
            generate_graph(neighbor, visited)

def return_to_unvisited(visited):
    count = 0
    index = len(traversal_path) - 1
    exits = player.current_room.get_exits()
    while True:
        for direction in exits:
            room = player.current_room.get_room_in_direction(direction)
            if room and room.id not in visited:
                return count
        index -= 1
        new_direction = get_reverse(traversal_path[index])
        if index >= 0 and player.current_room.get_room_in_direction(new_direction):
            player.travel(new_direction)
        else:
            return 0

def find_untraveled_directions(visited, room):
    directions = room.get_exits()
    possible = []
    for direction in directions:
        next_room = room.get_room_in_direction(direction)
        if next_room.id not in visited:
            possible.append(direction)
    return possible

def find_untraveled_secondary_direction(visited):
    exits = player.current_room.get_exits()
    for next_direction in exits:
        room = player.current_room.get_room_in_direction(next_direction)
        secondary_exits = find_untraveled_directions(visited, room)
        if len(secondary_exits) > 0:
            return (next_direction, secondary_exits)

def traverse_graph(graph, visited={player.current_room.id}, count=1):
    print(traversal_path)
    directions = find_untraveled_directions(visited, player.current_room)
    secondary_directions = find_untraveled_secondary_direction(visited)
    print(len(directions))
    if len(directions) > 0:
        direction = directions[random.randint(0, len(directions)-1)]
        room = player.current_room.get_room_in_direction(direction)
        if room is not None:
            visited.add(room.id)
            count += 1
            player.travel(direction)
            traversal_path.append(direction)
    elif secondary_directions:
        direction = secondary_directions[0]
        directions_arr = secondary_directions[1]
        direction2 = directions_arr[random.randint(0, len(directions_arr) - 1)]
        player.travel(direction)
        player.travel(direction2)

        visited.add(player.current_room.id)
        count += 2
        traversal_path.append(direction); traversal_path.append(direction2)
    else:
        add_count = return_to_unvisited(visited)
        if add_count is 0 or len(visited) is world.grid_size:
            return
        else:
            count += add_count
    traverse_graph(graph, visited, count)


def generate_path():
    room = world.starting_room
    graph.add_vertex(room.id)

    generate_graph(room)
    traverse_graph(graph)

    print(traversal_path)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

generate_path()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
