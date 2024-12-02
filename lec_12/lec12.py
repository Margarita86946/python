import random
import time

def measureTime(func):
    def wrapper(*args, **kwargs):
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        print(f"Function '{func.__name__}' took {endTime - startTime:.4f} seconds")
        return result
    return wrapper

@measureTime
def writeRandomNumbers():
    with open('information.txt', 'w') as file:
        for lineNumber in range(100):
            line = " ".join(str(random.randint(-100, 100)) for _ in range(20))
            if lineNumber < 99:
                file.write(line + "\n")
            else:
                file.write(line)

@measureTime
def filterAndWriteBack():
    with open('information.txt', 'r') as file:
        filteredData = []
        for line in file:
            numbers = map(int, line.split())
            filteredNumbers = list(filter(lambda x: x > 40, numbers))
            filteredData.append(" ".join(map(str, filteredNumbers)))
    
    with open('information.txt', 'w') as file:
        for lineNumber in range(100):
            if lineNumber < len(filteredData):
                file.write(filteredData[lineNumber])
            else:
                file.write('')
            if lineNumber < 99:
                file.write("\n")

def readAsGenerator():
    with open('information.txt', 'r') as file:
        for line in file:
            yield list(map(int, line.split()))

writeRandomNumbers()

filterAndWriteBack()

print("\nFiltered numbers from the file:")
for numbers in readAsGenerator():
    print(numbers)