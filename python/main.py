# by GiorDior aka Markimark aka Giorgio
from random import randint
import pygame, math

class Root:
    def __init__(self, size: tuple, caption: str) -> None:
        self.clock = pygame.time.Clock()
        # window size
        self.size = size
        # window caption
        self.caption = caption
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)

    def get_surface(self):
        return self.surface

    def update(self, fps: int):
        # update screen
        self.clock.tick(fps)
        pygame.display.update()

class Node:
    def __init__(self, position: tuple) -> None:
        # node position
        self.position = position
        # nodes which have a connection to this node
        self.next_nodes = []
        # starting travel cost is set as high as possible
        self.travel_cost = 100000000000000000000000
        # the node which previously led to this node and has the shortest distance
        self.prev_node = None

    def render(self, root, radius: int=5, color="black"):
        # draw a circle
        pygame.draw.circle(root, color, (self.position[0], self.position[1]), radius=radius)

def generate_connections(number_of_connections: int, amount_of_nodes: int):
    connections = []
    for i in range(number_of_connections):
        node1 = randint(0, amount_of_nodes - 1)
        node2 = randint(0, amount_of_nodes - 1)
        # checking if connection is already in the array
        # or if both points are the same
        # connection = [first_node_index, second_node_index]
        if not node1 == node2 and not (node1, node2) in connections and not (node2, node1) in connections:
            connections.append((node1, node2))
    return connections 

def assign_next_node(nodes: list[Node], connections: list[tuple]):
    for connection in connections:
        first_node = nodes[connection[0]]
        second_node = nodes[connection[1]]
        first_node.next_nodes.append(second_node)
        second_node.next_nodes.append(first_node)


def choose_start_and_end_node(nodes: list[Node]):
    # the start and end node are the one which have the 
    # longest distance between each other
    longest_distance = -float("inf")
    start_index = 0
    end_index = 0
    for index, node in enumerate(nodes):
        for _index, _node in enumerate(nodes):
            if not index == _index:
                # formula of distance
                distance = math.sqrt( (node.position[0] - _node.position[0]) ** 2 +  (node.position[1] - _node.position[1]) ** 2)
                if distance > longest_distance:
                    longest_distance = distance
                    start_index = index
                    end_index = _index
    return start_index, end_index

def calculate_travel_cost(current_node: Node):
    for node in current_node.next_nodes:
        # travel cost = distance to the next node + travel cost of the current node
        distance = math.sqrt( (node.position[0] - current_node.position[0]) ** 2 +  (node.position[1] - current_node.position[1]) ** 2)
        val = current_node.travel_cost + distance
        # checking if the new travel cost is better
        if val < node.travel_cost:
            node.travel_cost = val
            node.prev_node = current_node
            calculate_travel_cost(node)

def draw_shortest_distance(root: Root, nodes: list[Node], current_node: Node, start_index: int):
    # going as long as it takes back to the prev node until the starting node is reached
    if nodes.index(current_node) == start_index:
        return None
    first_position = current_node.position
    second_position = current_node.prev_node.position

    pygame.draw.polygon(root.get_surface(), ("green"), (first_position, second_position), width=5)
    draw_shortest_distance(root, nodes, current_node.prev_node, start_index)

def main():
    # nodes = [Node((100, 350)), Node((300, 150)), Node((300, 650)),
    #           Node((600, 350))]
    
    # Node((position_of_the_node))
    # random generation:
    # nodes = [Node((randint(100, 1100), randint(100, 600))) for i in range(10)] 
    
    nodes = [Node((100, 350)), Node((400, 600)), Node((400, 100)), 
    Node((700, 150)), Node((400, 350)), Node((1000, 350))]
    
    # first parameter: total amount of lines
    # amount of nodes
    # random generation:
    # connections = generate_connections(30, len(nodes))
    connections = [(0, 1), (0, 2), (2, 3), (1, 4), (3, 5), (4, 5)]
    # assign the next node for every node
    assign_next_node(nodes, connections)

    # get the starting and ending node
    start_node_index, end_node_index = choose_start_and_end_node(nodes)
    # the cost to travel to the starting node is 0
    nodes[start_node_index].travel_cost = 0
    # calculating the travel costs beginning from the starting node
    calculate_travel_cost(nodes[start_node_index])

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Consolas", 30)

    window_size = (1200, 700)
    root = Root(window_size, "djikstra algorithm")

    while True:
        # checking if user exits the app
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # render
        root.get_surface().fill("white")
        # render the lines
        for line in connections:
            first_node = nodes[line[0]]
            second_node = nodes[line[1]]
            pygame.draw.polygon(root.get_surface(), ("grey"), (first_node.position, second_node.position), width=3)

        # render every node
        for index, node in enumerate(nodes):
            if index == start_node_index:
                node.render(root.get_surface(), 5, color="blue")
            elif index == end_node_index:
                node.render(root.get_surface(), 5, color="red")
            else:
                node.render(root.get_surface(), 5)
            # displaying the travel cost above the node
            text = font.render(str(round(node.travel_cost)), False, ("black"))
            root.get_surface().blit(text, (node.position[0], node.position[1] - 50))

        try:
            # display the shortest distance in green
            draw_shortest_distance(root, nodes, nodes[end_node_index], start_node_index)
            additional_text = font.render("Total cost: " + str(round(nodes[end_node_index].travel_cost)), False, ("blue"))
            root.get_surface().blit(additional_text, (10, 10))
        
        except:
            # thrown when there is no route from the start to the end point
            additional_text = font.render(str("No route from the start to the end point!"), False, ("darkred"))
            root.get_surface().blit(additional_text, (10, 10))

        root.update(60)

if __name__ == "__main__":
    main()
