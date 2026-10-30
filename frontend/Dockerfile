# Stage 1: Build the React + Vite production bundle
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies using lockfile for deterministic builds
COPY package.json package-lock.json ./
RUN npm ci

# Copy application source code
COPY . .

# Set relative API URL for reverse-proxied production deployment
ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL

# Build the production assets
RUN npm run build

# Stage 2: Serve production assets via high-performance Nginx server
FROM nginx:1.27-alpine

# Copy compiled static assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration with reverse proxy rules
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose standard HTTP port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]

