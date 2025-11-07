"""
Graph Algorithms Toolkit (Interactive Version with PyVis)
Supports:
1) Spanning tree from a given source using DFS or BFS
2) Shortest path (Dijkstra) between given source and target
3) Minimum Spanning Tree (Prim and Kruskal)
4) Display graph interactively using pyvis

Input format (interactive / batch friendly):
First line: N M
Next M lines: u v [w]
 - u, v are vertex indices (1..N)
 - w is optional weight (if omitted, weight = 1)
Graph is treated as undirected for MST and as specified for searches.
"""

import sys
import heapq
from collections import deque
from pyvis.network import Network

# ---------- Utilities ----------

def read_graph():
    data = []
    print("Enter graph: first line 'N M', then M lines 'u v [w]'. Empty line to finish input.")
    try:
        first = input().strip()
    except EOFError:
        sys.exit("No input provided.")
    while first == "":
        try:
            first = input().strip()
        except EOFError:
            sys.exit("No input provided.")
    parts = first.split()
    if len(parts) < 2:
        sys.exit("First line must contain N and M")
    N = int(parts[0])
    M = int(parts[1])
    edges = []
    adj = [[] for _ in range(N+1)]
    for i in range(M):
        try:
            line = input().strip()
        except EOFError:
            sys.exit(f"Expected {M} edges, got {i}.")
        while line == "":
            line = input().strip()
        p = line.split()
        if len(p) < 2:
            sys.exit(f"Edge line must have at least u v: got '{line}'")
        u = int(p[0]); v = int(p[1])
        w = float(p[2]) if len(p) >= 3 else 1.0
        edges.append((u, v, w))
        adj[u].append((v, w))
        adj[v].append((u, w))
    return N, edges, adj

# ---------- 1. Spanning tree via DFS or BFS ----------

def spanning_tree_dfs(N, adj, src):
    visited = [False] * (N+1)
    parent = [-1] * (N+1)
    tree_edges = []

    sys.setrecursionlimit(10000)
    def dfs(u):
        visited[u] = True
        for v, _ in adj[u]:
            if not visited[v]:
                parent[v] = u
                tree_edges.append((u, v))
                dfs(v)
    parent[src] = 0
    dfs(src)
    return parent, tree_edges

def spanning_tree_bfs(N, adj, src):
    visited = [False] * (N+1)
    parent = [-1] * (N+1)
    tree_edges = []
    q = deque([src])
    visited[src] = True
    parent[src] = 0
    while q:
        u = q.popleft()
        for v, _ in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                tree_edges.append((u, v))
                q.append(v)
    return parent, tree_edges

# ---------- 2. Dijkstra's shortest path ----------

def dijkstra(N, adj, src, target=None):
    dist = [float('inf')] * (N+1)
    parent = [-1] * (N+1)
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if target is not None and u == target:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, parent

# ---------- 3. Prim's MST ----------

def prim_mst(N, adj):
    visited = [False] * (N+1)
    parent = [-1] * (N+1)
    key = [float('inf')] * (N+1)
    total_weight = 0.0
    edges_in_mst = []
    start = 1
    key[start] = 0
    pq = [(0, start)]
    while pq:
        k, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        total_weight += k
        if parent[u] != -1:
            edges_in_mst.append((parent[u], u, k))
        for v, w in adj[u]:
            if not visited[v] and w < key[v]:
                key[v] = w
                parent[v] = u
                heapq.heappush(pq, (w, v))
    if not all(visited[1:]):
        return None, None
    return total_weight, edges_in_mst

# ---------- Kruskal's MST ----------

class DSU:
    def __init__(self, n):
        self.parent = list(range(n+1))
        self.rank = [0] * (n+1)
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a, b):
        ra = self.find(a); rb = self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

def kruskal_mst(N, edges):
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DSU(N)
    mst_edges = []
    total = 0.0
    for u, v, w in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total += w
            if len(mst_edges) == N-1:
                break
    if len(mst_edges) != N-1:
        return None, None
    return total, mst_edges

# ---------- Helper to print path ----------

