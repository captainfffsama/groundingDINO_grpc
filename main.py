# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-04-10 10:50:34
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-04-13 12:48:35
@FilePath: /groundingDINO_grpc/main.py
@Description:
'''
import os
import argparse
from concurrent import futures
from pprint import pprint
from datetime import datetime
import asyncio
import pid
from pid.decorator import pidfile

import grpc
from core.proto import dldetection_pb2_grpc as dld_grpc

from core.model import Detector
import core.base_config as config_manager


def parse_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-mc", "--model_cfg", type=str, default="")
    parser.add_argument("-mw", "--model_weight", type=str, default="")
    parser.add_argument("-c", "--cfg", type=str, default="")
    args = parser.parse_args()
    return args


async def main(args):
    if os.path.exists(args.cfg):
            config_manager.merge_param(args.cfg)
    args_dict: dict = config_manager.param
    print("current time is: ", datetime.now())
    print("pid file save in {}".format(pid.DEFAULT_PID_DIR))

    pprint(args_dict)

    grpc_args = args_dict['grpc_args']
    detector_params = args_dict['detector_params']
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=grpc_args['max_workers']),
        options=[('grpc.max_send_message_length',
                  grpc_args['max_send_message_length']),
                 ('grpc.max_receive_message_length',
                  grpc_args['max_receive_message_length'])])
    if os.path.exists(args.model_cfg) and os.path.exists(args.model_weight):
        detector_params['cfg_path'] = args.model_cfg
        detector_params['ckpt_path'] = args.model_weight
    # FIXME: dirty fix device
    device=detector_params.get("device","None")
    if device.startswith("cuda"):
        detector_params.pop("device")
        if device.find(":") != -1:
            os.environ["CUDA_VISIBLE_DEVICES"] = device.split(":")[-1]
    model = Detector(**detector_params)
    dld_grpc.add_AiServiceServicer_to_server(model, server)

    server.add_insecure_port("{}:{}".format(grpc_args['host'],
                                            grpc_args['port']))
    await server.start()
    print('groundingDINO gprc server init done')
    await server.wait_for_termination()

@pidfile(pidname='GDINO_grpc')
def run():
    args = parse_args()
    asyncio.run(main(args))

if __name__ == "__main__":
    run()