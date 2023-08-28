import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def generator(data, lookback, delay, min_index, max_index, shuffle=False, batch_size=128, step=6):
    if max_index is None:
        max_index = len(data) - delay - 1
    i = min_index + lookback
    while 1:
        if shuffle:
            rows = np.random.randint(
                min_index + lookback, max_index, size=batch_size)
        else:
            if i + batch_size >= max_index:
                i = min_index + lookback
            rows = np.arange(i, min(i + batch_size, max_index))
            i += len(rows)
        samples = np.zeros((len(rows), lookback // step, data.shape[-1])) 
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets


player_data = pd.read_csv(r'C:\Users\dell\OneDrive\Desktop\stevenadams.csv')
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

# Create sequences for LSTM training
sequence_length = 10  # Adjust as needed
X = []
y = []
for i in range(sequence_length, len(scaled_data)):
    X.append(scaled_data[i-sequence_length:i, 0])
    y.append(scaled_data[i, 0])
X, y = np.array(X), np.array(y)

# Reshape X to match LSTM input shape [samples, time steps, features]
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X, y, epochs=50, batch_size=32, verbose=2)

# Predict the next game score based on the most recent historical data
last_sequence = scaled_data[-sequence_length:, 0]
last_sequence = np.reshape(last_sequence, (1, sequence_length, 1))
predicted_score = model.predict(last_sequence)

# Transform the prediction back to the original scale
predicted_score = scaler.inverse_transform(predicted_score)[0][0]
print(player_data)
print(f"Predicted Next Game Score: {predicted_score}")
