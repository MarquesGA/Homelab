> [!WARNING]
> **## Nunca execute uma aplicação sem antes enteder o seu funcionamento**
> 
> **## Nunca exponha uma porta do seu roteador sem antes enteder o seu funcionamento e os riscos e se for fazer que tenha todas as medidas de segurança**

# Caddy Reverse Proxy com Docker Compose

Este guia descreve como configurar um **Caddy** como reverse proxy para múltiplos serviços internos usando Docker Compose, com suporte a certificados SSL via Cloudflare ou outras ferramentas como DuckDNS.

---

## Referências

- Código de referência: [JimsGarage Caddy](https://github.com/JamesTurland/JimsGarage/tree/main/Caddy)  
- Vídeo tutorial: [YouTube - Caddy Docker Setup](https://www.youtube.com/watch?v=ZOtUco5EwoI)  
- Alternativa DuckDNS: [YouTube - DuckDNS HTTPS](https://www.youtube.com/watch?v=qlcVx-k-02E)  

> Nota: Os vídeos estão em inglês, mas é possível usar a tradução automática do YouTube para facilitar o entendimento.

---

## O que este setup faz

- Cria um container **Caddy** usando Docker Compose.
- Configura reverse proxy para serviços internos (Jellyfin, ARR Stack, Immich, Proxmox, etc.).
- Gera certificados SSL automaticamente usando Cloudflare, DuckDNS ou qualquer outro provedor suportado.
- Mantém logs separados por serviço para facilitar auditoria e debug.
- Suporte opcional a configuração de autenticação reversa (Authelia, Authentik, etc.) para segurança adicional.

---

## Pré-requisitos

- Docker e Docker Compose instalados no host.
- Acesso ao domínio que será usado no Caddy ou conta DuckDNS/Cloudflare.
- Familiaridade básica com Linux e Docker.
- Atenção: **todas as ações são de responsabilidade do usuário**, e **não execute scripts de fontes desconhecidas** sem conhecimento completo do que fazem.

---

## Estrutura do Docker Compose

Exemplo simplificado de `docker-compose.yml`:

```yaml
services:
  caddy:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: caddy
    restart: unless-stopped
    env_file:
      - .env
    environment:
      - CLOUDFLARE_EMAIL=${CF_EMAIL}
      - CLOUDFLARE_API_TOKEN=${CF_API_TOKEN}
      - ACME_AGREE=true
    ports:
      - 80:80
      - 443:443
    volumes:
      - caddy-config:/config
      - caddy-data:/data
      - local-caddy-config:/etc/caddy
      - local-caddy-logs:/var/log/caddy

volumes:
  caddy-config:
  caddy-data:
  local-caddy-config:
  local-caddy-logs:
```

> Os caminhos locais foram **mascarados** para exemplificação. Substitua pelos diretórios do seu host, caso queira persistir configuração ou logs fora do container.

---

## Configuração de certificados SSL

### 1. Usando Cloudflare
- Crie um token API com permissões de DNS para seu domínio.
- Configure o `.env` com:
  ```env
  CF_EMAIL=seu-email@exemplo.com
  CF_API_TOKEN=seu_token_cloudflare
  ```
- Caddy irá gerar certificados SSL automaticamente para os domínios configurados no Caddyfile.

### 2. Usando DuckDNS ou outro provedor gratuito
- Você pode usar DuckDNS para gerar certificados gratuitos via ACME.
- Substitua a configuração do Caddyfile para apontar para o DuckDNS e o token correspondente.
- Mais informações: [DuckDNS + Let's Encrypt](https://www.youtube.com/watch?v=qlcVx-k-02E)

---

## Pontos extras e boas práticas

- **Persistência de dados:** Sempre monte volumes locais para `/config` e `/data` do Caddy, garantindo que alterações no container não sejam perdidas.
- **Logs separados:** Use pastas dedicadas para logs (`local-caddy-logs`) para cada serviço proxy, facilita debugging.
- **Firewall e rede:** Certifique-se de expor somente portas 80/443 para a internet (APENAS EXPOR SE SOUBER OQUE ESTÁ FAZENDO). Serviços internos devem estar em rede privada ou isolada, **não precisa expor nenhuma porta para ter certificado ssl, apenas utilize DNS Challenge como validação**.
- **Atualizações:** Mantenha Caddy e containers atualizados para receber correções de segurança.
- **Testes locais:** Antes de publicar, teste os proxys localmente para garantir que os serviços respondem corretamente.
- **Autenticação adicional:** Para segurança, considere integrar Authentik ou Authelia para acesso aos serviços críticos.
- **Backup do Caddyfile e .env:** Mantenha cópias seguras do Caddyfile e do `.env`, evitando perda de configuração em caso de falha.

---

## Cuidados

- Não compartilhe seu `.env` ou tokens de API publicamente.
- Todos os riscos de execução são de responsabilidade do usuário.
- Evite executar scripts ou Dockerfiles de fontes desconhecidas sem revisão.
- O Caddy, ao usar reverse proxy, terá acesso aos serviços internos; configure firewall e rede adequadamente.

---

## Referências adicionais

- [JimsGarage - Caddy](https://github.com/JamesTurland/JimsGarage/tree/main/Caddy)
- [YouTube - Caddy Docker Setup](https://www.youtube.com/watch?v=ZOtUco5EwoI)
- [YouTube - DuckDNS HTTPS](https://www.youtube.com/watch?v=qlcVx-k-02E)

> Este guia foi baseado em múltiplas fontes, adaptando para um uso seguro e genérico de Caddy via Docker Compose.

## Licença

Este projeto é apenas para uso pessoal e aprendizado. Use por sua conta e risco.