import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation

def min_max_scaling(x):
    x_np = np.asarray(x)
    return (x_np - x_np.min()) / (x_np.max() - x_np.min() + 1e-7 )

def reverse_min_max_scaling(org_x, x):
    org_x_np = np.asarray(org_x)
    x_np = np.asarray(x)
    return (x_np * (org_x_np.max() - org_x_np.min() + 1e-7)) + org_x_np.min()

def lstm_model(data):
    end_prices = data['Close'].values

    last_close_prices = data['Close'].values
    last_prices = float(last_close_prices[-1])
    #print(last_prices)
    #print(type(last_prices))


    #50일 데이터를로 다음날을 예측 총 51
    seq_len = 50
    sequence_length = seq_len + 1

    result = []
    # for i in range(len(mid_prices) - sequence_length):
    #     result.append(mid_prices[i: i + sequence_length])

    for i in range(len(end_prices) - sequence_length):
        result.append(end_prices[i: i + sequence_length])

    c = []
    value = 1
    for i in end_prices[-50:]:
        value = i
        c.append(value)
    c.append(value)
    c = np.array(c)
    print(c)

    result.append(c)
    print(result[-1])

    #정규화를 진행
    result = min_max_scaling(result)

    #90프로를 학습데이터로 사용
    row = int(len(result) * 0.9)
    train = result[:row, :]
    np.random.shuffle(train)

    #print(train)

    #50개
    x_train = train[:, :-1]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    #1개
    y_train = train[:, -1]

    x_test = result[row:, :-1]
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = result[row:, -1]

    model = Sequential()

    #input size는 50개
    model.add(LSTM(50, return_sequences=True, input_shape=(50, 1)))

    model.add(LSTM(64, return_sequences=False))
    #결과값은 1개
    model.add(Dense(1, activation='linear'))

    model.compile(loss='mse', optimizer='rmsprop')

    model.fit(x_train, y_train,
              validation_data=(x_test, y_test),
              batch_size=10,
              epochs=20)

    pred = model.predict(x_test)

    fig = plt.figure(facecolor='white', figsize=(20, 10))
    ax = fig.add_subplot(111)
    ax.plot(y_test, label='True')
    ax.plot(pred, label='Prediction')
    ax.legend()
#    plt.show()

    #반정규화를 해줘서 값을 뽑아 냅니다.
    reverse_pre = reverse_min_max_scaling(end_prices, pred)

    score = model.evaluate(x_test, y_test, batch_size=30)
    print(score)

    return last_prices, reverse_pre[-1] , fig, score