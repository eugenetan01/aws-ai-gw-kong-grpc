# Setup

1. run the `pip3 install -r requirements.txt`

2. run the below command to generate the necessary protocol buffers
  `python -m grpc_tools.protoc -I. --python_out=./helloworld --grpc_python_out=./helloworld hello.proto`

3. change the import statement to `from . import hello_pb2 as hello__pb2` instead of `import hello_pb2 as hello__pb2` in the hello_pb2_grpc.py file

4. run the main.py
  `python3 main.py`

5. test the client connectivity by connecting to the grpc server and ensuring it connects to localhost:50051 instead of 9080
  `python3 client.py`

4. create a docker container for the kong gateway. use the below to spin up the docker image
  ```
  docker run -d --name kong-gateway \
  --network=kong-net \
  -e "KONG_DATABASE=postgres" \
  -e "KONG_PG_HOST=kong-database" \
  -e "KONG_PG_USER=kong" \
  -e "KONG_PG_PASSWORD=kongpass" \
  -e "KONG_PROXY_ACCESS_LOG=/dev/stdout" \
  -e "KONG_ADMIN_ACCESS_LOG=/dev/stdout" \
  -e "KONG_PROXY_ERROR_LOG=/dev/stderr" \
  -e "KONG_ADMIN_ERROR_LOG=/dev/stderr" \
  -e "KONG_ADMIN_LISTEN=0.0.0.0:8001" \
  -e "KONG_ADMIN_GUI_URL=http://localhost:8002" \
  -e "KONG_PROXY_LISTEN=0.0.0.0:9080 http2, 0.0.0.0:9081 http2 ssl" \
  -e KONG_LICENSE_DATA \
  -p 8000:8000 \
  -p 8443:8443 \
  -p 8001:8001 \
  -p 8444:8444 \
  -p 8002:8002 \
  -p 8445:8445 \
  -p 8003:8003 \
  -p 8004:8004 \
  -p 9080:9080 \
  kong/kong-gateway:3.7.1.2
  ```

5. Create a service and route
  ```
  curl -XPOST localhost:8001/services \
    --data name=grpc \
    --data protocol=grpc \
    --data host=host.docker.internal \
    --data port=50051
  ```

  ```
  curl -XPOST localhost:8001/services/grpc/routes \
    --data protocols=grpc \
    --data name=catch-all \
    --data paths=/
  ```

6. Test the proxy connectivity via Kong by changing the port back to port 9080
  `python3 client.py`
