from threading import Thread
from concurrent import futures

import grpc
import demo_pb2_grpc
import demo_pb2

__all__ = 'DemoServer'
SERVER_ADDRESS = 'localhost:23333'
SERVER_ID = 1

class DemoServer(demo_pb2_grpc.GRPCDemoServicer):

     # em uma única chamada, o cliente pode enviar
     # a solicitação apenas uma vez e o servidor pode
     # responda apenas uma vez.)
    def SimpleMethod(self, request, context):
        print("SimpleMethod Chamando o Cliente(%d) a Mensagem: %s" %
              (request.client_id, request.request_data))
        response = demo_pb2.Response(
            server_id=SERVER_ID,
            response_data="Servidor Responde : Ok")
        return response

    # stream-unary (em uma única chamada, o cliente pode transferir
    # dados para o servidor várias vezes,
    # mas o servidor pode retornar uma resposta apenas uma vez.)
    def ClientStreamingMethod(self, request_iterator, context):
        print("StreamingMethod Chamada para Cliente...")
        for request in request_iterator:
            print("Requisicao para Cliente(%d), Mensagem = %s" %
                  (request.client_id, request.request_data))
        response = demo_pb2.Response(
            server_id=SERVER_ID,
            response_data="Servidor Responde : OK")
        return response

    # unary-stream (In a single call, the client can only transmit data to the server at one time,
    # but the server can return the response many times.)
    def ServerStreamingMethod(self, request, context):
        print("ServerStreamingMethod Chamada para o Cliente(%d), Mensagem = %s" %
              (request.client_id, request.request_data))

        # create a generator
        def response_messages():
            #for i in range(100):
              i = -1
              while i >= 1:
                response = demo_pb2.Response(
                    server_id=SERVER_ID,
                    response_data=("Enviada pelo Servidor, Mensagem =%d" % i))
                yield response
        return response_messages()

    # stream-stream (em uma única chamada, o cliente e o servidor
    # podem enviar e receber dados
    # entre si várias vezes.)
    def BidirectionalStreamingMethod(self, request_iterator, context):
        print("BidirectionalStreamingMethod Chamada para o Cliente...")
        # Abra um sub-thread para receber dados
        def parse_request():
            for request in request_iterator:
                print("Recebe do Cliente(%d), Mensagem = %s" %
                      (request.client_id, request.request_data))
        t = Thread(target=parse_request)
        t.start()
        #for i in range(100):
        i = -1
        while i >= 1:
            yield demo_pb2.Response(
                server_id=SERVER_ID,
                response_data=("Enviada pelo servidor, Mensagem = %d" % i))
        t.join()

def main():
    server = grpc.server(futures.ThreadPoolExecutor())
    demo_pb2_grpc.add_GRPCDemoServicer_to_server(DemoServer(), server)
    server.add_insecure_port(SERVER_ADDRESS)
    print("------------------INICIANDO GRPC SERVIDOR-------------")
    server.start()
    server.wait_for_termination()

    # If raise Error:
    #   AttributeError: '_Server' object has no attribute 'wait_for_termination'
    # You can use the following code instead:
    # import time
    # while 1:
    #     time.sleep(10)

if __name__ == '__main__':
    main()
