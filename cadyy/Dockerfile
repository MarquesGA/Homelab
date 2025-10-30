# Para producao e melhor deixar uma versao fixa: exemplo, 2.9.1-builder
FROM caddy:builder AS builder

RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
FROM caddy:latest

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
