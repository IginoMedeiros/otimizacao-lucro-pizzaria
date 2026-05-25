# [DOC-D01] frontend/Dockerfile
# --------------------------------
# Build multi-stage da imagem Docker do frontend Vue 3.
#
# Etapa 1 (build):
#   - Usa node:20-alpine (imagem mínima)
#   - Instala dependências npm
#   - Executa vite build — gera /app/dist com os arquivos estáticos otimizados
#
# Etapa 2 (serve):
#   - Usa nginx:alpine (imagem ultra-leve ~23MB)
#   - Copia apenas o /dist da etapa anterior (sem node_modules)
#   - Copia nginx.conf customizado
#   - Expõe porta 80
#
# Resultado: imagem final ~25MB, sem código-fonte ou dependências de dev

# ---- Etapa 1: Build -------------------------------------------------------
FROM node:20-alpine AS build

WORKDIR /app

# Copiar manifests primeiro (cache de camadas do Docker)
COPY package*.json ./
RUN npm install --silent

# Copiar restante do código e gerar build de produção
COPY . .
RUN npm run build

# ---- Etapa 2: Serve -------------------------------------------------------
FROM nginx:alpine AS serve

# Remover config padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar config customizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar arquivos estáticos do build
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

# Health check do container
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
