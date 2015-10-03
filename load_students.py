import csv
output = {"persons":[]}
with open("students.csv") as csv_file:
	for row in csv.reader(csv_file):
		id = row[0]
		output['persons'].append({
		"pk": int(id),
		"model": row[1],
		"fields":{
			"id_number":row[2],
			"first_name":row[4],
			"last_name":row[3],
			"course":row[5]
		}
	})

with open("json_data.txt","w") as text_file:
	text_file.write(''.join(map(str,output['persons'])));