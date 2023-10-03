import random
import turtle as otherModule
import myClass


# This is how to comment
print("Hello World")

# If Statements
if 2 < 3 and 3 < 4:
    print("Hello There")
    print("Hello Goodbye")
elif 3 != 3:
    print("Hi")
else:
    print("Goodbye")

# Loops
# range(10) produces a list such as [0, 1, ...,8 , 9]
for x in range(10):
    print(x)

for x in "Earth":
    print(x)

x = 0
while x < 5:
    print(x)
    x = x + 1

# variables can be changed to different types
myVariable = 10
print(myVariable)
myVariable = "A sentence"
print(myVariable)

# Lists (python's arrays)
myEmptyList = [5,6,7,89,5,4]
myEmptyList.append(10)
myEmptyList.insert(3,"a")
print(myEmptyList)

myList = ["California", "Texas", "North Dakota"]
print(myList)

# Functions
def sayHello():
    print("Hi")

# Calling functions
sayHello()
sayHello()

def sayGreeting(name):
    print("Hello " + name)

sayGreeting("Matthew")

def addition(num1, num2, num3):
    answer1 = num1 + num2
    answer2 = num2 + num3
    return answer1, answer2 # 2 return values

output1, output2 = addition(3, 4, 5) # must 
a, _ = addition(4,5,6)
print(output1)
print(output2)

# input
# answer = input("What is your favorite food? ")
# print(answer)

# create a function that can check if the given arguement is prime or not
# return True or False
def checkPrime(number):
    if number < 2:
        return False
    for i in range(2,number): # 2 to the given number
        if number%i == 0:
            return False
    return True

print(checkPrime(373))
print(checkPrime(5))   # True
print(checkPrime(3))   # True
print(checkPrime(11))  # True
print(checkPrime(16))  # False

# create a function call findPrimes(number)
# It takes in a number and gives out that amount of prime numbers



def findPrimes(number):
    numLeft = number
    a = 2
    while numLeft != 0:
        if checkPrime(a) == True:
            print(a)
            numLeft -= 1
        a += 1
    

findPrimes(3) # 2, 3, 5
print()
findPrimes(1) # 2
print()
findPrimes(5) # 2, 3, 5, 7, 11

# Classes
class Dog:

    # special function used to keep track of the class variables (attributes)
    def __init__(self):
        self.length = None

    def getLength(self):
        return self.length
    
    def setLength(self, number):
        self.length = number

myDog = Dog()
print(myDog)
print(myDog.length)
myDog.setLength("Hello")
print(myDog.length)


# Dictionaries
colorlist=["red","green","blue"] # indexes: [0, 1, 2]
print(colorlist[1]) # green

# Dictionary can only have unique keys or "indexes"

colorDictionary = {"Tim":"green", "Jerry":"blue", "Matthew":"purple"}
# What is Jerry's favorite color?
print(colorDictionary["Jerry"]) # blue
print(colorDictionary.keys()) #dict_keys(['Tim', 'Jerry', 'Matthew'])

# adding another entry to dictionary
colorDictionary["Alan"] = "blue" # add at end
print(colorDictionary) #{'Tim': 'green', 'Jerry': 'blue', 'Matthew': 'purple', 'Alan': 'blue'}

# Deleting an entry
colorDictionary.pop("Tim") #remove Tim
print(colorDictionary)

# Using the random module
print(random.randint(0,10)) #random number from 0-10
print(random.choice(colorlist)) #random color from colorlist

# Using an object from a module
mT = otherModule.Turtle()
mT.forward(100)

# Run myFunction from myClass
myClass.myFunction()

myDiction = {'Tim': 'green', 'Jerry': 'blue', 'Matthew': 'purple', 'Alan': 'blue'}

for x in myDiction:
    print(x)