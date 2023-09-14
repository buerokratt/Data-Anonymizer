FROM node:14-alpine
WORKDIR /usr/src/app/my-app
COPY package*.json ./
# Copy the necessary folder fom the project folder
COPY ./ .
RUN npm i
COPY start_server.sh ./start_server.sh
EXPOSE 5000
CMD ["sh", "start_server.sh"]
