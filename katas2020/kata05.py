"""
Profiling decorator
2020-12-09
"""
import dataclasses
import functools
import time
from typing import Dict, Tuple, Any


@dataclasses.dataclass
class Call:
    start_time: float
    end_time: float
    args: Tuple = dataclasses.field(default_factory=tuple)
    kwargs: Dict = dataclasses.field(default_factory=dict)
    result: Any = None


def profiled(fn):
    calls = []

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        result = fn(*args, **kwargs)
        calls.append(Call(
            start_time=start_time,
            end_time=time.time(),
            args=args,
            kwargs=kwargs,
            result=result,
        ))
        return result

    wrapped.calls = calls

    return wrapped


def test_all():

    @profiled
    def do_this(message: str, *extras):
        print(message)

    assert do_this.calls == []

    do_this("hello")
    assert len(do_this.calls) == 1
    assert do_this.calls[0].args == ("hello",)

    do_this("world")
    assert len(do_this.calls) == 2
    assert do_this.calls[1].args == ("world",)
