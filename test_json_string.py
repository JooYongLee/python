import numpy as np
import json
import matplotlib.pyplot as plt
import cv2
import base64

test_image_path = "d:/test/99C71A475AAE773807.jpg"

def img_array_to_bytes(img_array):
    _, enc_array = cv2.imencode(".png", img_array)
    # print(enc_array.shape)
    enc_bytes = enc_array.tobytes()
    encode_bytes = base64.encodebytes(enc_bytes)
    return encode_bytes


def bytes_to_img_array(encode_bytes):
    img_data = base64.b64decode(encode_bytes)
    np_array = np.frombuffer(img_data, np.uint8)

    rest_img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return rest_img


def write_json(buff, filename):
    if type(buff) == bytes:
        buff = buff.decode()
    elif type(buff) == str:
        raise ValueError
    with open(filename, "w") as f:
        json.dump({"imagedata":buff}, f)

def load_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    image = data.get("imagedata")
    if image is None:
        return None
    else:
        return image.encode()


def get_image():
    image = cv2.imread(test_image_path, cv2.IMREAD_COLOR)
    return image


def test_image_bytes_conversion():
    source_image = get_image()
    bytes_array = img_array_to_bytes(source_image)

    write_json(bytes_array, "test.json")
    load_bytes = load_json("test.json")
    assert bytes_array == load_bytes

    restored_image = bytes_to_img_array(load_bytes)
    restored_image2 = bytes_to_img_array(bytes_array)
    np.testing.assert_allclose(source_image, restored_image2)
    np.testing.assert_allclose(source_image, restored_image, verbose="check ")


if __name__=="__main__":
    test_image_bytes_conversion()