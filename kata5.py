"""
    2013-03-28
    Decorator that allows profiling nested functions.
"""
from functools import wraps
from unittest.case import TestCase
import time


class ProfilerRecord(object):

    def __init__(self, name, start_time, end_time,
                 func_args=None, func_kwargs=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.children = []
        self.func_args = [str(a) for a in func_args]
        self.func_kwargs = {str(k): str(v) for k, v in func_kwargs.items()}

    def __repr__(self):
        args_repr = []
        if self.func_args:
            args_repr.append(str(self.func_args))
        if self.func_kwargs:
            args_repr.append(str(self.func_kwargs))
        return '{}: {} {} {} {} {}'.format(self.__class__.__name__, self.name,
                                           ', '.join(args_repr),
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
    def flush_report():
        report = Profiler.get_report()
        Profiler._records = []
        return report

    @staticmethod
    def get_report():

        def record_start_time(profiler_record):
            return profiler_record.start_time

        records = sorted(Profiler._records, key=record_start_time)

        if not records:
            return []

        if len(records) == 1:
            return [records[0]]

        report = [records[0]]
        for i in range(1, len(records)):
            if records[i].start_time < records[i - 1].end_time:
                # Is a child of the previous record
                records[i - 1].children.append(records[i])
            else:
                # Is a sibling of the previous record, must find the parent.
                # Parent is the most recent previous record that
                # has end_time larger than the end_time of the current record.
                parent_found = False
                for j in range(i - 1, -1, -1):
                    if records[j].end_time >= records[i].end_time:
                        records[j].children.append(records[i])
                        parent_found = True
                        break
                if not parent_found:
                    report.append(records[i])

        return report


def profiled(f):

    @wraps(f)
    def profiled_func(*args, **kwargs):
        f.start_time = time.clock()
        try:
            response = f(*args, **kwargs)
            return response
        finally:
            f.end_time = time.clock()
            if args and hasattr(args[0], f.__name__) and callable(getattr(args[0], f.__name__)):
                # This is a heuristic check whether the first arg is 'self'
                reported_args = args[1:]
            else:
                reported_args = args
            Profiler.add_record(ProfilerRecord(f.__name__, f.start_time, f.end_time,
                                               func_args=reported_args, func_kwargs=kwargs))

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
        self.assertIsInstance(report, list)
        self.assertEqual(1, len(report))

        root = report[0]
        self.assertIsInstance(root, ProfilerRecord)
        self.assertEqual('main_function', root.name)
        self.assertLess(root.start_time, root.end_time)
        self.assertEqual(2, len(root.children))
        self.assertEqual('sub_function_1', root.children[0].name)
        self.assertEqual('sub_function_2', root.children[1].name)

    def test_two_unrelated_profiles(self):

        @profiled
        def function1():
            pass

        @profiled
        def function2():
            function2_sub()
            pass

        @profiled
        def function2_sub():
            pass

        function1()
        function2()

        report = Profiler.get_report()
        self.assertIsInstance(report, list)
        self.assertEqual(2, len(report))
        self.assertEqual('function1', report[0].name)
        self.assertEqual('function2', report[1].name)
        self.assertEqual(1, len(report[1].children))
        self.assertEqual('function2_sub', report[1].children[0].name)

    def test_profile_includes_func_args_string_representations(self):

        @profiled
        def get_price(quantity):
            return quantity * 5.0

        @profiled
        def get_bill(product_name, quantity=1):
            return '{} {}: {}'.format(quantity, product_name, get_price(quantity))

        get_bill('apples', quantity=3)

        report = Profiler.get_report()
        root = report[0]
        self.assertEqual('get_bill', root.name)
        self.assertEqual(['apples'], root.func_args)
        self.assertDictContainsSubset({'quantity': '3'}, root.func_kwargs)

        self.assertEqual('get_price', root.children[0].name)
        self.assertEqual(['3'], root.children[0].func_args)

    def test_func_args_converted_to_strings(self):

        @profiled
        def object_function(obj, key=None):
            pass

        object_function({1, 2, 3, 4, 5}, key=[1, 2])

        report = Profiler.get_report()
        root = report[0]
        self.assertIsInstance(root.func_args[0], basestring)
        self.assertIsInstance(root.func_kwargs['key'], basestring)

    def test_same_function_called_multiple_times(self):

        @profiled
        def common_function(key=None):
            pass

        common_function(key='first')
        common_function(key='second')
        common_function(key='third')

        report = Profiler.get_report()
        self.assertEqual(3, len(report))

        self.assertEqual('first', report[0].func_kwargs['key'])
        self.assertEqual('second', report[1].func_kwargs['key'])
        self.assertEqual('third', report[2].func_kwargs['key'])

        self.assertLess(report[0].start_time, report[1].start_time)
        self.assertLess(report[1].start_time, report[2].start_time)
        
        self.assertLess(report[0].end_time, report[1].end_time)
        self.assertLess(report[1].end_time, report[2].end_time)

    def test_get_report_returns_empty_list_when_no_profiles_were_collected(self):
        report = Profiler.get_report()
        self.assertIsInstance(report, list)
        self.assertEqual(0, len(report))

    def test_one_record_report_ok(self):

        @profiled
        def hello():
            pass

        hello()

        report = Profiler.get_report()
        self.assertIsInstance(report, list)
        self.assertEqual(1, len(report))
        self.assertEqual('hello', report[0].name)

    def test_function_raises_exception(self):

        @profiled
        def failing_function():
            raise RuntimeError()

        try:
            failing_function()
        except RuntimeError:
            pass

        report = Profiler.get_report()
        self.assertEqual(1, len(report))

    def test_profiler_can_be_flushed(self):

        @profiled
        def some_function(big_arg_in_memory=None):
            pass

        self.assertEqual(0, len(Profiler.get_report()))

        some_function()
        some_function()
        some_function()

        self.assertEqual(3, len(Profiler.get_report()))

        flushed_report = Profiler.flush_report()
        self.assertEqual(3, len(flushed_report))
        self.assertEqual(0, len(Profiler.get_report()))

        some_function()
        new_report = Profiler.get_report()
        self.assertEqual(1, len(new_report))

        Profiler.flush_report()
        self.assertEqual(0, len(Profiler.get_report()))

    def test_class_function(self):

        class MyClass(object):

            @profiled
            def class_function(self, name, key=None):
                pass

        c = MyClass()
        c.class_function('My Call', key=23)

        report = Profiler.get_report()
        self.assertEqual(1, len(report))
        self.assertEqual('class_function', report[0].name)
        self.assertEqual(['My Call'], report[0].func_args)
        self.assertDictContainsSubset({'key': '23'}, report[0].func_kwargs)