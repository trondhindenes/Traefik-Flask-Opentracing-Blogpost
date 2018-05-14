# Traefik/Flask/Opentracing

Code and config for a blogpost that I wrote


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
#Console 1 (run microservice1 on port 20000):
cd app && python3 app.py 20000 microservice1


#Console 2 (run microservice2 on port 20001):
cd app && python3 app.py 20001 microservice2
```

5. At this point, we can test out everything. This request to `service1` will make `service1` invoke `service2` so we can test that distributed tracing works:   
`curl http://localhost:9000/service1/customer`   
Refresh the jaeger query web ui to see the produced traces

6. To see in-app instrumentation, browse to the following url:
`curl http://localhost:9000/service1/orders`   
Refresh the jaeger query web ui to see the produced traces