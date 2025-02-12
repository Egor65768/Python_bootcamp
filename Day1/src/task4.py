def pascal_triangle():
    try:
        n = int(input())
        if n <= 0:
            raise ValueError
    except ValueError:
        print("Введите целое число")
        return
    matrix = [[1]]
    for i in range(1, n):
        new_matrix = [1] * (i + 1)
        for j in range(i - 1):
            new_matrix[j + 1] = matrix[i - 1][j] + matrix[i - 1][j + 1]
        matrix.append(new_matrix)
    show(matrix)


def show(matrix):
    print()
    for i in matrix:
        for j in i:
            print(j, end=" ")
        print()


def main():
    pascal_triangle()


if __name__ == "__main__":
    main()
