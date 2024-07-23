import unittest
from unittest import mock

import task


class TestProgressTracker(unittest.TestCase):
    @mock.patch('task.input', create=True)
    def test_get_user_input(self, mocked_input):
        # Tests for the get_user_input() function
        mocked_input.side_effect = ['   add students    ', 'Test']

        result = task.get_user_input()
        self.assertEqual(result, 'add students')

        result = task.get_user_input()
        self.assertEqual(result, 'Test')

    def test_get_credentials(self):
        # Tests for the get_credentials() function
        self.assertTrue(task.get_credentials('John Doe jdoe@mail.net'))
        self.assertTrue(task.get_credentials('Jane Doe jane.doe@yahoo.com'))
        self.assertTrue(task.get_credentials('Jean-Clause van Helsing jc@google.it'))
        self.assertTrue(task.get_credentials('Mary Luise Johnson maryj@google.com'))

        with self.assertRaises(ValueError, msg='Incorrect credentials.'):
            task.get_credentials('help')

        with self.assertRaises(ValueError, msg='Incorrect email.'):
            task.get_credentials('John Doe email')

        with self.assertRaises(ValueError, msg='Incorrect first name.'):
            task.get_credentials('J. Doe name@domain.com')

        with self.assertRaises(ValueError, msg='Incorrect first name.'):
            task.get_credentials("nam-'e surname email@email.xyz")

        with self.assertRaises(ValueError, msg='Incorrect last name.'):
            task.get_credentials('John D. name@domain.com')

        with self.assertRaises(ValueError, msg='Incorrect first name.'):
            task.get_credentials('陳 港 生')

    def test_student_add_points(self):
        # Test for the Student.add_points() function
        student_object = task.Student(10000, 'John', 'Doe', 'jdoe@email.net')

        student_object.add_points(0, 3, 4, 0)

        self.assertEqual(student_object.points['Python'], 0)
        self.assertEqual(student_object.points['DSA'], 3)
        self.assertEqual(student_object.points['Databases'], 4)
        self.assertEqual(student_object.points['Flask'], 0)

        self.assertEqual(student_object.submissions['Python'], 0)
        self.assertEqual(student_object.submissions['DSA'], 1)
        self.assertEqual(student_object.submisisons['Databases'], 1)
        self.assertEqual(student_object.submissions['Flask'], 0)


if __name__ == '__main__':
    unittest.main()
