# -*- coding: utf-8 -*-
'''
@Author: captainfffsama
@Date: 2023-04-10 10:54:49
@LastEditors: captainfffsama tuanzhangsama@outlook.com
@LastEditTime: 2023-04-13 12:49:59
@FilePath: /groundingDINO_grpc/core/model.py
@Description:
'''
from collections import defaultdict
from typing import Union

import numpy as np
import cv2
import torch
from PIL import Image
from core.proto import dldetection_pb2
from core.proto import dldetection_pb2_grpc as dld_pb2_grpc

import groundingdino.datasets.transforms as T
from groundingdino.models import build_model
from groundingdino.util import box_ops
from groundingdino.util.slconfig import SLConfig
from groundingdino.util.utils import clean_state_dict, get_phrases_from_posmap

from .utils import get_img

def get_grounding_output(model, image, caption, box_threshold, text_threshold, with_logits=True, device="cuda"):
    caption = caption.lower()
    caption = caption.strip()
    if not caption.endswith("."):
        caption = caption + "."
    # model = model.to(device)
    image = image.to(device)
    with torch.no_grad():
        outputs = model(image[None], captions=[caption])
    logits = outputs["pred_logits"].cpu().sigmoid()[0]  # (nq, 256)
    boxes = outputs["pred_boxes"].cpu()[0]  # (nq, 4)
    logits.shape[0]

    # filter output
    logits_filt = logits.clone()
    boxes_filt = boxes.clone()
    filt_mask = logits_filt.max(dim=1)[0] > box_threshold
    logits_filt = logits_filt[filt_mask]  # num_filt, 256
    boxes_filt = boxes_filt[filt_mask]  # num_filt, 4

    # get phrase
    tokenlizer = model.tokenizer
    tokenized = tokenlizer(caption)
    # build pred
    pred_phrases = []
    for logit, box in zip(logits_filt, boxes_filt):
        pred_phrase = get_phrases_from_posmap(logit > text_threshold, tokenized, tokenlizer)
        pred_phrases.append((pred_phrase,logit.max().item()))

    return boxes_filt, pred_phrases

class Detector(dld_pb2_grpc.AiServiceServicer):

    def __init__(self,
                 cfg_path,
                 ckpt_path,
                 device: str = 'cuda:0'):
        model_args=SLConfig.fromfile(cfg_path)
        model_args.device = device
        ckpt=torch.load(ckpt_path,map_location="cpu")
        self.model=build_model(model_args,)
        print("model will build on device: ",device)
        self.device=device
        load_res=self.model.load_state_dict(clean_state_dict(ckpt["model"]),strict=False)
        self.model=self.model.to(device)
        self.model.eval()
        self._transform = T.Compose(
            [
                T.RandomResize([800], max_size=1333),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        print("model init done!")


    def infer(self, img,prompt:str,box_thr:float,text_thr:float):
        W,H=img.size
        classes=set(prompt.split(";"))
        img_det,_=self._transform(img,None)
        boxes_filt, pred_phrases = get_grounding_output(
            self.model,img_det,prompt, box_thr, text_thr, device=self.device
        )
        new_result =[]
        for box,label in zip(boxes_filt, pred_phrases):
            if label[0] in classes:
                box:torch.Tensor = box * torch.Tensor([W, H, W, H])
                box[:2] -= box[2:] / 2
                box[2:] += box[:2]
                box=box.detach().cpu().numpy().tolist()
                new_result .append((label[0],label[1],*box))

        return new_result


    def ZeroShotDet(self, request, context):
        img=get_img(request.imdata)
        img=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        print("prompt is: ",request.prompt)
        result = self.infer(img,request.prompt,request.boxThr,request.textThr)
        print(result)
        result_pro = dldetection_pb2.DlResponse()
        for obj in result:
            obj_pro = result_pro.results.add()
            obj_pro.classid = obj[0]
            obj_pro.score = float(obj[1])
            obj_pro.rect.x = int(obj[2])
            obj_pro.rect.y = int(obj[3])
            obj_pro.rect.w = int(obj[4] - obj[2])
            obj_pro.rect.h = int(obj[5] - obj[3])
        torch.cuda.empty_cache()

        return result_pro
