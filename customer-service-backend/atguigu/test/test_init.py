from pydantic import BaseModel


class A(BaseModel):
    command: str

class B(A):
    flow: str | None = None

if __name__ == '__main__':

    obj = B(command="cc")
    print(obj)
