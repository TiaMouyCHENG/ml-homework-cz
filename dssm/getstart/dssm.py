#coding:utf-8
from __future__ import print_function
from keras.layers import Embedding, Dense, Conv1D, Input, GlobalAveragePooling1D, dot, Activation
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.preprocessing import sequence
import numpy as np
import random
sentence_maxlen = 64
word_cnt = 128
class DSSM(object):
    def __init__(self, ):
        x1 = Input(shape=(sentence_maxlen,))
        x2 = Input(shape=(sentence_maxlen,))
        """
        TODO 利用keras创建DSSM模型
        """
        model = Sequential([
            Embedding(input_dim=word_cnt, output_dim=128, input_shape=(sentence_maxlen, )),
            Dense(units=64, activation='relu'),
            Conv1D(filters=32, kernel_size=3),
            GlobalAveragePooling1D(),
            Dense(units=32)
        ])
        s1 = model(x1)
        s2 = model(x2)
        s = dot([s1, s2], axes=1)
        y_ = Activation(activation='sigmoid')(s)
        self.model = Model(inputs=[x1, x2], outputs=[y_,])
        self.model.compile(Adam(lr=0.001), loss=binary_crossentropy, metrics=['accuracy'])

    def fit(self, train_set, eval_set = None, **kwargs):
        """
        TODO 模型训练
        HINT: 有用的函数 KERAS: model.fit_generator
        """
        self.model.fit_generator(generator=train_set, validation_data=eval_set, **kwargs)
        raise NotImplemented()

    def predict(self, test_set):
        """
        TODO 模型预测
        """
        return self.model.predict_generator(generator=test_set, **kwargs)
        raise NotImplemented()


def training():
    global sentence_maxlen
    global word_cnt
    import pickle
    data = pickle.load(open("data.pkl"))
    word_cnt = 1 + data['wordcnt']
    sentence_maxlen = 1 + max(len(d['title']) for d in data['train'])
    print(sentence_maxlen)

    def data_set(train_or_test = 'train'):
        if train_or_test == 'test':
            dataset = data['test']
        else:
            dataset = data['train']
        while True:
            x1 = []
            x2 = []
            y = []
            n_samples = len(dataset)
            for i in range(n_samples):
                """
                TODO 构造一个正样本
                """
                x1.append(dataset[i]['title'])
                x2.append(dataset[i]['tags'])
                y.append([1])

                """
                TODO 通过负采样构建一个负样本
                """
                j = random.randint(0, n_samples-1)
                while j == i:
                    j = random.randint(0, n_samples-1)

                x1.append(dataset[j]['title'])
                x2.append(dataset[j]['tags'])
                y.append([0])

                if (i+1) % 16 == 0:
                    x1 = sequence.pad_sequences(x1, maxlen=sentence_maxlen)
                    x2 = sequence.pad_sequences(x2, maxlen=sentence_maxlen)
                    y = np.array(y)
                    yield ([x1, x2], y)

                    x1 = []
                    x2 = []
                    y = []

    """
    TODO 创建模型,并调用fit方法
    """
    model = DSSM()
    train = data_set('train')
    test = data_set('test')
    model.fit(train_set=train, eval_set=test, steps_per_epoch=128, validation_steps=64, epochs=1)




if __name__ == '__main__':
    training()