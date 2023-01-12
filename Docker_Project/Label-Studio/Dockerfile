FROM node:14-alpine
WORKDIR /usr/src/app/my-app
COPY package*.json ./
RUN npm i
EXPOSE 5000
CMD ["npm", "run", "start"]