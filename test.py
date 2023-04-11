# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-04-10 15:51:57
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-04-11 13:17:25
@FilePath: /groundingDINO_grpc/test.py
@Description:
'''
import base64

import grpc
from core.proto import dldetection_pb2

from core.proto import dldetection_pb2_grpc as dld_grpc
from core.utils import tensor_proto2np

import cv2
import os


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:52007') as channel:
        stub = dld_grpc.AiServiceStub(channel)
        img_path = r"/home/chiebotgpuhq/MyCode/python/pytorch/groundingDINO_grpc/test_weight/2.jpg"
        img_file = open(img_path,'rb')  # 二进制打开图片文件
        img_b64encode = base64.b64encode(img_file.read())  # base64编码
        img_file.close()  # 文件关闭

        req1 = dldetection_pb2.ZeroShotRequest()
        req1.imdata = img_b64encode
        req1.prompt="dryer"
        req1.boxThr=0.3
        req1.textThr=0.3
        r1 = stub.ZeroShotDet(req1)

        # breakpoint()

        for obj in r1.results:
            print("type: {} score: {}  box: {}".format(obj.classid, obj.score,
                                                       obj.rect.x))


def unit_run():

    import core.base_config as config_manager
    config_manager.merge_param("/home/chiebotgpuhq/MyCode/python/pytorch/groundingDINO_grpc/test_weight/cfg.yaml")
    args_dict: dict = config_manager.param

    print(args_dict)

    grpc_args = args_dict['grpc_args']
    detector_params = args_dict['detector_params']
    from core.model import Detector
    model = Detector(**detector_params)
    from PIL import Image
    img_path = r"/home/chiebotgpuhq/MyCode/python/pytorch/groundingDINO_grpc/test_weight/2.jpg"
    img=Image.open(img_path)
    r=model.infer(img,"dryer",0.3,0.3)
    print(r)

if __name__ == '__main__':
    run()
