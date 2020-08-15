import os


try:
    with open("serverless_stack/lambda.py") as f:
        var=f.read()
        print("file read\n")
except OSError:
    print("file not found")