def reconstruct_path(parent, src, target):
    if parent[target] == -1 and src != target:
        return None
    path = []
    cur = target
    while cur != 0 and cur != -1:
        path.append(cur)
        if cur == src:
            break
        cur = parent[cur]
    path.reverse()
    if path and path[0] == src:
        return path
    return None

# ---------- Display graph with PyVis ----------

def display_graph_interactive(N, edges, highlight_edges=None, source=None, target=None):
    net = Network(height='600px', width='100%', notebook=False)
    for i in range(1, N+1):
        color = 'skyblue'
        if i == source:
            color = 'green'
        elif i == target:
            color = 'red'
        net.add_node(i, label=str(i), color=color)
    for u, v, w in edges:
        color = 'gray'
        width = 2
        if highlight_edges and ((u,v) in highlight_edges or (v,u) in highlight_edges):
            color = 'orange'
            width = 4
        net.add_edge(u, v, value=w, title=str(w), color=color, width=width)
    net.show("graph.html")
    print("Graph displayed in 'graph.html' – เปิดไฟล์นี้ใน browser เพื่อดู interactive graph")

# ---------- Main interactive menu ----------

def main():
    N, edges, adj = read_graph()
    while True:
        print('\nSelect operation:')
        print('1) Spanning tree from source (DFS)')
        print('2) Spanning tree from source (BFS)')
        print('3) Shortest path (Dijkstra) from source to target')
        print('4) Prim\'s MST')
        print('5) Kruskal\'s MST')
        print('6) Display graph interactively')
        print('7) Print adjacency list')
        print('0) Exit')
        choice = input('Choice: ').strip()
        if choice == '0':
            print('Bye')
            break
        if choice == '1' or choice == '2':
            s = int(input('Enter source vertex: ').strip())
            if not (1 <= s <= N):
                print('Invalid source')
                continue
            if choice == '1':
                parent, tree_edges = spanning_tree_dfs(N, adj, s)
                print(f'DFS spanning tree edges (parent -> child):')
            else:
                parent, tree_edges = spanning_tree_bfs(N, adj, s)
                print(f'BFS spanning tree edges (parent -> child):')
            for u, v in tree_edges:
                print(f'{u} -> {v}')
            unreachable = [i for i in range(1, N+1) if parent[i] == -1]
            if unreachable:
                print('Unreachable vertices from source:', unreachable)
            # Display interactive graph
            display_graph_interactive(N, edges, highlight_edges=tree_edges, source=s)
        elif choice == '3':
            s = int(input('Enter source vertex: ').strip())
            t = int(input('Enter target vertex: ').strip())
            dist, parent = dijkstra(N, adj, s, t)
            if dist[t] == float('inf'):
                print(f'No path from {s} to {t}')
            else:
                path = reconstruct_path(parent, s, t)
                print(f'Shortest distance {s} -> {t} = {dist[t]}')
                print('Path:', ' -> '.join(map(str, path)))
                # Highlight shortest path
                path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                display_graph_interactive(N, edges, highlight_edges=path_edges, source=s, target=t)
        elif choice == '4':
            res = prim_mst(N, adj)
            if res[0] is None:
                print('Graph is not connected; Prim cannot produce MST')
            else:
                total, mst_edges = res
                print(f"Prim's MST total weight = {total}")
                for u, v, w in mst_edges:
                    print(f'{u} - {v} : {w}')
                display_graph_interactive(N, edges, highlight_edges=[(u,v) for u,v,w in mst_edges])
        elif choice == '5':
            total, mst_edges = kruskal_mst(N, edges)
            if total is None:
                print('Graph is not connected; Kruskal cannot produce MST')
            else:
                print(f"Kruskal's MST total weight = {total}")
                for u, v, w in mst_edges:
                    print(f'{u} - {v} : {w}')
                display_graph_interactive(N, edges, highlight_edges=[(u,v) for u,v,w in mst_edges])
        elif choice == '6':
            display_graph_interactive(N, edges)
        elif choice == '7':
            print('Adjacency list:')
            for i in range(1, N+1):
                print(i, '->', adj[i])
        else:
            print('Invalid choice')

if __name__ == '__main__':
    main()
