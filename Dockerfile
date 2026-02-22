FROM ubuntu:latest
LABEL authors="busin"

ENTRYPOINT ["top", "-b"]