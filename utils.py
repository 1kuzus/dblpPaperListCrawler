import functools
import json
import os


def deduplicate(arr):
    visited = set()
    return [x for x in arr if not (x in visited or visited.add(x))]


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path, sort_fn=lambda item: item[0], reverse=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if sort_fn is not None:
        data = dict(sorted(data.items(), key=sort_fn, reverse=reverse))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def retry(max_retries=3):
    def inner_decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args)
                except AssertionError as ae:
                    print(f"[?] {ae}\n", end="")
                    return None
                except Exception as e:
                    print(f"[!] {func.__name__}{args} raised an exception: {e}\n", end="")
                    retries += 1
            print(f"[x] {func.__name__}{args} failed after {max_retries} retries.\n", end="")
            return None

        return wrapper

    return inner_decorator
