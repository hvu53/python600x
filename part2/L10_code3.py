import datetime

class Person(object):
    def __init__(self, name):
        self.name = name
        self.birthday = None
        self.lastName = name.split(' ')[-1]

    def getLastName(self):
        return self.lastName

    def setBirthday(self, month, day,year):
        self.birthday = datetime.date(year,month,day)

    def getAge(self):
        if self.birthday == None:
            raise ValueError
        return (datetime.date.today() - self.birthday).days

    def __lt__(self, other):
        if self.lastName == other.lastName:
            return self.name < other.name
        return self.lastName < other.lastName

    def __str__(self):
        return self.name

class MITPerson(Person):
    nextIdNum = 0

    def __init__(self, name):
        Person.__init__(self, name)
        self.idNum = MITPerson.nextIdNum
        MITPerson.nextIdNum += 1

    def getIdNum(self):
        return self.idNum

class UG(MITPerson):
    def __init__(self, name, classYear):
        MITPerson.__init__(self, name)
        self.year = classYear

    def getClass(self):
        return self.year()

class Grad(MITPerson):
    pass

def isStudent(obj):
    return isinstance(obj, UG) or isinstance(obj, Grad)

class Grades(object):
    def __init__(self):
        self.students = [] # list of student objects
        self.grades = {} # maps idNum --> list of grades
        self.isSorted = True # true of self.students is sorted

    def addStudent(self, student):
        if student in self.students:
            raise ValueError('Duplicate student')
        self.students.append(student)
        self.grades[student.getIdNum()] = []
        self.isSorted = False

    def addGrade(self, student, grade):
        try:
            self.grades[student.getIdNum()].append(grade)
        except KeyError:
            raise ValueError('Student not in grade book')

    def getGrades(self, student):
        try:
            return self.grades[student.getIdNum()][:]
        except KeyError:
            raise ValueError('Student not in gradebook')

    def allStudents(self):
        if not self.isSorted:
            self.students.sort()
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
            avg = tot/numGrades
            report.append(str(s) + '\'s mean grade is ' + str(avg))
        except ZeroDivisionError:
                report.append(str(s) + ' has no grades')
    return '\n'.join(report)

        
ug1 = UG('Jane Doe', 2014)
ug2 = UG('John Doe', 2015)
ug3 = UG('David Henry', 2003)
g1 = Grad('Billy Buckner')
g2 = Grad('Bucky F. Dent')

six00 = Grades()
six00.addStudent(g1)
six00.addStudent(ug2)
six00.addStudent(ug1)
six00.addStudent(g2)

for s in six00.allStudents():
    six00.addGrade(s, 75)
    print str(s)+ ' ' + str(six00.getGrades(s))

six00.addGrade(g1, 25)
six00.addGrade(g2, 100)

six00.addStudent(ug3)

print gradeReport(six00)
