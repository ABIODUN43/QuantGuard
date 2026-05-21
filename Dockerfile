FROM node:22-alpine AS build

WORKDIR /app
ARG VITE_SERVER_BASE=http://127.0.0.1:8000
ARG VITE_API_BASE=http://127.0.0.1:8000/api/v1
ENV VITE_SERVER_BASE=$VITE_SERVER_BASE
ENV VITE_API_BASE=$VITE_API_BASE

COPY package*.json ./
RUN npm ci
COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
