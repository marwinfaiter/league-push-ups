# develop stage
FROM node:current-alpine3.15 as develop-stage
WORKDIR /app
COPY package*.json ./
RUN yarn install

# build stage
FROM develop-stage as build-stage
COPY . .
RUN yarn build

# production stage
FROM nginx:1.15.7-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
