def string_to_number():
    number = input()
    if not validateNumberString(number):
        print("Error")
        return
    sign = 1
    if number[0] == "-":
        sign = -1
        number = number[1:]
    elif number[0] == "+":
        number = number[1:]
    decimal = 0
    flag = False
    pow_ten = 1
    for i in number:
        if i == ".":
            flag = True
            continue
        if not flag:
            decimal = decimal * 10 + ord(i) - 48
        else:
            decimal = decimal + (ord(i) - 48) / (10**pow_ten)
            pow_ten += 1

    decimal *= 2 * sign
    return decimal


def validateNumberString(number):
    if number is None or number == "":
        return False
    point = False
    decimal = True
    if number[0] in ("-", "+"):
        number = number[1:]
    for i in number:
        if not (48 <= ord(i) <= 57):
            if i == "." and not point:
                point = True
            else:
                decimal = False
    return decimal


def main():
    decimal = string_to_number()
    print(f"{decimal:.3f}")


if __name__ == "__main__":
    main()
