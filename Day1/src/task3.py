def figures():
    my_file = open("task3/input.txt")
    k = 0
    matrix = list()
    for i in my_file:
        matrix.append(i.split())
    res = search_figures(matrix)
    print(res[0], res[1])
    my_file.close()


def search_figures(matrix):
    res = [0, 0]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "1":
                res[type_figure(matrix, i, j)] += 1
                floodFill(matrix, i, j)
    return res


# 1 - круг 0 - квадрат
def type_figure(matrix, i, j):
    if i + 1 < len(matrix) and j - 1 >= 0 and matrix[i + 1][j - 1] == "1":
        return 1
    return 0


def floodFill(matrix, i, j):
    if i < 0 or j < 0 or i >= len(matrix) or j >= len(matrix[i]) or matrix[i][j] != "1":
        return
    matrix[i][j] = "0"
    floodFill(matrix, i, j + 1)
    floodFill(matrix, i, j - 1)
    floodFill(matrix, i - 1, j)
    floodFill(matrix, i + 1, j)


def main():
    figures()


if __name__ == "__main__":
    main()
