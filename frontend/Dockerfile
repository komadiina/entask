FROM node:22.9.0 AS builder

WORKDIR /frontend

RUN npm i -g npm@10.8.3

COPY package*.json .
RUN npm i

COPY . .
RUN npm i -s -g @angular/cli@19
RUN npm i -s -g @angular/compiler-cli@19 @angular/language-service@19 @angular-devkit/build-angular@19

EXPOSE 4200
CMD ["ng", "serve", "--host", "0.0.0.0", "--poll", "1000"]
