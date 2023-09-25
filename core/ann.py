import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Read the CSV data into a DataFrame
player_data = pd.read_csv(r'C:\Users\dell\OneDrive\Desktop\lebronjames.csv')

# Extract the 'game_date' and 'game_score' columns
game_dates = player_data['game_date']
game_scores = player_data['game_score']

# Convert 'game_date' to a datetime type
game_dates = pd.to_datetime(game_dates)

# Create a DataFrame with 'game_date' and 'game_score'
career_data = pd.DataFrame({'game_date': game_dates, 'game_score': game_scores})

# Set 'game_date' as the index
career_data.set_index('game_date', inplace=True)

# Normalize the data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(career_data)

# Define the sequence length
sequence_length = 10

# Create sequences for ANN training
X = []
y = []
for i in range(sequence_length, len(scaled_data)):
    X.append(scaled_data[i-sequence_length:i, 0])
    y.append(scaled_data[i, 0])
X, y = np.array(X), np.array(y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Build the ANN model
model = Sequential()
model.add(Dense(64, activation='relu', input_dim=sequence_length))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_absolute_error')  

# Train the model on the training data
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=2)

# Evaluate the model on the test data
mae = model.evaluate(X_test, y_test, verbose=0)  # Use MAE for evaluation

# Predict the next game score based on the most recent historical data
last_sequence = scaled_data[-sequence_length:, 0]
last_sequence = np.reshape(last_sequence, (1, sequence_length))
predicted_score = model.predict(last_sequence)

# Transform the prediction back to the original scale
predicted_score = scaler.inverse_transform(predicted_score)[0][0]

print(player_data)
print(f"Predicted Next Game Score with ANN model: {predicted_score}")
print(f"Mean Absolute Error on Test Data: {mae}")
