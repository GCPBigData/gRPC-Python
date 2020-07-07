import os
import lib

import time
import grpc

import demo_pb2_grpc
import demo_pb2

__all__ = [
    'simple_method', 'client_streaming_method', 'server_streaming_method',
    'bidirectional_streaming_method'
]

SERVER_ADDRESS = "localhost:23333"
client = lib.FileClient('localhost:23333')
CLIENT_ID = 2

def simple_method(stub):
    #Uploading file
    in_file_name = 'C:\Users\usuario\Documents\Dev\gRPC-Python\data_transmission\uploading\file.parquet'
    client.upload(in_file_name)

    #Downloading file
    out_file_name = 'C:\Users\usuario\Documents\Dev\gRPC-Python\data_transmission\downloading\file.parquet'
    if os.path.exists(out_file_name):
       os.remove(out_file_name)
    client.download('whatever_name', out_file_name)
    os.system(f'sha1sum {in_file_name}')
    os.system(f'sha1sum {out_file_name}')

    print("//--------------INICIANDO LIGACAO : SIMPLES :--------//")
    request = demo_pb2.Request(client_id=CLIENT_ID,
                               request_data="Chamada pelo cliente Python")
    response = stub.SimpleMethod(request)
    print("Resposta Servidor(%d), A Mensagem =%s" %
          (response.server_id, response.response_data))
    print("//--------------FINALIZANDO LIGACAO---------------//")

def client_streaming_method(stub):
    print("//--------------INICIANDO LIGACAO : CLIENTE STREAMING :--------------//")
    # create a generator
    def request_messages():
        for i in range(5):
            request = demo_pb2.Request(
                client_id=CLIENT_ID,
                request_data=("Chamada pelo cliente Python, Mensagem:%d" % i))
            yield request
    response = stub.ClientStreamingMethod(request_messages())
    print("Resposta Servidor(%d), A Mensagem =%s" %
          (response.server_id, response.response_data))
    print("//--------------FINALIZANDO LIGACAO---------------//")

def server_streaming_method(stub):
    print("//--------------INICIANDO LIGACAO : SERVIDOR STREAMING :--------------//")
    request = demo_pb2.Request(client_id=CLIENT_ID,
                               request_data="Chamada pelo cliente Python")
    response_iterator = stub.ServerStreamingMethod(request)
    for response in response_iterator:
        print("Resposta Servidor(%d), A Mensagem =%s" %
              (response.server_id, response.response_data))
    print("//--------------FINALIZANDO LIGACAO---------------//")

def bidirectional_streaming_method(stub):
    print("//--------------INICIANDO LIGACAO : BIDIRECIONAL STREAMING :--------------//")
    # create a generator
    def request_messages():
        for i in range(100):
            request = demo_pb2.Request(
                client_id=CLIENT_ID,
                request_data=("Chamada pelo cliente Python, Mensagem: %d" % i))
            yield request
            time.sleep(1)
    response_iterator = stub.BidirectionalStreamingMethod(request_messages())
    for response in response_iterator:
        print("Resposta Servidor(%d), Mensagem=%s" %
              (response.server_id, response.response_data))
    print("//--------------FINALIZANDO LIGACAO---------------//")

def main():
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        stub = demo_pb2_grpc.GRPCDemoStub(channel)
        simple_method(stub)
        client_streaming_method(stub)
        server_streaming_method(stub)
        bidirectional_streaming_method(stub)

if __name__ == '__main__':
    main()
