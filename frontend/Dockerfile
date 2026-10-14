# ── Build stage ────────────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci --prefer-offline

COPY . .
RUN npm run build


# ── Runtime stage ──────────────────────────────────────────────────────────────
FROM nginx:1.27-alpine

# Non-root: create user and update Nginx to use it
RUN addgroup -S bookease && adduser -S -G bookease bookease

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Allow non-root to write nginx cache/pid
RUN mkdir -p /var/cache/nginx /var/run /var/log/nginx \
    && chown -R bookease:bookease /var/cache/nginx /var/run /var/log/nginx /usr/share/nginx/html \
    && touch /var/run/nginx.pid \
    && chown bookease:bookease /var/run/nginx.pid

USER bookease

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
