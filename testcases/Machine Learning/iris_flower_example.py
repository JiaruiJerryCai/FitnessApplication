from sklearn import svm

input = [
    [5.0, 3.4, 1.5, 0.2],   # Setosa
    [4.4, 2.9, 1.4, 0.2],   # Setosa  
    [4.3, 3.0, 1.1, 0.1],   # Setosa
    [5.5, 2.4, 3.7, 1.0],   # Versicolor
    [5.5, 2.4, 3.8, 1.1],   # Versicolor
    [5.8, 2.7, 3.9, 1.2],   # Versicolor
    [7.2, 3.6, 6.1, 2.5],   # Virginica
    [6.5, 3.2, 5.1, 2.0],   # Virginica
    [6.4, 3.2, 5.3, 2.3]    # Virginica
]

answers = [
    0,  # Setosa
    0,  # Setosa
    0,  # Setosa
    1,  # Versicolor
    1,  # Versicolor
    1,  # Versicolor
    2,  # Virginica
    2,  # Virginica
    2,  # Virginica
]

model = svm.SVC() # SVC is a ML algorithm

# Train the model
model.fit(input, answers)

# Use the model 
print(
    model.predict([
        [5.1,3.5,1.4,0.2],
        [6.5,2.8,4.6,1.5],
        [7.2,3.0,5.8,1.6]
    ])
)