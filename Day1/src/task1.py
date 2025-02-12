def scalar_vector():
    a = input().split()
    b = input().split()
    if len(a) == len(b):
        result = 0
        for i in range(len(a)):
            result += float(a[i]) * float(b[i])
        print(result)


def main():
    scalar_vector()


if __name__ == "__main__":
    main()
