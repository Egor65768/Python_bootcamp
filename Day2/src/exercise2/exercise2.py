import asyncio
import aiohttp
import os
from prettytable import PrettyTable
import tempfile


async def read_input(queue):
    while True:
        user_input = await asyncio.get_event_loop().run_in_executor(
            None,
            input,
            "Введите ссылку на изображение (пустую строку для завершения): ",
        )
        if user_input == "":
            await queue.put(False)
            break
        await queue.put(user_input)
    os.system("cls" if os.name == "nt" else "clear")
    print("Идет загрузка оставшихся фотографий")


async def download_image(session, queue, status, save_path):
    while True:
        url = await queue.get()
        if not url:
            break
        file_name = save_path + os.path.basename(url)
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(file_name, "wb") as f:
                    f.write(await response.read())
                status[url] = "Успех"
        except aiohttp.ClientError:
            status[url] = "Ошибка"


async def main():
    queue = asyncio.Queue()
    while True:
        save_path = input("Введите путь для сохранения изображений: ")
        if os.path.isdir(save_path):
            try:
                test_file = tempfile.NamedTemporaryFile(dir=save_path, delete=True)
                break
            except Exception:
                print("Ошибка доступа к директории. Пожалуйста, введите другой.")
        else:
            print("Некорректный путь. Пожалуйста, введите другой.")
    async with aiohttp.ClientSession() as session:
        status_dict = dict()
        await asyncio.gather(
            read_input(queue), download_image(session, queue, status_dict, save_path)
        )
        os.system("cls" if os.name == "nt" else "clear")
        status_table = PrettyTable()
        status_table.field_names = ["Ссылка", "Статус"]
        for url, status in status_dict.items():
            status_table.add_row([url, status])
        print(status_table)


if __name__ == "__main__":
    asyncio.run(main())
