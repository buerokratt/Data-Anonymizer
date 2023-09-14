FROM node:14-alpine
WORKDIR /usr/src/app/my-app
COPY package*.json ./
# Copy the necessary folder fom the project folder
COPY ./dm/ .
RUN npm i
EXPOSE 8002
CMD ["npm", "start"]
