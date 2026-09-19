#include <stdio.h>

#define MAX_VERTICES 9
#define MAX_EDGES 12

// Adjacency list representation using arrays
char adjList[MAX_EDGES];  // Array to store adjacent vertices
int start[MAX_VERTICES];  // Array to store start index of each vertex in adjList
int degree[MAX_VERTICES]; // Array to store degree (number of outgoing edges) for each vertex

// Function to add a directed edge (src -> dest)
void addEdge(char src, char dest) {
    // Add edge from src to dest
    adjList[start[src - 'A'] + degree[src - 'A']] = dest;
    degree[src - 'A']++;
}

// Function to initialize the adjacency list
void initializeGraph() {
    // Initialize start positions based on the maximum number of edges each vertex can have
    start[0] = 0;
    for (int i = 1; i < MAX_VERTICES; i++) {
        start[i] = start[i-1] + MAX_EDGES / MAX_VERTICES; // Evenly divide the space for edges
    }
    
    // Initialize degrees to 0
    for (int i = 0; i < MAX_VERTICES; i++) {
        degree[i] = 0;
    }
}

// Function to print the adjacency list
void printGraph() {
    for (int i = 0; i < MAX_VERTICES; i++) {
        printf("Adjacency list of vertex %c:\n", i + 'A');
        for (int j = 0; j < degree[i]; j++) {
            printf(" -> %c", adjList[start[i] + j]);
        }
        printf("\n");
    }
}

int main() {
    initializeGraph();

    // Add directed edges
    addEdge('A', 'B');
    addEdge('A', 'D');
    addEdge('A', 'E');
    addEdge('B', 'C');
    addEdge('B', 'D');
    addEdge('C', 'D');
    addEdge('C', 'A');
    addEdge('E', 'D');
    addEdge('E', 'F');
    addEdge('G', 'H');
    addEdge('G', 'I');
    addEdge('H', 'F');

    // Print the adjacency list
    printGraph();

    return 0;
}
