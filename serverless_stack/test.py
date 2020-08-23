import os


# try:
#     with open("serverless_stack/lambda.py") as f:
#         var=f.read()
#         print("file read\n")
# except OSError:
#     print("file not found")

class Test:
    def __init__(self,name,age):
        self.name=name,
        self.age=age
    

t=Test(name="b",age=2)
print(t.age)