import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split


# generator function from Chollet's book

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

def generator(data, lookback, delay, min_index, max_index,
                shuffle=False, batch_size=128, step=6):
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
        samples = np.zeros((len(rows),
                            lookback // step,
                            data.shape[-1]))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            indices = range(rows[j] - lookback, rows[j], step)
            samples[j] = data[indices]
            targets[j] = data[rows[j] + delay][1]
        yield samples, targets

lookback = 20
step = 6
delay = 1
batch_size = 32

train_gen = generator(career_data,
                        lookback=lookback,
                        delay=delay,
                        min_index=0,
                        max_index=1000,
                        shuffle=True,
                        step=step,
                        batch_size=batch_size)
val_gen = generator(career_data,
                        lookback=lookback,
                        delay=delay,
                        min_index=1000,
                        max_index=1200,
                        step=step,
                        batch_size=batch_size)
test_gen = generator(career_data,
                    lookback=lookback,
                    delay=delay,
                    min_index=1200,
                    max_index=None,
                    step=step,
                    batch_size=batch_size)
val_steps = (1421 - 1200 - lookback)
test_steps = (len(career_data) - 1421 - lookback)


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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(sequence_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model and record the training history
history = model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=2, validation_data=(X_test, y_test))

# Plot the loss function over epochs for training and validation sets
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Predict the next game score based on the most recent historical data
last_sequence = scaled_data[-sequence_length:, 0]
last_sequence = np.reshape(last_sequence, (1, sequence_length, 1))
predicted_score = model.predict(last_sequence)

# Transform the prediction back to the original scale
predicted_score = scaler.inverse_transform(predicted_score)[0][0]

# Calculate and print regression evaluation metrics
true_values = career_data.values[-1]  # True game score for the next game

# Reshape predicted_score to match the shape of true_values
predicted_score = np.reshape(predicted_score, true_values.shape)

mae = mean_absolute_error(true_values, predicted_score)

print(f"Predicted Next Game Score: {predicted_score[0]}")
print(f"Mean Absolute Error (MAE): {mae}")

