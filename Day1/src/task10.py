def machines():
    info = input().split()
    try:
        available_devices = int(info[0])
        required_time = int(info[1])
    except ValueError:
        print("Введите натуральное число")
        return
    except IndexError:
        print("Введены не все данные")
        return
    if available_devices < 0 or required_time < 0:
        print("Введите натуральное число")
        return
    my_table = list()
    try:
        for i in range(available_devices):
            device_info = input().split()
            device_info_table = [int(i) for i in device_info]
            if (
                device_info_table[0] < 0
                or device_info_table[1] < 0
                or device_info_table[2] < 0
            ):
                print("Введите натуральное число")
                return
            my_table.append(device_info_table)
    except ValueError:
        print("Введите натуральное число")
        return
    except IndexError:
        print("Введены не все данные")
        return
    my_table = sorted(my_table, key=lambda x: (x[0], x[2], x[1]))
    if len(my_table) <= 1:
        print("Некоректные данные")
        return
    device_index = 0
    while my_table[device_index][0] != my_table[device_index + 1][0]:
        device_index += 1
    min_required_time = my_table[device_index][2] + my_table[device_index + 1][2]
    res_price = my_table[device_index][1] + my_table[device_index + 1][1]
    for device_index in range(available_devices - 1):
        if my_table[device_index][0] == my_table[device_index + 1][0]:
            work_time = my_table[device_index][2] + my_table[device_index + 1][2]
            price = my_table[device_index][1] + my_table[device_index + 1][1]
            if required_time <= work_time < min_required_time:
                min_required_time = work_time
                res_price = price
            elif (
                work_time >= required_time
                and work_time == min_required_time
                and res_price > price
            ):
                min_required_time = work_time
                res_price = price
    return res_price


def main():
    print(machines())


if __name__ == "__main__":
    main()
