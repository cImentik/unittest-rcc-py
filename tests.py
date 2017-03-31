# -*- encoding: utf-8 -*-

from unittest.mock import patch
import unittest
import importlib
import io
import os
import sys


class Task(unittest.TestCase):

    def __init__(self, test_name, solution_file, fixture_dir):
        super(Task, self).__init__(test_name)
        self.solution_file = solution_file.split('/')[-1][:-3]
        self.fixture_dir = fixture_dir

    def setUp(self):
        self.stdout_files = sorted(
            f for f in os.listdir(self.fixture_dir) if f.endswith('.a'))

    def test_task(self):
        for file_name in self.stdout_files:
            file_name = self.fixture_dir + '/' + file_name
            with self.subTest(file_name):
                self.wrap_check_task(file_name[:-2], file_name)

    def wrap_check_task(self, stdin_file, stdout_file):
        @patch('sys.stdin', open(stdin_file, 'r'))
        @patch('sys.stdout', io.StringIO())
        def check_task():
            with open(stdout_file, 'r') as answer:
                if self.solution_file in sys.modules:
                    importlib.reload(sys.modules[self.solution_file])
                else:
                    importlib.import_module(self.solution_file)
                self.assertEqual(
                    sys.stdout.getvalue().strip(),
                    ''.join(answer.readlines()).strip()
                )
                sys.stdin.close()
        check_task()

if __name__ == '__main__':
    solution_file = 'task'
    fixture_dir = 'tests'

    if len(sys.argv) == 2:
        solution_file = sys.argv[1]
    if len(sys.argv) == 3:
        fixture_dir = sys.argv[2]

    suite = unittest.TestSuite()
    suite.addTest(Task('test_task', solution_file, fixture_dir))
    runner = unittest.TextTestRunner()
    runner.run(suite)
