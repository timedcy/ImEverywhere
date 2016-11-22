import time
import functools
def time_me(info="used"):
    def _time_me(fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            start = time.clock()
            fn(*args, **kwargs)
            print("%s %s %s"%(fn.__name__, info, time.clock() - start), "second")
        return _wrapper
    return _time_me
@time_me()
def test(x, y):
    time.sleep(0.1)
@time_me("cost")
def test2(x):
    time.sleep(0.2)
test(1, 2)
test2(2)
