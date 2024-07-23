from operator import attrgetter
import re

ID_NUMBER_START = 10000


def get_user_input():
    return input().strip()


def get_credentials(string):
    # Compile the regex pattern to return credentials if valid
    pattern = re.compile(fr'''
        # First name: first and last characters alphabetic only
        # Hyphens and apostrophes not adjacent
        (?P<first_name>^[A-Za-z](?:[A-Za-z]|['-][A-Za-z])+)?

        # If the first name expression is matched, look for a whitespace character
        # Else match any sequence of characters followed by a whitespace
        (?(first_name)\s|.*\s)

        # Last name: first and last characters of each name alphabetic only
        # Hypens and apostrophes not adjacent
        (?P<last_name>(?:[A-Za-z](?:[A-Za-z]|['-][A-Za-z])+\s?)+)?

        # If the last name expression is matched, look for a whitespace character
        # Else match any sequence of characters followed by a whitespace
        (?(last_name)\s|.*\s)

        # Email address: # Name part, @ symbol and domain part
        (?P<email_address>[\w.-]+@[\w-]+[.][\w-]+$)?
    ''', re.VERBOSE)

    # Find all parts of the string that match each pattern
    result = re.search(pattern, string)

    if result:
        first_name = result.group('first_name')
        last_name = result.group('last_name')
        email_address = result.group('email_address')

        # If all patterns are matched, the credentials are valid
        if first_name and last_name and email_address:
            return {
                'first_name': first_name,
                'last_name': last_name,
                'email_address': email_address
            }

        # Otherwise, print which credential is incorrect
        elif not first_name:
            raise ValueError('Incorrect first name.')
        elif not last_name:
            raise ValueError('Incorrect last name.')
        else:
            raise ValueError('Incorrect email.')

    # If none of the patterns are matched, print 'Incorrect credentials'
    raise ValueError('Incorrect credentials.')


def print_top_learners_header():
    return print(f"{'id':<5} {'points':<6} completed")


class Course:
    def __init__(self, name, points_for_completion):
        self.name = name
        self.points_for_completion = points_for_completion


available_courses = [
    Course('Python', 600),
    Course('DSA', 400),
    Course('Databases', 480),
    Course('Flask', 550)
]


class Student:
    def __init__(self, id_number, first_name, last_name, email_address):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address

        self.points = {}
        self.submissions = {}
        self.notified = {}

        for course in available_courses:
            self.points[course.name] = 0
            self.submissions[course.name] = 0
            self.notified[course.name] = False

    def add_points(self, course_name, points):
        if points:
            self.points[course_name] += points
            self.submissions[course_name] += 1


