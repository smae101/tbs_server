csv_filepathname = "students.csv"

from tbs.models import Student

import csv

dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
	student = Student()
	student.id_number = row[0]
	student.first_name = row[1]
	student.last_name = row[2]
	student.course = row[3]
	student.save()