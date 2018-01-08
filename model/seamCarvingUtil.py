import time

def timer(f):
    def f_timer(self, *args, **kwargs):
        start = time.time()
        res = f(self, *args, **kwargs)
        end = time.time()
        print(f, "done in", round(end - start, 2), "s")
        return res
    return f_timer
