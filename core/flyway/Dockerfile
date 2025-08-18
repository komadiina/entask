FROM flyway/flyway:latest AS flyway

WORKDIR /flyway
COPY ./scripts /sql
COPY ./entrypoint.sh /flyway/entrypoint.sh

ENTRYPOINT [ "/flyway/entrypoint.sh" ]
