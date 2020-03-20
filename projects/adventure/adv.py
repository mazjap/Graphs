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

north = 'n'
south = 's'
east = 'e'
west = 'w'

graph = Graph()
traversal_path = []

# def generate_graph():
#     graph = Graph()
#     grid = world.room_grid
#     for row in range(len(grid)):
#         for col in range(len(grid[row])):
#             low_row = row-1
#             low_col = col-1
#             room_north = None
#             room_west = None
#             room = grid[row][col]
#             if low_row >= 0:
#                 room_north = grid[low_row][col]
#             if low_col >= 0:
#                 room_west = grid[row][low_col]

#             if room:
#                 graph.add_vertex(room.id)
#                 if room_north:
#                     graph.add_undirected_edge(room.id, room_north.id)
#                 if room_west:
#                     graph.add_undirected_edge(room.id, room_west.id)

#     print(graph.dfs('000', '010'))
#     return graph

# def generate_graph():
#     graph = Graph()
#     visited = set()
#     q = Queue()
#     room = world.starting_room
#     previous_room = room
#     q.enqueue(room)
#     while q.size > 0:
#         room = q.dequeue()
#         visited.add(room.id)
#         graph.add_vertex(room.id)

#         if previous_room is not room:
#             graph.add_undirected_edge(room, previous_room)

#         rooms = room.get_exits()
#         for neighbor in rooms:
#             q.enqueue(neighbor)
    


#     return graph

def get_reverse(direction):
    if direction is south:
        return north
    elif direction is north:
        return south
    elif direction is east:
        return west
    elif direction is west:
        return east
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
    has_unvisited = False
    while not has_unvisited:
        for direction in exits:
            room = player.current_room.get_room_in_direction(direction)
            if room.id not in visited:
                return count
        index -= 1
        new_direction = get_reverse(traversal_path[index])
        player.travel(new_direction)





def traverse_graph(graph, visited={player.current_room.id}, count=1):
    exits = player.current_room.get_exits()
    if len(exits) > 0:
        direction = exits[random.randint(0, len(exits) - 1)]
        room = player.current_room.get_room_in_direction(direction)
        if room.id not in visited:
            visited.add(room.id)
            count += 1
            player.travel(direction)
            traversal_path.append(direction)
            traverse_graph(graph, visited, count)
    if len(visited) != world.grid_size:
        count += return_to_unvisited(visited)
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
