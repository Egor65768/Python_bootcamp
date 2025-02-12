def palindrome():
    a = int(input())
    b = a
    result = False
    reverse_num = 0
    while a > 0:
        reverse_num = reverse_num * 10 + a % 10
        a = a // 10
    if reverse_num == b:
        result = True
    return result


def main():
    print(palindrome())


if __name__ == "__main__":
    main()
