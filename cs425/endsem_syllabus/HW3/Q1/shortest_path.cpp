#include <bits/stdc++.h>
using namespace std;

const string NODE_NAMES[] = {"A","B","C","D","E","F","G","H","J","K"};
const int N = 10;
map<string,int> nameToIdx;
vector<pair<int,int> > graph[N];

void buildNameMap() {
    for (int i = 0; i < N; i++)
        nameToIdx[NODE_NAMES[i]] = i;
}

void buildGraph() {
    graph[4].push_back(make_pair(6,1)); graph[6].push_back(make_pair(4,1)); // E-G
    graph[4].push_back(make_pair(0,1)); graph[0].push_back(make_pair(4,1)); // E-A
    graph[4].push_back(make_pair(3,5)); graph[3].push_back(make_pair(4,5)); // E-D
    graph[6].push_back(make_pair(7,1)); graph[7].push_back(make_pair(6,1)); // G-H
    graph[7].push_back(make_pair(3,1)); graph[3].push_back(make_pair(7,1)); // H-D
    graph[0].push_back(make_pair(1,1)); graph[1].push_back(make_pair(0,1)); // A-B
    graph[1].push_back(make_pair(2,1)); graph[2].push_back(make_pair(1,1)); // B-C
    graph[3].push_back(make_pair(1,1)); graph[1].push_back(make_pair(3,1)); // D-B
    graph[3].push_back(make_pair(9,1)); graph[9].push_back(make_pair(3,1)); // D-K
    graph[3].push_back(make_pair(2,2)); graph[2].push_back(make_pair(3,2)); // D-C
    graph[9].push_back(make_pair(8,1)); graph[8].push_back(make_pair(9,1)); // K-J
    graph[8].push_back(make_pair(2,4)); graph[2].push_back(make_pair(8,4)); // J-C
    graph[5].push_back(make_pair(2,3)); graph[2].push_back(make_pair(5,3)); // F-C
}

void printPath(const vector<int>& parent, int src, int dest) {
    if (dest == -1 || (dest != src && parent[dest] == -1)) {
        cout << "  No path found.\n";
        return;
    }
    vector<int> path;
    int v = dest;
    while (v != -1) {
        path.push_back(v);
        if (v == src) break;
        v = parent[v];
    }
    reverse(path.begin(), path.end());
    cout << "  Route : ";
    for (int i = 0; i < (int)path.size(); i++) {
        cout << NODE_NAMES[path[i]];
        if (i + 1 < (int)path.size()) cout << " -> ";
    }
    cout << "\n";
}

void dijkstra(int src, int dest) {
    vector<int> dist(N, INT_MAX), parent(N, -1);
    priority_queue<pair<int,int>, vector<pair<int,int> >, greater<pair<int,int> > > pq;
    dist[src] = 0;
    pq.push(make_pair(0, src));

    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        if (d > dist[u]) continue;

        for (int i = 0; i < (int)graph[u].size(); i++) {
            int v = graph[u][i].first;
            int w = graph[u][i].second;
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                parent[v] = u;
                pq.push(make_pair(dist[v], v));
            }
        }
    }

    cout << "\n+-- Dijkstra (Link State) ------------------+\n";
    if (dist[dest] == INT_MAX)
        cout << "  Destination unreachable.\n";
    else {
        cout << "  Cost  : " << dist[dest] << "\n";
        printPath(parent, src, dest);
    }
    cout << "+-------------------------------------------+\n";
}

void bellmanFord(int src, int dest) {
    vector<int> dist(N, INT_MAX), parent(N, -1);
    dist[src] = 0;

    vector<tuple<int,int,int> > edges;
    for (int u = 0; u < N; u++) {
        for (int i = 0; i < (int)graph[u].size(); i++) {
            int v = graph[u][i].first;
            int w = graph[u][i].second;
            edges.push_back(make_tuple(u, v, w));
        }
    }

    for (int i = 0; i < N - 1; i++) {
        for (int j = 0; j < (int)edges.size(); j++) {
            int u = get<0>(edges[j]);
            int v = get<1>(edges[j]);
            int w = get<2>(edges[j]);
            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                parent[v] = u;
            }
        }
    }

    for (int j = 0; j < (int)edges.size(); j++) {
        int u = get<0>(edges[j]);
        int v = get<1>(edges[j]);
        int w = get<2>(edges[j]);
        if (dist[u] != INT_MAX && dist[u] + w < dist[v]) {
            cout << "\n[Bellman-Ford] Negative cycle detected!\n";
            return;
        }
    }

    cout << "\n+-- Bellman-Ford (Distance Vector) ---------+\n";
    if (dist[dest] == INT_MAX)
        cout << "  Destination unreachable.\n";
    else {
        cout << "  Cost  : " << dist[dest] << "\n";
        printPath(parent, src, dest);
    }
    cout << "+-------------------------------------------+\n";
}

int main() {
    buildNameMap();
    buildGraph();

    cout << "Available nodes: ";
    for (int i = 0; i < N; i++) cout << NODE_NAMES[i] << " ";
    cout << "\n";

    string srcName, destName;
    cout << "Enter source node      : ";
    cin >> srcName;
    cout << "Enter destination node : ";
    cin >> destName;

    if (nameToIdx.find(srcName) == nameToIdx.end() ||
        nameToIdx.find(destName) == nameToIdx.end()) {
        cout << "Invalid node. Use one of: ";
        for (int i = 0; i < N; i++) cout << NODE_NAMES[i] << " ";
        cout << "\n";
        return 1;
    }

    int src  = nameToIdx[srcName];
    int dest = nameToIdx[destName];

    dijkstra(src, dest);
    bellmanFord(src, dest);

    return 0;
}
