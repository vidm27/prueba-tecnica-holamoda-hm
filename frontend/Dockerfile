FROM node:22-alpine AS build
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY . .
# La URL de la API se incorpora al compilar (la consume el navegador, no el contenedor).
ARG NUXT_PUBLIC_API_BASE=http://localhost:8000
RUN pnpm generate

FROM nginx:alpine
COPY --from=build /app/.output/public /usr/share/nginx/html
# SPA: cualquier ruta devuelve index.html
RUN printf 'server {\n  listen 80;\n  root /usr/share/nginx/html;\n  location / { try_files $uri $uri/ /index.html; }\n}\n' > /etc/nginx/conf.d/default.conf
