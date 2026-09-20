customer_file = input("Enter file path: ")

f = open(customer_file,"r")

for line in f.readlines():
    print(line.strip())

f.close()