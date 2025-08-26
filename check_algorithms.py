#!/usr/bin/env python3
import algorithms
import inspect

print("Available Algorithm Functions:")
for name in dir(algorithms):
    if not name.startswith('_') and callable(getattr(algorithms, name)):
        func = getattr(algorithms, name)
        if inspect.isfunction(func):
            print(f"  - {name}")
