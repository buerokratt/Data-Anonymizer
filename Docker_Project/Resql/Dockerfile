FROM maven:3.8.5-openjdk-17-slim

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

#Start application
WORKDIR /src/app
RUN ["chmod", "+x", "/usr/local/bin/entrypoint.sh"]
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]