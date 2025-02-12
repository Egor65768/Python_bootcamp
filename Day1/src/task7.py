def robot():
    N, M, matrix = input_date()
    print(max_coins(N, M, matrix))


def input_date():
    str_input = input().split()
    N, M = int(str_input[0]), int(str_input[1])
    matrix = list()
    for i in range(N):
        str_input = input().split()
        matrix.append([int(i) for i in str_input])
    return N, M, matrix


def max_coins(N, M, matrix):
    max_matrix = [[0 for j in range(M)] for i in range(N)]
    max_matrix[0][0] = matrix[0][0]
    for i in range(1, N):
        max_matrix[i][0] = max_matrix[i - 1][0] + matrix[i][0]
    for i in range(1, M):
        max_matrix[0][i] = max_matrix[0][i - 1] + matrix[0][i]
    for i in range(1, N):
        for j in range(1, M):
            max_matrix[i][j] = matrix[i][j] + max(
                max_matrix[i - 1][j], max_matrix[i][j - 1]
            )
    return max_matrix[N - 1][M - 1]


def main():
    robot()


if __name__ == "__main__":
    main()
