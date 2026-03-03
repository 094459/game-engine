FROM eclipse-temurin:21-jdk-alpine

RUN addgroup -S sandbox && adduser -S sandbox -G sandbox

WORKDIR /sandbox
RUN chown sandbox:sandbox /sandbox

USER sandbox

ENTRYPOINT ["sh", "-c"]
