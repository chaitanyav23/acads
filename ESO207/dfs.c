#include <stdio.h>

#define MAX 100

int adj[MAX][MAX]; // Adjacency list
int start[MAX], finish[MAX], pi[MAX], color[MAX];
int stack[MAX], top = -1;
int clock = 0;

void push(int v) {
    stack[++top] = v;
}

int pop() {
    return stack[top--];
}

int peek() {
    return stack[top];
}

int isEmpty() {
    return top == -1;
}

void printDFS_Tree(int pi[], int n) {
    printf("DFS Tree (Parent -> Child relationships):\n");
    for (int i = 0; i < n; i++) {
        // If a vertex has a parent, print the parent-child relationship
        if (pi[i] != -1) {
            printf("%c -> %c\n", 'A' + pi[i], 'A' + i); // Convert indices to characters A, B, C...
        }
    }
}


void DFS(int v, int n) {
    push(v);
    while (!isEmpty()) {
        int u = peek();
        if (color[u] == 0) { // white
            start[u] = clock++;
            color[u] = 1; // gray
        }
        int flag = 0;

        // Explore neighbors in lexicographical order by pushing them in reverse order
        for (int i = n - 1; i >= 0; i--) {
            int w = adj[u][i];
            if (w != -1 && color[w] == 0) {  // Only consider unvisited neighbors
                push(w);
                pi[w] = u;
                flag = 1;
                break;
            }
        }

        if (!flag) {
            if (color[u] == 1) {
                color[u] = 2; // black
                finish[u] = clock++;
            }
            pop();
        }
    }
}

void DFS_Explore(int n) {
    for (int i = 0; i < n; i++) {
        start[i] = -1;
        finish[i] = -1;
        pi[i] = -1;
        color[i] = 0; // white
    }

    for (int v = 0; v < n; v++) {
        if (start[v] == -1) {
            DFS(v, n);
        }
    }

    // Print results
    printf("Vertex\tStart\tFinish\tPi\n");
    for (int i = 0; i < n; i++) {
        printf("%c\t%d\t%d\t%c\n", 'A' + i, start[i], finish[i], pi[i] == -1 ? '-' : 'A' + pi[i]);
    }
    printDFS_Tree(pi, n);
}

int main() {
    int n = 10; // Number of vertices
    // Adjacency list based on Figure 1 from the PDF
    int edges[10][4] = {
        {1, 2, 3, -1},    // A -> B, C, D
        {6, -1, -1, -1},   // B -> G
        {1, -1, -1, -1},   // C -> B
        {4, 9, -1, -1}, // D -> E, J
        {5, -1, -1, -1},   // E -> F
        {4, -1, -1, -1}, // F -> E
        {2, -1, -1, -1},   // G -> C
        {9, -1, -1, -1},  // H -> J
        {7, 9, -1, -1},  // I -> H, J
        {0, -1, -1, -1} // J -> A
    };

    // Sort each row of adjacency list lexicographically
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < 4; j++) {
            adj[i][j] = edges[i][j];
        }
    }

    DFS_Explore(n);
    return 0;
}
