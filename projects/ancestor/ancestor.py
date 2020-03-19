from graph import Graph
from util import Stack, Queue

def earliest_ancestor(ancestors, starting_node):
    graph = Graph()
    for ancestor in ancestors:
        parent, child = ancestor

        if parent not in graph.vertices:
            graph.add_vertex(parent)
        if child not in graph.vertices:
            graph.add_vertex(child)
        graph.add_edge(parent, child)
        

    if len(graph.get_neighbors(starting_node)) == 0:
        return -1
    
    q = Queue()
    q.enqueue([starting_node, 0])

    processed_ancestors = {}
    while q.size() > 0:
        person, distance = q.dequeue()

        if distance in processed_ancestors:
            processed_ancestors[distance].append(person)
        else:
            processed_ancestors[distance] = person

        a = graph.get_neighbors(person)
        if len(a) > 0:
            for p in a:
                q.enqueue([p, distance + 1])

        max_distance = max(processed_ancestors.keys())
        return max_distance

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

print(earliest_ancestor(test_ancestors, 1)) # 10
print(earliest_ancestor(test_ancestors, 2)) # -1
print(earliest_ancestor(test_ancestors, 3)) # 10