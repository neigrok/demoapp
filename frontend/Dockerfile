# Build stage
FROM node:20-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the app
RUN npm run build

# Serve stage
FROM nginx:alpine

# Install envsubst
RUN apk add --no-cache gettext

# Copy built files to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx template
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Start nginx with environment variable substitution
CMD ["/bin/sh", "-c", "envsubst '${BACKEND_URL} ${CONSTRUCTOR_APP_PREFIX}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
