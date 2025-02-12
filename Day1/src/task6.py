import json


def movies():
    try:
        file = open("task6/input.txt", "r")
        date = json.loads(file.read())
        file.close()
        result = json.dumps({"list0": merge(date["list1"], date["list2"])}, indent=2)
    except json.decoder.JSONDecodeError:
        print("Код введен не в формате JSON")
        return
    except KeyError:
        print("Ошибка в данных")
        return
    except FileNotFoundError:
        print("Файл не найден")
        return
    print(result)


def merge(list1, list2):
    merger_list = list()
    i, j = 0, 0
    while i < len(list1) and j < len(list2):

        if list1[i]["year"] < list2[j]["year"]:
            merger_list.append(list1[i])
            i += 1
        else:
            merger_list.append(list2[j])
            j += 1
    while i < len(list1):
        merger_list.append(list1[i])
        i += 1
    while j < len(list2):
        merger_list.append(list2[j])
        j += 1
    return merger_list


def main():
    movies()


if __name__ == "__main__":
    main()
