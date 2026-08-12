

condition = "__import__('os').system('del test.txt')"
data = {"a": 3, "b": 5}

print(eval(condition, {"__builtins__": None}, data))



