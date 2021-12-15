FROM alpine:3.12

RUN apk update && apk add python3 && apk add py3-pip
RUN pip install p2pnetwork && pip install jsonpickle
ADD ./blockchain_demo blockchain_demo

ENTRYPOINT python3 blockchain_demo/main.py