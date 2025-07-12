FROM redis:6.2.19



WORKDIR /app
COPY conf.conf /app
RUN mkdir /opt/redis && chown redis:redis /opt/redis
WORKDIR /opt/redis
EXPOSE 6379

CMD ["redis-server", "/app/conf.conf"]
