import time
import grpc

import demo_pb2_grpc
import demo_pb2

__all__ = [
    'simple_method', 'client_streaming_method', 'server_streaming_method',
    'bidirectional_streaming_method'
]

SERVER_ADDRESS = "localhost:23333"
CLIENT_ID = 3


