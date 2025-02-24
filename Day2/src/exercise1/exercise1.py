import os
from random import randint, choice, uniform
from time import sleep
from threading import Thread, Lock
from prettytable import PrettyTable
from enum import Enum
from copy import copy


class Status(Enum):
    WAITING = "Очередь"
    COMPLETED = "Сдал"
    FAILED = "Провалил"

    def __str__(self):
        return self.value


class Column_names(Enum):
    NAME = 0
    STATUS = 1
    CURRENT_STUDENT = 1
    TOTAL_STUDENTS = 2
    FAILED_STUDENT = 3
    WORK_TIME = 4


class Student:
    def __init__(self, name: str, gender: str) -> None:
        self.name = name
        self.gender = gender
        self.status = Status.WAITING.value
        self.exam_time = 0


class Examiner:
    def __init__(self, name: str, gender: str) -> None:
        self.name = name
        self.len_name = len(self.name)
        self.gender = gender
        self.work_time = 0
        self.total_students = 0
        self.failed_students = 0
        self.number_of_lunches = 1

    def exam_passing(self, exam_status: bool, student: "Student") -> "Student":
        """Function of assigning a grade to an examiner to a student"""
        random_num = randint(1, 8)
        if random_num == 1:
            exam_status = False
        elif random_num <= 3:
            exam_status = True
        self.total_students += 1
        if not exam_status:
            self.failed_students += 1
        time_exam = uniform(self.len_name - 1, self.len_name + 1)
        self.work_time += time_exam
        self.work_time = round(self.work_time, 2)
        sleep(time_exam)
        student.status = Status.COMPLETED.value if exam_status else Status.FAILED.value
        student.exam_time = self.work_time
        return student


class Question:
    def __init__(self, txt: str):
        self.txt = txt.split()
        self.len_question = len(self.txt)
        self.total_students_correctly_answered = 0


def parsing() -> tuple:
    mf = open("students.txt")
    students = list()
    examiners = list()
    questions = dict()
    for i in mf:
        name, gender = map(str, i.split())
        students.append(Student(name, gender))
    mf.close()
    mf = open("examiners.txt")
    for i in mf:
        name, gender = map(str, i.split())
        examiners.append((Examiner(name, gender)))
    mf.close()
    mf = open("questions.txt")
    id_question = 0
    for i in mf:
        questions[id_question] = Question(i)
        id_question += 1
    return students, examiners, questions


def unpackaging_data(date_list) -> tuple:
    """
    The function unpacks data from a list
    :return: examiner, students, questions, number_of_students
    """
    return date_list[0], date_list[1], date_list[2], date_list[3]


def update_date(examiner: "Examiner", student: "Student") -> None:
    """Function for adding exam results to tables"""
    for i in range(len(students_table.rows)):
        if students_table.rows[i][Column_names.NAME.value] == student.name:
            students_table.rows[i][Column_names.STATUS.value] = student.status
            break
    for i in range(len(examiners_table.rows)):
        if examiners_table.rows[i][Column_names.NAME.value] == examiner.name:
            examiners_table.rows[i][
                Column_names.TOTAL_STUDENTS.value
            ] = examiner.total_students
            examiners_table.rows[i][
                Column_names.FAILED_STUDENT.value
            ] = examiner.failed_students
            examiners_table.rows[i][Column_names.WORK_TIME.value] = examiner.work_time


def input_current_student(examiner_name: str, student_name: str) -> None:
    """Writes down the examination student in the examiner's table"""
    for i in range(len(examiners_table.rows)):
        if examiners_table.rows[i][Column_names.NAME.value] == examiner_name:
            examiners_table.rows[i][Column_names.CURRENT_STUDENT.value] = student_name
            break


def input_current_exam_information(
    students: list, examiner: "Examiner", number_of_students: int
) -> None:
    os.system("cls" if os.name == "nt" else "clear")
    print(students_table)
    print(examiners_table)
    print(f"Осталось в очереди: {len(students)} из {number_of_students}")
    print(f"Время с момента начала экзамена: {examiner.work_time}")


def permission_to_retake() -> bool:
    res = [True, False, False]
    return choice(res)


def simulation_response(gender: str, len_question: int) -> int:
    """
    Simulation of answering a question
    Taking into account the fact that men more often choose the word
    at the beginning of the question as an answer, and women vice versa
    """
    simulation_list_numbers = [0]
    quantity = 1
    element_sim_list_numbers = 0
    while simulation_list_numbers[-1] != len_question - 1:
        if quantity >= len_question - element_sim_list_numbers:
            quantity = 0
            element_sim_list_numbers += 1
        simulation_list_numbers.append(element_sim_list_numbers)
        quantity += 1
    simulation_number = choice(simulation_list_numbers)
    if gender == "Ж":
        simulation_number = len_question - 1 - simulation_number
    return simulation_number


def lunch(examiner: list) -> None:
    """Lunch simulation function"""
    time_lunch = uniform(12, 18)
    sleep(time_lunch)
    examiner[0].number_of_lunches += 1


