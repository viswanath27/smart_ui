from typing import Callable, TypeVar
import time

T = TypeVar('T', bound=Callable[..., any])

def throttle(func: T, limit: int) -> T:
    """
    Throttles the execution of a function based on a time limit.

    Args:
        func (T): The function to throttle.
        limit (int): The time limit in milliseconds.

    Returns:
        T: The throttled function.

    """
    last_func = None
    last_ran = 0

    def throttled_func(*args) -> None:
        nonlocal last_func, last_ran
        if not last_ran:
            func(*args)
            last_ran = time.time()
        else:
            if last_func:
                last_func.cancel()
            time_diff = time.time() - last_ran
            if time_diff >= limit:
                func(*args)
                last_ran = time.time()
            else:
                remaining_time = limit - time_diff
                last_func = Timer(remaining_time, func, args=args)
                last_func.start()

    return throttled_func

