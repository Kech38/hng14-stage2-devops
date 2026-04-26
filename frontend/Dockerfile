# Stage 1: Install dependencies
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Production image
FROM node:18-alpine AS production
WORKDIR /app

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy dependencies and app files
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Set correct ownership
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=10s --start-period=40s --retries=5 \
  CMD wget -qO- http://localhost:3000 || exit 1

CMD ["node", "app.js"]