FROM node:20-bullseye as build
WORKDIR /app
RUN apt update -y \
    && apt install -y python2-minimal \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

ARG NPM_CONFIG_REGISTRY=""
ARG YARN_REGISTRY=""

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy build dependencies
COPY ./src ./src
COPY ./public ./public
COPY index.html ./
COPY .eslintrc.js ./
COPY .env.production ./
COPY vite.config.mjs ./
COPY jsconfig.json ./


RUN npm run build

FROM nginx:1.27-alpine
WORKDIR /var/www
COPY .deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY .deploy/podosintovik.org.crt /etc/nginx/ssl/podosintovik.org.crt
COPY .deploy/podosintovik.org.key /etc/nginx/ssl/podosintovik.org.key

RUN nginx -t
COPY --from=build /app/dist /var/www

# Used by entrypoint.sh to replace environment variables from .env.production in javascript files
ENV JS_FILES=/var/www/js/*.js
ENV HTML_FILES=/var/www/*.html

COPY .deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
