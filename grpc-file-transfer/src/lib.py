import os
from concurrent import futures

import grpc
import time

import chunk_pb2, chunk_pb2_grpc

CHUNK_SIZE = 1024 * 1024  # 1MB

def get_file_chunks(filename):
    # rb   -> Abre um arquivo para leitura apenas em formato binário.
    # rb + -> Abre um arquivo para leitura e gravação em formato binário.
    # ab + -> Abre um arquivo para anexar e ler em formato binário.
    with open(filename, 'rb') as f:
        while True:
            piece = f.read(CHUNK_SIZE)
            tac = time.perf_counter()
            print(f"Lendo as Partes: ->> {tac:0.4f}")
            if len(piece) == 0:
                return
            yield chunk_pb2.Chunk(buffer=piece)

def save_chunks_to_file(chunks, filename):
    # wb   -> Abre um arquivo para gravação apenas em formato binário.
    # wb + -> Abre um arquivo para escrever e ler em formato binário.
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)
            tic = time.perf_counter()
            print(f"Escrevendo as Partes: ->> {tic:0.4f}")

class FileClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = chunk_pb2_grpc.FileServerStub(channel)

    def upload(self, in_file_name):
        print("INICIANDO UPLOADING DO ARQUIVO")
        chunks_generator = get_file_chunks(in_file_name)
        response = self.stub.upload(chunks_generator)
        assert response.length == os.path.getsize(in_file_name)
        tic = time.perf_counter()
        print(f"Enviado as Partes: ->> {tic:0.4f}")

    def download(self, target_name, out_file_name):
        print("INICIANDO DOWNLOAD DO ARQUIVO")
        response = self.stub.download(chunk_pb2.Request(name=target_name))
        save_chunks_to_file(response, out_file_name)

class FileServer(chunk_pb2_grpc.FileServerServicer):
    def __init__(self):

        class Servicer(chunk_pb2_grpc.FileServerServicer):
            def __init__(self):
                self.tmp_file_name = 'D:/teste/file.mkv'

            def upload(self, request_iterator, context):
                save_chunks_to_file(request_iterator, self.tmp_file_name)
                return chunk_pb2.Reply(length=os.path.getsize(self.tmp_file_name))

            def download(self, request, context):
                if request.name:
                    return get_file_chunks(self.tmp_file_name)

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        chunk_pb2_grpc.add_FileServerServicer_to_server(Servicer(), self.server)

    def start(self, port):
        self.server.add_insecure_port(f'[::]:{port}')
        self.server.start()

        try:
            while True:
                time.sleep(60*60*24)
        except KeyboardInterrupt:
            self.server.stop(0)
