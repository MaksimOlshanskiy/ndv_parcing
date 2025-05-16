result = []

# от 23 до 60 с шагом 1
for i in range(23, 60):
    result.append([i, i + 1])

# от 60 до 80 с шагом 2
for i in range(60, 80, 2):
    result.append([i, i + 2])

# от 80 до 100 с шагом 5
for i in range(80, 100, 5):
    result.append([i, i + 5])

# от 100 до 200 с шагом 10
for i in range(100, 200, 10):
    result.append([i, i + 10])

print(result)