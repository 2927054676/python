
class Student:
    def __init__(self, id, name, good, bad):
        self.id  = id
        self.name = name
        self.good = good
        self.bad = bad

def read():  # 文件操作
    try:
        with open("students.txt", "r") as file:
            students_data = file.readlines()
            students = {}
            for data in students_data:
                id, name, good, bad = data.strip().split(',')
                students[id] = Student(int(id), name, int(good), int(bad))
            return students
    except FileNotFoundError:
        return {}


def save(students):#保存
    with open("students.txt", "w") as file:
        for s in students.values():
            student_str = f"{s.id},{s.name},{s.good},{s.bad}\n"
            file.write(student_str)


