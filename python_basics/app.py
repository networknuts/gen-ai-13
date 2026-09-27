def greeting():
    print("hello world")
    print("hello python")

def goodbye():
    print("goodbye world")

def say_hello(name):
    print(f"hello {name}")

def say_data(name="john",location="USA",role="developer"):
    print(f"Your name is {name} and your location is {location}")
    print(f"Your access is {role}")

def add_together(n1=0,n2=0):
    return(n1+n2)

result = add_together(5,5)
print(result)