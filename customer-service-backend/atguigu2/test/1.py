from pydantic import BaseModel
class Person(BaseModel):
    name: str
    age: int

p1 = Person(name="Alice", age=18)

# p2 = Person("Bob", 20)

person_dict = {"name": "Alice", "age": 18}
p3 = Person(**person_dict)

p4 = Person.model_validate(person_dict)

