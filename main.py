import sqlite3

from faker import Faker
# Faker is a really awesome library for generating random things

import random


def main():
    # Making Faker class object, that can generate names, places, text and etc
    fake = Faker()

    # Creating random advisors and students
    advisors = [(i, fake.name()) for i in range(1, 31)]
    students = [(i, fake.name(), random.randint(1, 30)) for i in range(1, 100)]

    # Opening database in the memory(you can use your own .db file if you want)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Creating and filling a database tables
    cursor.executescript(f'''
    CREATE TABLE IF NOT EXISTS Advisor(
        AdvisorID INTEGER NOT NULL,
        AdvisorName TEXT NOT NULL,
        PRIMARY KEY(AdvisorID)
    );

    CREATE TABLE IF NOT EXISTS Student(
        StudentID INTEGER NOT NULL,
        StudentName TEXT NOT NULL,
        AdvisorID INTEGER,
        FOREIGN KEY(AdvisorID) REFERENCES Advisor(AdvisorID),
        PRIMARY KEY(StudentID)
    );

    INSERT INTO Advisor(AdvisorID, AdvisorName) VALUES
    {','.join(map(str, advisors))};

    INSERT INTO Student(StudentID, StudentName, AdvisorID) VALUES
    {','.join(map(str, students))};
    ''')

    conn.commit()

    # Joining all students with their advisors
    query = '''
    SELECT Advisor.AdvisorID, Advisor.AdvisorName, 
           GROUP_CONCAT(Student.StudentID), GROUP_CONCAT(Student.StudentName)
    FROM Advisor
    LEFT JOIN Student ON Advisor.AdvisorID = Student.AdvisorID
    GROUP BY Advisor.AdvisorID, Advisor.AdvisorName
    ORDER BY Advisor.AdvisorID
    '''

    cursor.execute(query)

    data = cursor.fetchall()

    # Function for printing advisors info with their students info
    def print_advisors():
        for row in data:
            advisor_id, advisor_name, student_ids, student_names = row
            print(f'Advisor ID: {advisor_id} ')
            print(f'Advisor Name: {advisor_name} ')
            if student_ids:
                print(f'Student IDs: {student_ids} ')
                print(f'Student Names: {student_names} ')
            else:
                print('This advisor has no students :(')
            print('\n')

    print_advisors()

    conn.close()


if __name__ == '__main__':
    main()
