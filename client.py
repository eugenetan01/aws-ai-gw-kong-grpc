import grpc
from helloworld import hello_pb2, hello_pb2_grpc

def run():
    # Point to Kong instead of the gRPC server directly
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.HelloServiceStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(prompt='Eugene'))
    print("Client received: " + response.message)

if __name__ == '__main__':
    run()
