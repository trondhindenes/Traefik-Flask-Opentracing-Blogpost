# Traefik/Flask/Opentracing

Code and config for a blogpost that I wrote at https://medium.com/@trondhindenes/exploring-distributed-tracing-using-traefik-jaeger-and-flask-4f1835c8ed8d

### Prerequisites
You need:
- Docker
- Python3 with pip

### How to run
1. Run the jaeger opentracing all-in-one thingy. This sets up a local in-memory collector, agent and query instance:
```
docker run \
    -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 -p5775:5775/udp -p6831:6831/udp -p6832:6832/udp \
    -p5778:5778 -p16686:16686 -p14268:14268 -p9411:9411 jaegertracing/all-in-one:latest
```
2. Verify that the Jaeger query frontend is working by browsing to `http://localhost:16686`
3. In a new console window, download and run traefik (minimum version 1.6.0):
```
cd traefik
wget https://github.com/containous/traefik/releases/download/v1.6.0/traefik_linux-amd64
mv traefik_linux-amd64 traefik && chmod +x traefik
./traefik -c config.toml
```
Browse to `http://localhost:8080` to check out Traefik's web interface


4. Run the app in two separate consoles on two separate ports (this simulates two different microservices):
```
#First, install prerequisites (one-time things)
pip3 install -r app/requirements.txt

#Console 1 (run microservice1 on port 20000):
cd app
FLASK_APP_NAME=microservice1 python3 runserver.py 20000


#Console 2 (run microservice2 on port 20001):
cd app
FLASK_APP_NAME=microservice2 python3 runserver.py 20001
```

5. At this point, we can test out everything.   
`curl http://localhost:19000/service1/customers`   
Refresh the jaeger query web ui to see the produced traces

6. The following endpoints have the necessary plumbing wired up to enable "real" distributed tracing:
`curl http://localhost:19000/service1/orders`   
Refresh the jaeger query web ui to see the produced traces, noticed that this time we get a continous trace, from the traefik load balancer, thru `microservice1` and all the way to `microservice2`.