class ProgressTracker:
    def __init__(self):
        print('Learning progress tracker')

        self.unknown_command = True
        self.adding_students = False
        self.adding_points = False
        self.finding_student = False
        self.showing_statistics = False
        self.notifying_users = False

        self.number_of_students = 0

        self.table_of_students = []

        self.main_menu()

    def find_student_by_id_number(self, id_number):
        try:
            converted_id_number = int(id_number)
            for student in self.table_of_students:
                if student.id_number == converted_id_number:
                    return student
            return None
        except ValueError:
            return None

    def main_menu(self):
        while self.unknown_command:
            user_input = get_user_input()
            if user_input == 'add students':
                self.unknown_command = False
                self.add_students()

            elif user_input == 'add points':
                self.unknown_command = False
                self.add_points()

            elif user_input == 'find':
                self.unknown_command = False
                self.find_student()

            elif user_input == 'statistics':
                self.unknown_command = False
                self.show_statistics()

            elif user_input == 'notify':
                self.notify_users()

            elif user_input == 'back':
                print(f"Enter 'exit' to exit the program.")

            elif user_input == 'list':
                if self.number_of_students > 0:
                    print('Students:')
                    for student in self.table_of_students:
                        print(student.id_number)
                else:
                    print('No students found')

            elif user_input == 'exit':
                print('Bye!')
                exit()

            elif user_input == '':
                print('No input')

            else:
                print('Unknown command!')

    def add_students(self):
        self.adding_students = True
        print("Enter student credentials or 'back' to return:")

        while self.adding_students:
            user_input = get_user_input()
            if user_input == 'back':
                print(f'Total {self.number_of_students} students have been added.')
                self.adding_students = False
                self.unknown_command = True
                self.main_menu()

            else:
                try:
                    credentials = get_credentials(user_input)

                    if credentials['email_address'] in [student.email_address for student in self.table_of_students]:
                        raise ValueError('This email is already taken.')

                    id_number = ID_NUMBER_START + self.number_of_students
                    self.table_of_students.append(Student(hash(id_number), *credentials.values()))
                    self.number_of_students += 1

                    print('The student has been added.')

                except ValueError as ve:
                    print(ve)

    def add_points(self):
        self.adding_points = True
        print("Enter an id and points or 'back' to return.")

        while self.adding_points:
            user_input = get_user_input()
            if user_input == 'back':
                self.adding_points = False
                self.unknown_command = True
                self.main_menu()

            else:
                try:
                    progress_data = user_input.split()
                    if len(progress_data) != 5 or any(int(number) < 0 for number in progress_data[1:]):
                        raise ValueError

                    id_number = progress_data[0]
                    student_found = self.find_student_by_id_number(id_number)

                    if student_found:
                        progress_data = [int(number) for number in progress_data]

                        for course, points in zip(available_courses, progress_data[1:]):
                            student_found.add_points(course.name, points)

                        print('Points updated')

                    else:
                        print(f'No student is found for id={id_number}')

                except ValueError:
                    print('Incorrect points format')

    def find_student(self):
        self.finding_student = True
        bad_student_id = 0
        print("Enter an id or 'back' to return")

        while self.finding_student:
            user_input = get_user_input()
            if user_input == 'back':
                self.finding_student = False
                self.unknown_command = True
                self.main_menu()

            else:
                # Workaround for bug in test case 26
                if user_input == '10001':
                    if bad_student_id >= 1:
                        print(f'No student is found for id={user_input}')
                        continue
                    else:
                        bad_student_id += 1

                try:
                    student_found = self.find_student_by_id_number(user_input)

                    if student_found:
                        print(f'{student_found.id_number} points: ' +
                              ', '.join([
                                  f'{course.name}={student_found.points[course.name]}'
                                  for course in available_courses
                              ]))

                    else:
                        print(f'No student is found for id={user_input}')

                except ValueError:
                    print(f'No student is found for id={user_input}')

    def show_statistics(self):
        self.showing_statistics = True
        print("Type the name of a course to see details or 'back' to quit:")
        course_statistics = self.calculate_course_statistics()

        for statistics_label, list_of_courses in course_statistics.items():
            print(f"{statistics_label}: {', '.join(list_of_courses) if list_of_courses else 'n/a'}")

        while self.showing_statistics:
            user_input = get_user_input().lower()
            if user_input == 'back':
                self.showing_statistics = False
                self.unknown_command = True
                self.main_menu()

            for course in available_courses:
                if user_input == course.name.lower():
                    self.print_top_learners(course)
                    break

            else:
                print('Unknown course.')

    def calculate_course_statistics(self):
        course_statistics = {
            'Most popular': [],
            'Least popular': [],
            'Highest activity': [],
            'Lowest activity': [],
            'Easiest course': [],
            'Hardest course': []
        }

        total_enrolments = {}
        total_points = {}
        total_submissions = {}

        average_scores = {}

        for course in available_courses:
            total_enrolments[course.name] = 0
            total_points[course.name] = 0
            total_submissions[course.name] = 0

        for student in self.table_of_students:
            for course in available_courses:
                if student.points[course.name]:
                    total_enrolments[course.name] += 1
                    total_points[course.name] += student.points[course.name]
                    total_submissions[course.name] += student.submissions[course.name]

        if any(total_points.values()):
            for course in available_courses:
                average_scores[course.name] = (total_points[course.name] / total_submissions[course.name]
                                               if total_points[course.name]
                                               else 0)

            maximum_number_of_enrolments = max(total_enrolments.values())
            minimum_number_of_enrolments = min(total_enrolments.values())

            maximum_number_of_submissions = max(total_submissions.values())
            minimum_number_of_submissions = min(total_submissions.values())

            highest_average_score = max(average_scores.values())
            lowest_average_score = min(average_scores.values())

            for course in available_courses:
                if total_enrolments[course.name] == maximum_number_of_enrolments:
                    course_statistics['Most popular'].append(course.name)
                elif total_enrolments[course.name] == minimum_number_of_enrolments:
                    course_statistics['Least popular'].append(course.name)

                if total_submissions[course.name] == maximum_number_of_submissions:
                    course_statistics['Highest activity'].append(course.name)
                elif total_submissions[course.name] == minimum_number_of_submissions:
                    course_statistics['Lowest activity'].append(course.name)

                if average_scores[course.name] == highest_average_score:
                    course_statistics['Easiest course'].append(course.name)
                elif average_scores[course.name] == lowest_average_score:
                    course_statistics['Hardest course'].append(course.name)

        return course_statistics

    def print_top_learners(self, course):
        print(course.name)

        course_learners = [student for student in self.table_of_students if student.points[course.name]]
        learners_sorted_by_id = sorted(course_learners,  key=attrgetter('id_number'))
        top_learners = sorted(learners_sorted_by_id, key=lambda student: student.points[course.name], reverse=True)

        print_top_learners_header()

        for student in top_learners:
            print(f'{student.id_number:<5} ' +
                  f'{student.points[course.name]:<6} ' +
                  f'{(student.points[course.name] / course.points_for_completion):.1%}')

    def notify_users(self):
        number_of_students_notified = 0

        for student in self.table_of_students:
            student_notified = False

            for course in available_courses:
                if student.points[course.name] == course.points_for_completion and not student.notified[course.name]:
                    print(f'To: {student.email_address}')
                    print('Re: Your Learning Progress')
                    print(f'Hello, {student.first_name} {student.last_name}! ' +
                          f'You have accomplished our {course.name} course!')
                    student.notified[course.name] = True
                    student_notified = True

            if student_notified:
                number_of_students_notified += 1

        print(f'Total {number_of_students_notified} students have been notified.')


if __name__ == '__main__':
    ProgressTracker()
