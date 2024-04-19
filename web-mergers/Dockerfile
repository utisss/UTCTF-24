# specify the node base image with your desired version node:<version>
FROM node:20
WORKDIR /usr/src/app
COPY package*.json ./

RUN npm install
RUN npm ci --omit=dev
COPY . .

CMD [ "node", "app.js" ]

# replace this with your application's default port
EXPOSE 8725