FROM node:18

RUN npm install -g pm2

WORKDIR /app

COPY package.json ./
RUN npm install --production 

COPY . .

CMD ["pm2-runtime", "Server/src/server.mjs"]  