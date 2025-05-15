from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DlRequest(_message.Message):
    __slots__ = ("type", "imdata")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IMDATA_FIELD_NUMBER: _ClassVar[int]
    type: int
    imdata: bytes
    def __init__(self, type: _Optional[int] = ..., imdata: _Optional[bytes] = ...) -> None: ...

class ZeroShotRequest(_message.Message):
    __slots__ = ("prompt", "imdata", "boxThr", "textThr")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    IMDATA_FIELD_NUMBER: _ClassVar[int]
    BOXTHR_FIELD_NUMBER: _ClassVar[int]
    TEXTTHR_FIELD_NUMBER: _ClassVar[int]
    prompt: str
    imdata: bytes
    boxThr: float
    textThr: float
    def __init__(self, prompt: _Optional[str] = ..., imdata: _Optional[bytes] = ..., boxThr: _Optional[float] = ..., textThr: _Optional[float] = ...) -> None: ...

class DlBoundingRect(_message.Message):
    __slots__ = ("x", "y", "w", "h")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    H_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    w: int
    h: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., w: _Optional[int] = ..., h: _Optional[int] = ...) -> None: ...

class DlPoint(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class DlMask(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[DlPoint]
    def __init__(self, points: _Optional[_Iterable[_Union[DlPoint, _Mapping]]] = ...) -> None: ...

class DlResult(_message.Message):
    __slots__ = ("classid", "score", "rect", "mask")
    CLASSID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    RECT_FIELD_NUMBER: _ClassVar[int]
    MASK_FIELD_NUMBER: _ClassVar[int]
    classid: str
    score: float
    rect: DlBoundingRect
    mask: DlMask
    def __init__(self, classid: _Optional[str] = ..., score: _Optional[float] = ..., rect: _Optional[_Union[DlBoundingRect, _Mapping]] = ..., mask: _Optional[_Union[DlMask, _Mapping]] = ...) -> None: ...

class DlResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[DlResult]
    def __init__(self, results: _Optional[_Iterable[_Union[DlResult, _Mapping]]] = ...) -> None: ...