def exam_thread(date_list: list) -> None:
    """The main function in which each exam is simulated"""
    examiner, students, questions, number_of_students = unpackaging_data(date_list)
    correct_answers = 0
    student = students.pop(0)
    locker.acquire()
    input_current_student(examiner.name, student.name)
    input_current_exam_information(students, examiner, number_of_students)
    locker.release()
    for _ in range(3):
        id_question = choice(list(questions))
        student_answer = simulation_response(
            student.gender, questions[id_question].len_question
        )
        question_status = False
        while True:
            examiner_answer = simulation_response(
                examiner.gender, questions[id_question].len_question
            )
            if examiner_answer == student_answer:
                question_status = True
                break
            elif not permission_to_retake():
                break
        if question_status:
            questions[id_question].total_students_correctly_answered += 1
        correct_answers += 1 if question_status else -1
    exam_status = correct_answers > 0
    student = examiner.exam_passing(exam_status, student)
    date_list[0] = examiner
    date_list[1] = student
    locker.acquire()
    update_date(examiner, student)
    input_current_student(examiner.name, "-")
    input_current_exam_information(students, examiner, number_of_students)
    locker.release()


def paint_start_table(students: list, examiners: list) -> None:
    for student in students:
        students_table.add_row([student.name, str(student.status)])
    for examiner in examiners:
        examiners_table.add_row(
            [
                examiner.name,
                "-",
                examiner.total_students,
                examiner.failed_students,
                examiner.work_time,
            ]
        )
    print(students_table)
    print(examiners_table)


def exam_information(students: list, examiners: list, questions: dict) -> None:
    """Displaying final information about the exam"""
    exam_time = 0
    students_complete = 0
    fail_student = len(students)
    completed_question = 0
    best_questions = ""
    best_student = ""
    worst_student = ""
    best_examiner = ""
    students = sorted(students, key=lambda stud: stud.exam_time)
    examiners = sorted(examiners, key=lambda ex: ex.failed_students)
    for student in students:
        if not best_student and student.status == Status.COMPLETED.value:
            best_student = student.name
        elif not worst_student and student.status == Status.FAILED.value:
            worst_student = student.name
        if student.status == Status.COMPLETED.value:
            students_complete += 1
    for examiner in examiners:
        if examiner.work_time > exam_time:
            exam_time = examiner.work_time
        if fail_student > examiner.failed_students:
            fail_student = examiner.failed_students
            best_examiner = ""
            best_examiner += examiner.name
        elif fail_student == examiner.failed_students:
            best_examiner += ", " + examiner.name
    for question in questions.values():
        if completed_question < question.total_students_correctly_answered:
            best_questions = ""
            completed_question = question.total_students_correctly_answered
            best_questions += " ".join(question.txt)
        elif completed_question == question.total_students_correctly_answered:
            best_questions += ", " + " ".join(question.txt)
    print(f"Время с момента начала экзамена и до момента и его завершения: {exam_time}")
    print(f"Имена лучших студентов: {best_student}")
    print(f"Имена лучших экзаменаторов: {best_examiner}")
    print(f"Имена студентов, которых после экзамена отчислят: {worst_student}")
    print(f"Лучшие вопросы: {best_questions}")
    if students_complete / len(students) >= 0.85:
        print("Вывод: экзамен удался")
    else:
        print("Вывод: экзамен не удался")


def main():
    try:
        students, examiners, questions = parsing()
    except Exception:
        print("Ошибка в данных")
        return
    copy_stud = copy(students)
    number_of_students = len(students)
    paint_start_table(students, examiners)
    thread_dict = dict()
    for examiner in examiners:
        date_list = [examiner, students, questions, number_of_students]
        th = Thread(target=exam_thread, args=[date_list])
        thread_dict[examiner] = th
        if not students:
            break
    for th in thread_dict.values():
        th.start()
    while students:
        for examiner, th in thread_dict.items():
            if not th.is_alive():
                if examiner.work_time // 30 >= examiner.number_of_lunches:
                    date_list = [examiner]
                    th = Thread(target=lunch, args=[date_list])
                    thread_dict[examiner] = th
                    th.start()
                elif students:
                    date_list = [examiner, students, questions, number_of_students]
                    th = Thread(target=exam_thread, args=[date_list])
                    thread_dict[examiner] = th
                    th.start()
                    break
    for th in thread_dict.values():
        th.join()
    os.system("cls" if os.name == "nt" else "clear")
    examiners_table.del_column("Текущий студент")
    print(students_table)
    print(examiners_table)
    exam_information(copy_stud, examiners, questions)


students_table = PrettyTable()
examiners_table = PrettyTable()
examiners_table.field_names = [
    "Экзаменатор",
    "Текущий студент",
    "Всего студентов",
    "Завалил",
    "Время работы",
]
students_table.field_names = ["Студент", "Статус"]
order = {"Очередь": 1, "Сдал": 2, "Провалил": 3}
students_table.sortby = "Статус"
students_table.sort_key = lambda x: order.get(x[2])
locker = Lock()

if __name__ == "__main__":
    main()
