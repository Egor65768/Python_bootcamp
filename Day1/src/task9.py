def derivative_at_point():
    list_date = input().split()
    n = int(list_date[0])
    x_0 = float(list_date[1])
    coefficient = list()
    for i in range(n + 1):
        coefficient.append(float(input()))
    coefficient.reverse()
    result = 0
    for i in range(n + 1):
        f = lambda x: coefficient[i] * i * (x ** (i - 1)) if i != 0 else 0
        result += f(x_0)
    print(f"{result:.3f}")


def main():
    derivative_at_point()


if __name__ == "__main__":
    main()
