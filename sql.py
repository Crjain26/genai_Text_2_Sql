import sqlite3
connection=sqlite3.connect("EMPLOYEE.db")
cursor=connection.cursor()
table_info="""
Create table employee(NAME VARCHAR(25),BRANCH VARCHAR(25),
SECTION VARCHAR(25),Working_Hours INT,Project_Pending INT);

"""
cursor.execute(table_info)
cursor.execute('''Insert Into employee values('Karthikeyan Soundararajan sir','Database Engineer','Systems Software',70,2)''')
cursor.execute('''Insert Into employee values('Raunak','Artificial Intelligence','Intern',25,4)''')
cursor.execute('''Insert Into employee values('Anshul','Natural Language processing','Intern',23,3)''')
cursor.execute('''Insert Into employee values('Priyanshi','Machine Learning','Intern',22,5)''')
cursor.execute('''Insert Into employee values('Vishesh','Machine Learning','Intern',20,6)''')
cursor.execute('''Insert Into employee values('Vidhi ','Data Science','Intern',21,1)''')
cursor.execute('''Insert Into employee values('Rahul ','Data Science','Data Engineer',45,4)''')
cursor.execute('''Insert Into employee values('Raghav ','LLM','LLM Expert',80,7)''')
cursor.execute('''Insert Into employee values('Vaishali ','Software Development','Developer',65,8)''')
cursor.execute('''Insert Into employee values('Dhruv ','Mobile App Development','App Developer',21,1)''')
cursor.execute('''Insert Into employee values('Vansh ','Artificial Intelligence','Prompt Engineer',55,3)''')
cursor.execute('''Insert Into employee values('Virat ','Database','Database Engineer',57,6)''')
cursor.execute('''Insert Into employee values('Aditya ','MERN Developer','Intern',21,1)''')
cursor.execute('''Insert Into employee values('Naman ','Data Science','Data Engineer',58,3)''')


print("The inserted recorde are")
data=cursor.execute('''Select * From Employee''')
for row in data:
    print(row)

connection.commit()
connection.close()