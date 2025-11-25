from pyvis.network import Network
import webbrowser
import os
import heapq

# ========================
# ฟังก์ชัน DFS
# ========================
def dfs_spanning_tree(N, adj, start):
    visited = [False] * (N+1)
    tree_edges = []

    def dfs(u):
        visited[u] = True
        for v, w in adj[u]:
            if not visited[v]:
                tree_edges.append((u, v, w))
                dfs(v)
    
    dfs(start)
    return tree_edges

# ========================
# ฟังก์ชัน BFS
# ========================
from collections import deque
def bfs_spanning_tree(N, adj, start):
    visited = [False] * (N+1)
    tree_edges = []
    q = deque([start])
    visited[start] = True

    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if not visited[v]:
                visited[v] = True
                tree_edges.append((u, v, w))
                q.append(v)
    return tree_edges

# ========================
# ฟังก์ชัน Dijkstra
# ========================
def dijkstra(N, adj, src, tgt):
    dist = [float('inf')] * (N+1)
    prev = [None] * (N+1)
    dist[src] = 0
    pq = [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    
    # สร้าง path
    path = []
    u = tgt
    while u is not None:
        path.append(u)
        u = prev[u]
    path.reverse()
    
    return dist[tgt], path

# ========================
# ฟังก์ชัน Prim's MST
# ========================
def prim_mst(N, edges):
    adj = [[] for _ in range(N+1)]
    for u,v,w in edges:
        adj[u].append((v,w))
        adj[v].append((u,w))
    
    visited = [False]*(N+1)
    pq = [(0,1,-1)]  # cost, node, parent
    mst_edges = []

    while pq:
        w,u,p = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        if p != -1:
            mst_edges.append((p,u,w))
        for v,c in adj[u]:
            if not visited[v]:
                heapq.heappush(pq,(c,v,u))
    return mst_edges

# ========================
# ฟังก์ชัน Kruskal's MST
# ========================
class DSU:
    def __init__(self, n):
        self.parent = list(range(n+1))
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        xr = self.find(x)
        yr = self.find(y)
        if xr == yr:
            return False
        self.parent[yr] = xr
        return True

def kruskal_mst(N, edges):
    edges_sorted = sorted(edges, key=lambda x: x[2])
    dsu = DSU(N)
    mst_edges = []
    for u,v,w in edges_sorted:
        if dsu.union(u,v):
            mst_edges.append((u,v,w))
    return mst_edges

# ========================
# ฟังก์ชัน PyVis
# ========================
def display_graph_interactive(N, edges):
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    for i in range(1, N+1):
        net.add_node(i, label=str(i))
    for u,v,w in edges:
        net.add_edge(u,v,value=w)
    html_file = "graph.html"
    net.show(html_file, notebook=False)
    webbrowser.open(f"file://{os.path.abspath(html_file)}")

# ========================
# ฟังก์ชัน Print Adjacency List
# ========================
def print_adj_list(N, adj):
    for u in range(1,N+1):
        print(f"{u}: {adj[u]}")

# ========================
# Main Program
# ========================
def main():
    print("Enter graph: first line 'N M', then M lines 'u v [w]'. Empty line to finish input.")
    first_line = input().strip()
    if not first_line:
        return
    N, M = map(int, first_line.split())
    edges = []
    adj = [[] for _ in range(N+1)]

    for _ in range(M):
        line = input().strip()
        if not line:
            break
        parts = list(map(int, line.split()))
        u,v,w = parts if len(parts)==3 else (*parts,1)
        edges.append((u,v,w))
        adj[u].append((v,w))
        adj[v].append((u,w))  # กราฟ undirected

    while True:
        print("\nSelect operation:")
        print("1) Spanning tree from source (DFS)")
        print("2) Spanning tree from source (BFS)")
        print("3) Shortest path (Dijkstra) from source to target")
        print("4) Prim's MST")
        print("5) Kruskal's MST")
        print("6) Display graph interactively")
        print("7) Print adjacency list")
        print("0) Exit")
        choice = input("Choice: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            s = int(input("Start node: "))
            tree = dfs_spanning_tree(N, adj, s)
            print("DFS Spanning Tree edges:", tree)
        elif choice == "2":
            s = int(input("Start node: "))
            tree = bfs_spanning_tree(N, adj, s)
            print("BFS Spanning Tree edges:", tree)
        elif choice == "3":
            s = int(input("Source node: "))
            t = int(input("Target node: "))
            dist, path = dijkstra(N, adj, s, t)
            print(f"Shortest path from {s} to {t}: {path} with distance {dist}")
        elif choice == "4":
            tree = prim_mst(N, edges)
            print("Prim's MST edges:", tree)
        elif choice == "5":
            tree = kruskal_mst(N, edges)
            print("Kruskal's MST edges:", tree)
        elif choice == "6":
            display_graph_interactive(N, edges)
            print("Graph displayed in browser.")
        elif choice == "7":
            print_adj_list(N, adj)
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
