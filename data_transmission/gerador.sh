python -m grpc_tools.protoc -IC../Users/usuario/Documents/Dev/gRPC-Python/data_transmission/protos --python_out=.
--grpc_python_out=. ../Users/usuario/Documents/Dev/gRPC-Python/data_transmission/protos/demo.proto
python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/example.proto