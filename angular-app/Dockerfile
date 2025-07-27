# Stage 1: Build Angular app
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy all source files
COPY . .

# Build the Angular app in production mode
RUN npm run build -- --configuration production

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine

# Remove default nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy built Angular files from build stage
COPY --from=build /app/dist/angular-app /usr/share/nginx/html

# Expose port 80 to serve the app
EXPOSE 80

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]
