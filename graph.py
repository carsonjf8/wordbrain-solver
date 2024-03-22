# Graph data structure
# uses adjacency list representation
class Graph:
    # constructor
    def __init__(self, debug: bool = False) -> None:
        self.adj_list = {}
        self.debug = debug

    # add vertex (vertex_id must be unique)
    def add_vertex(self, vertex_id: str) -> None:
        if self.debug:
            print('adding vertext', vertex_id)
        self.adj_list[vertex_id] = []

    # add edge
    def add_edge(self, from_vertex_id: str, to_vertex_id: str) -> None:
        if self.debug:
            print('adding edge', from_vertex_id, to_vertex_id)
        # check that both vertices are in the graph
        if from_vertex_id not in self.adj_list or to_vertex_id not in self.adj_list:
            if self.debug:
                print('failed to add edge')
            return
        
        adj_vertices = self.adj_list[from_vertex_id]
        adj_vertices.append(to_vertex_id)
        self.adj_list[from_vertex_id] = adj_vertices
    
    # get list of vertices
    def get_vertices(self) -> list:
        return list(self.adj_list.keys())

    # get list of neighboring vertices for a vertex
    def get_adj_vertices(self, vertex_id) -> list:
        return self.adj_list[vertex_id]

    def print(self) -> None:
        for key in self.adj_list:
            print(key, self.adj_list[key])