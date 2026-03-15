# Create a dictionary to store student names and marks
students = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "Diana": 88,
    "Ethan": 95
}
# 1. Print the dictionary
print("1. Original dictionary:")
print(students)
print()
# 2. Add a new student to the dictionary with their marks
students["Fiona"] = 90
print("2. After adding Fiona:")
print(students)
print()
# 3. Update the marks of an existing student
students["Charlie"] = 82
print("3. After updating Charlie's marks:")
print(students)
print()

# 4. Remove a student from the dictionary
removed_student = students.pop("Bob")
print(f"4. After removing Bob (who had {removed_student} marks):")
print(students)
print()
# 5. Print only the names of all students (keys)
print("5. Names of all students:")
for student in students.keys():
    print(student)
print()
# Alternative way using list of keys
print("Student names (alternative method):")
print(list(students.keys()))
print()

# 6. Print the average marks of all students
total_marks = sum(students.values())
number_of_students = len(students)
average_marks = total_marks / number_of_students

print("6. Average marks calculation:")
print(f"Total marks: {total_marks}")
print(f"Number of students: {number_of_students}")
print(f"Average marks: {average_marks:.2f}")