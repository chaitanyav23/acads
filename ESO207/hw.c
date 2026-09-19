#include <stdio.h>

#define MAX 100
#define INF 999999

int adj[MAX][MAX];     
int weight[MAX][MAX];   
int pi[MAX];          
int dist[MAX];    
int visited[MAX];      

int pq[MAX];
int pq_size;


void initializePQ(int n) {
    for (int i = 0; i < n; i++) {
        pq[i] = i;
        dist[i] = INF;
        visited[i] = 0;
        pi[i] = -1; 
    }
    pq_size = n;
}

void decreaseKey(int v, int newDist) {
    dist[v] = newDist;
}

int extractMin(int n) {
    int minIndex = -1;
    for (int i = 0; i < n; i++) {
        if (!visited[pq[i]] && (minIndex == -1 || dist[pq[i]] < dist[pq[minIndex]])) {
            minIndex = i;
        }
    }
    visited[pq[minIndex]] = 1;
    return pq[minIndex];
}

void dijkstra(int n, int source) {
    initializePQ(n);
    decreaseKey(source, 0);

    for (int i = 0; i < n; i++) {
        int u = extractMin(n);
        for (int j = 0; adj[u][j] != -1; j++) {
            int v = adj[u][j];
            if (!visited[v] && dist[u] + weight[u][j] < dist[v]) {
                decreaseKey(v, dist[u] + weight[u][j]);
                pi[v] = u;
            }
        }
    }
}

void printSortedResults(int n) {
    int results[MAX][2];

    for (int i = 0; i < n; i++) {
        results[i][0] = i;  
        results[i][1] = dist[i]; 
    }

    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (results[j][1] > results[j + 1][1]) {
                int tempVertex = results[j][0];
                int tempDist = results[j][1];
                results[j][0] = results[j + 1][0];
                results[j][1] = results[j + 1][1];
                results[j + 1][0] = tempVertex;
                results[j + 1][1] = tempDist;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        printf("%d %d ", results[i][0], results[i][1]);
    }
}

int main() {
    int n, source;

    scanf("%d", &n);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < MAX; j++) {
            adj[i][j] = -1;     
            weight[i][j] = INF; 
        }
    }

    for (int i = 0; i < n; i++) {
        int index = 0;
        while (1) {
            int child, wt;
            scanf("%d", &child);
            if (child == -1) break;  
            scanf("%d", &wt);
            adj[i][index] = child;
            weight[i][index] = wt;
            index++;
        }
    }

    scanf("%d", &source);

    dijkstra(n, source);

    printSortedResults(n);

    return 0;
}
