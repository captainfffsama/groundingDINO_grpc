# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-03-23 18:05:51
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-04-10 15:26:00
@FilePath: /groundingDINO_grpc/core/utils.py
@Description:
'''
import os
import re
from typing import Optional
import base64
from io import BytesIO

import numpy as np
import cv2

from .proto import dldetection_pb2
from PIL import Image, ImageDraw, ImageFont

def get_img(img_info) -> Optional[Image.Image]:
    if os.path.isfile(img_info):
        if not os.path.exists(img_info):
            return None
        else:
            return Image.open(img_info)  #ignore
    else:
        # base64_data = re.sub('^data:image/.+;base64,', '',img_info)
        img_str = base64.b64decode(img_info)
        img_data=BytesIO(img_str)
        return Image.open(img_data)


def np2tensor_proto(np_ndarray: np.ndarray):
    shape = list(np_ndarray.shape)
    data = np_ndarray.flatten().tolist()
    tensor_pb = dldetection_pb2.Tensor()
    tensor_pb.shape.extend(shape)
    tensor_pb.data.extend(data)
    return tensor_pb


def tensor_proto2np(tensor_pb):
    np_matrix = np.array(tensor_pb.data,
                         dtype=np.float).reshape(tensor_pb.shape)
    return np_matrix