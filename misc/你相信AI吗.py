import base64
import signal
import string
import itertools
import contextlib


def has_visible_bytes(input_bytes):
    return all(chr(byte) in (string.ascii_letters + string.digits + '=+/') for byte in input_bytes)


cipher_text = ''.split(
    " ")
with open("out.txt", "wb") as f:
    for i in itertools.permutations("0123456789", 10):
        maktrans = str.maketrans("0123456789", ''.join(i))

        lis = [str.translate(i, maktrans) for i in cipher_text]

        with contextlib.suppress(Exception):
            plan_text = bytes(list(map(lambda x: int(x), lis)))
            if has_visible_bytes(plan_text):
                print(plan_text)

import cv2
import numpy as np
import glob
import os

for i in range(80):
    file_path = f"./dataset/{i}.txt"
    image_data = np.loadtxt(file_path)

    if image_data.size == 2352:
        image_data = image_data.reshape(84, 28)
    elif image_data.size == 1568:
        image_data = image_data.reshape(56, 28)
    else:
        print(i)
        continue

    os.makedirs("./out", exist_ok=True)  # 创建out文件夹，如果已存在则不会抛出异常
    cv2.imwrite(f"./out/{i}.png", image_data)