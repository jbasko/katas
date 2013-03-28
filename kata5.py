"""
    2013-03-28
    Decorator that allows profiling nested functions.
"""
import collections
from functools import wraps
from unittest.case import TestCase
import time

ProfilerRecord = collections.namedtuple('ProfilerRecord', ['name', 'start_time', 'end_time'])


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

        report = [records[0]]
        for i in range(1, len(records)):
            if records[i].start_time > report[-1].end_time:
                # [i] is a sibling of current item in the report
                report.append(records[i])
            elif records[i].start_time > records[i - 1].end_time:
                # [i] is a sibling of the previous record
                report.append(records[i])
            else:
                # [i] is a child of the previous record
                assert records[i].end_time < records[i - 1].end_time
                records[i - 1].children.append(records[i])
            pass

        return report


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

        #
        # Example of the expected report:
        #
        # expected_report = [{
        #     'name': 'main_function',
        #     'start_time': 0.0,
        #     'end_time': 0.0,
        #     'children': [{
        #         'name': 'sub_function_1',
        #         'start_time': 0.0,
        #         'end_time': 0.0
        #     }, {
        #         'name': 'sub_function_2',
        #         'start_time': 0.0,
        #         'end_time': 0.0
        #     }]
        # }]

        report = Profiler.get_report()
        self.assertIsInstance(report, list)
        self.assertEqual(1, len(report))
        self.assertEqual('main_function', report[0].name)
        self.assertLess(report[0].start_time, report[0].end_time)
        print report
        self.assertEqual(2, len(report[0].children))


