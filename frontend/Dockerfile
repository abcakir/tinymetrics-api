FROM node:20-alpine

WORKDIR /app

# Package-Dateien kopieren (für npm install)
COPY package*.json ./

RUN npm install

# Angular CLI global im Container installieren (damit 'ng serve' geht)
RUN npm install -g @angular/cli

COPY . .

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0"]