# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import dldetection_pb2 as dldetection__pb2


class AiServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ZeroShotDet = channel.unary_unary(
                '/aiservice.AiService/ZeroShotDet',
                request_serializer=dldetection__pb2.ZeroShotRequest.SerializeToString,
                response_deserializer=dldetection__pb2.DlResponse.FromString,
                )


class AiServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ZeroShotDet(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AiServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ZeroShotDet': grpc.unary_unary_rpc_method_handler(
                    servicer.ZeroShotDet,
                    request_deserializer=dldetection__pb2.ZeroShotRequest.FromString,
                    response_serializer=dldetection__pb2.DlResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'aiservice.AiService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AiService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ZeroShotDet(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/aiservice.AiService/ZeroShotDet',
            dldetection__pb2.ZeroShotRequest.SerializeToString,
            dldetection__pb2.DlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
