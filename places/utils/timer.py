from datetime import timedelta
import time


def timer(func):
    def quantify(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        duration = timedelta(seconds=end_time - start_time)
        print(f'Время выполнения - {duration}')
        return result
    return quantify
