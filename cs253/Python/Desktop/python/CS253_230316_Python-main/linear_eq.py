import numpy as np
import sys


def inverse_matrix(a):
    try:
        inverse = np.linalg.inv(a)
        return inverse
    except np.linalg.LinAlgError:
        print("\nError: The matrix is singular and cannot be inverted. Program will stop.\n")
        sys.exit(1)        



def get_n_by_n_matrix(n,m):
    while True:
        try:
            if n <= 0:
                print("\nPlease enter a positive integer for the size.")
            else:
                break
        except ValueError:
            print("\nInvalid input. Please enter an integer.")

    matrix_list = []
    print(f"\nEnter the elements of the {n}x{n} matrix row by row:")
    for i in range(m):
        row = []
        while len(row) < n:
            try:
                row_input = input(f"\nEnter space-separated elements for row {i + 1}: ").split()
                row_elements = [float(elem) for elem in row_input]
                if len(row_elements) == n:
                    row = row_elements
                else:
                    print(f"\nPlease enter exactly {n} elements for this row.")
            except ValueError:
                print("\nInvalid input. Please enter numbers separated by spaces.")
        matrix_list.append(row)
    
    matrix = np.array(matrix_list)

    print("\nThe entered matrix (as NumPy array) is:")
    print(matrix)


    return matrix


def solve(a,b):
    try:
        X = np.dot(a,b)
        print("\nThe solution to the system of linear equations is\n")
        print(X)
    except ValueError as e:
        print(f"ValueError during np.dot: {e}")

def main():
    print("\nLet us start with Matrix A")
    n = int(input("\nEnter the size of the square matrix (n): "))
    A = get_n_by_n_matrix(n,n)

    A_inv = inverse_matrix(A)

    print("\nMoving on to matrix B")
    B = get_n_by_n_matrix(1,n)

    solve(A_inv,B)


if __name__ == "__main__":
    main()