# encoding=utf-8
from flask import Flask, request, jsonify
import jieba
import jieba.analyse
import sys
import os

sys.path.append('../')

app = Flask(__name__)

USER_DICT_LOADED = False
JIANHUANG_LOADED = False


@app.route('/')
def index():
    global USER_DICT_LOADED
    if request.method == 'POST':
        text = request.form.get('text')
    else:
        text = request.args.get('text')

    if False == USER_DICT_LOADED:
        jieba.load_userdict('dict/dict.txt.big')
        jieba.analyse.set_idf_path('dict/idf.txt.big')
        jieba.analyse.set_stop_words('dict/stop_words.txt')
        USER_DICT_LOADED = True

    seg_list = jieba.cut_for_search(text)
    keywords = []
    for keyword in seg_list:
        if len(keyword) > 1:
            keywords.append(keyword)

    tags = []
    for x, w in jieba.analyse.textrank(text, withWeight=True):
        tags.append(x)

    return jsonify(keywords=keywords, tags=tags)


@app.route('/jianhuang')
def jianhuang():
    global JIANHUANG_LOADED
    if request.method == 'POST':
        path = request.form.get('path')
    else:
        path = request.args.get('path')

    from keras.preprocessing.image import img_to_array, load_img
    from keras.layers.core import Dense, Flatten
    from keras.layers import Input
    from keras.models import Model
    from keras import optimizers
    import keras as ks

    # input image dimensions
    img_rows, img_cols = 128, 128
    img_channels = 3
    n_classes = 1

    # define model
    img_input = Input(shape=(img_rows, img_cols, 3))
    xinception = ks.applications.Xception(include_top=False, weights=None, input_tensor=img_input)
    output = xinception.output
    output = Flatten(name='flatten')(output)
    output = Dense(n_classes, activation='sigmoid', name='predictions')(output)
    model = Model(xinception.input, output)
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizers.Adam(),
                  metrics=["accuracy"])

    # load weights
    if False == JIANHUANG_LOADED:
        if os.path.exists('./model/0.12-loss_18epoch_128x128_aug_0.001lr_run0_Xception_128_1493071505.11time.h5'):
            print('loading weights..........')
            model.load_weights('./model/0.12-loss_18epoch_128x128_aug_0.001lr_run0_Xception_128_1493071505.11time.h5')
            JIANHUANG_LOADED = True
            print('load OK!')
        else:
            print('Not Find Weights........')

    re_img = load_img(path)  # this is a jpg image
    re_img = re_img.resize((img_cols, img_rows))
    x_img = img_to_array(re_img)  # this is a Numpy array with shape (100,100,3)
    x_img /= 255
    x_img -= 0.5
    x_img *= 2
    x_img = x_img.reshape((1,) + x_img.shape)  # this is a Numpy array with shape (1, 100, 100, 3)
    s = model.predict_on_batch(x_img)
    print('Input image is: %s, probability is: %3.3f%%' % (path, 100 * s,))

    return jsonify(weight=100 * s)
