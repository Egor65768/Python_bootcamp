def different_numbers():
    n = int(input())
    res = set()
    for i in range(n):
        res.add(int(input()))
    print(len(res))


def main():
    different_numbers()


if __name__ == "__main__":
    main()
