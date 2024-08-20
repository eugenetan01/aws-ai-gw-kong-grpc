import uvicorn
from fastapi import FastAPI
from concurrent import futures
import grpc
from helloworld import hello_pb2, hello_pb2_grpc


class HelloService(hello_pb2_grpc.HelloServiceServicer):
    def SayHello(self, request, context):
        response = hello_pb2.HelloReply()
        response.message = request.prompt
        return response


def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    import threading
    grpc_thread = threading.Thread(target=serve_grpc)
    grpc_thread.start()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)
