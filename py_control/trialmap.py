import heapq

def dijkstra(graph,start, end):
    num_vertices = len(graph)
    distances = [float('inf')] * num_vertices
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_vertices = [-1] * num_vertices
    directions = [''] * num_vertices

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex == end:
            break

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, (weight, direction) in enumerate(graph[current_vertex]):
            if weight > 0:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    directions[neighbor] = direction
                    heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    path_directions = []
    current_vertex = end

    while current_vertex != -1:
        path.append(current_vertex)
        if current_vertex != start:
            path_directions.append(directions[current_vertex])
        current_vertex = previous_vertices[current_vertex]

    path.reverse()
    path_directions.reverse()

    return path, path_directions, distances[end]

# graph = [
#     [(0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
#     [(1, 'south'), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (1, 'west'), (0, ''), (0, 'east'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (1, 'wast'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (1, 'north')],
#     [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (0, '')],
#     [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, '')]
# ]

# start = int(input("Enter the start vertex (0-14): "))
# end = int(input("Enter the end vertex (0-14): "))

# path, path_directions, distance = dijkstra(graph, start, end)
# d = {"north":0, "east":1, "south":2, "west":3}
# patht = []
# for i in path_directions:
#     patht.append(d[i])
#     # print(d[i])
# # print(patht)
# print(f"The shortest path from vertex {start} to vertex {end} is: {' -> '.join(map(str, path))} with a distance of {distance}")
# print(patht)

def run_dij(start, end):
    graph = [
    [(0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
    [(0, ''), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
    [(1, 'south'), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
    [(0, ''), (0, ''), (1, 'west'), (0, ''), (0, 'east'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
    [(0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
    [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
    [(0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, ''), (0, '')],
    [(0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, ''), (0, '')],
    [(0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, ''), (1, 'north'), (0, '')],
    [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, '')],
    [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'east'), (0, ''), (0, ''), (0, '')],
    [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (0, ''), (0, '')],
    [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (1, 'east'), (1, 'north')],
    [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, ''), (0, ''), (1, 'west'), (0, ''), (0, '')],
    [(0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (0, ''), (1, 'south'), (0, ''), (0, '')]
]
    path, path_directions, distance = dijkstra(graph, start, end)
    d = {"north":0, "east":1, "south":2, "west":3}
    patht = []
    for i in path_directions:
        patht.append(d[i])
        # print(d[i])
    # print(patht)
    print(f"The shortest path from vertex {start} to vertex {end} is: {' -> '.join(map(str, path))} with a distance of {distance}")
    # print(patht)
    return patht

# run_dij(4,9)