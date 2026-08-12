

condition = "slots.get('product_id')"
data = {"slots": {"product_id": "P002"}}

print(bool(eval(condition, {"__builtins__": None}, data)))


