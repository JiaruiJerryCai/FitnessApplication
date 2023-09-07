# Create a model that can predict the temperature based on the sales of ice cream
from sklearn import linear_model

input = [[190],[210],[320],[315],[405],[410],[405],[405],[520],[450],[550],[610]]

answers = [12,14,15,16,17,18,18,19,22,22,23,25]

model = linear_model.LinearRegression()

# Train the model
model.fit(input, answers)

# Use the model 
print(
    model.predict([[400]])
)