class Queue():
    def __init__(self):
        self.vals = {}

    def insert(self,e):
        self.vals.append(e)

    def remove(self,e):
        try:
            self.vals.pop(e)
        except:
            raise ValueError(str(e) + 'not found')

    def __str__(self):
        return str(e) for e in self.vals

# encapsulation

class Grades(object):
    def __init__(self):
        self.students = []
        self.grades = {}
        self.isSorted = True

    def addStudent(self, student):
        if student in self.students:
            raise ValueError('duplicated student')
        self.students.append(student)
        self.grades[student.getIdNum()] = []
        self.isSorted = False

    def addGrade(self, student, grade):
        try:
            self.grades[student.getIdNum()].append(grade)
        except KeyError:
            raise ValueError('student not in grade book')

    def getGrades(self, student):
        try:
            return self.grades[student.getIdNum()][:]
        except KeyError:
            raise ValueError('Student not in grade book')

    def allStudents(self):
        if not self.isSorted:
            self.student.sort()
            self.isSorted = True
        return self.students[:]

def gradeReport(course):
    report = []
    for s in course.allStudents():
        tot = 0.0
        numGrades = 0
        for g in course.getGrades(s):
            tot += g
            numGrades += 1
        try:
            average = tot/numGrades
            report.append(str(s) + '\'s mean grade is ' + str(average))
        except ZeroDivisionError:
            report.append(str(s) + ' has no grades')
    return '\n'.join(report)
ug1 = UG('Jane Doe', 2014)
ug2 = UG('John Doe', 2015)
ug3 = UG('David Henry', 2003)
g1 = Grad('Billy Buckner')
g2 =  Grad('Bucky Dent')

six00 = Grades()
six00.addStudent(g1)
six00.addStudent(ug2)
six00.addStudent(ug1)
six00.addStudent(g2)

for s in six00.allStudents():
    six00.addGrade(s, 75)
six00.addGrade(g1,25)
six00.addGrade(g2,100)

six00.addStudent(ug3)

#data hiding
#inefficiency - generate a copy of the list