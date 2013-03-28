"""
    2013-03-28
    Decorator that allows profiling nested functions.
"""
from functools import wraps
from unittest.case import TestCase
import time


class ProfilerRecord(object):

    def __init__(self, name, start_time, end_time):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.children = []

    def __repr__(self):
        return '{}: {} {} {} {}'.format(self.__class__.__name__, self.name,
                                        self.start_time, self.end_time,
                                        self.children)


class Profiler(object):

    _records = []

    @staticmethod
    def add_record(record):
        Profiler._records.append(record)

    @staticmethod
    def records():
        return Profiler._records

    @staticmethod
    def get_report():

        def record_start_time(profiler_record):
            return profiler_record.start_time

        records = sorted(Profiler._records, key=record_start_time)

        if len(records) == 1:
            return records[0]

        root = records[0]
        for i in range(1, len(records)):
            if records[i].start_time < records[i - 1].end_time:
                # Is a child of the previous record
                records[i - 1].children.append(records[i])
            else:
                # Is a sibling of the previous record, must find the parent.
                # Parent is the most recent previous record that
                # has end_time larger than the end_time of the current record.
                for j in range(i - 1, -1, -1):
                    if records[j].end_time >= records[i].end_time:
                        records[j].children.append(records[i])
                        break

        return root


def profiled(f):

    @wraps(f)
    def profiled_func(*args, **kwargs):
        f.start_time = time.clock()
        response = f(*args, **kwargs)
        f.end_time = time.clock()
        Profiler.add_record(ProfilerRecord(f.__name__, f.start_time, f.end_time))
        return response

    return profiled_func


class ProfilerTest(TestCase):

    def setUp(self):
        Profiler._records = []

    def test_simple_function(self):
        @profiled
        def simple_function():
            return 'result'

        test_start_time = time.clock()
        self.assertEqual('result', simple_function())

        last_record = Profiler.records()[-1]
        self.assertEqual('simple_function', last_record.name)
        self.assertLess(test_start_time, last_record.start_time)
        self.assertLess(last_record.start_time, last_record.end_time)
        self.assertLess(last_record.end_time, time.clock())

    def test_nested_functions(self):

        @profiled
        def sub_function():
            return 'sub_result'

        @profiled
        def main_function():
            return sub_function()

        test_start_time = time.clock()
        self.assertEqual('sub_result', main_function())

        main_record = Profiler.records()[-1]
        self.assertEqual('main_function', main_record.name)
        self.assertLess(test_start_time, main_record.start_time)
        self.assertLess(main_record.start_time, main_record.end_time)
        self.assertLess(main_record.end_time, time.clock())
        
        sub_record = Profiler.records()[-2]
        self.assertEqual('sub_function', sub_record.name)
        self.assertLess(test_start_time, sub_record.start_time)
        self.assertLess(sub_record.start_time, sub_record.end_time)
        self.assertLess(sub_record.end_time, time.clock())

        self.assertLess(main_record.start_time, sub_record.start_time)
        self.assertLess(sub_record.end_time, main_record.end_time)

    def test_report(self):

        @profiled
        def sub_function_1():
            pass

        @profiled
        def sub_function_2():
            pass

        @profiled
        def main_function():
            sub_function_1()
            sub_function_2()

        main_function()

        report = Profiler.get_report()
        self.assertIsInstance(report, ProfilerRecord)
        self.assertEqual('main_function', report.name)
        self.assertLess(report.start_time, report.end_time)
        self.assertEqual(2, len(report.children))
        self.assertEqual('sub_function_1', report.children[0].name)
        self.assertEqual('sub_function_2', report.children[1].name)
