> [!WARNING]
> **## Nunca execute uma aplicação sem antes enteder o seu funcionamento**

# ARR Stack Docker

Este repositório contém a configuração para rodar uma **ARR stack** (Automation, Radarr, Sonarr, etc.) usando Docker, baseada no `docker-compose.yml` fornecido. A stack inclui: qBittorrent, Sonarr, Radarr, Prowlarr, Bazarr, Jellyseerr, FlareSolverr, Gluetun (VPN) e um bot Discord opcional para integração com Jellyseerr.

---

## Estrutura da Stack

- **Gluetun:** container VPN que protege os serviços de download (qBittorrent, Sonarr, Radarr, Prowlarr, FlareSolverr).
- **qBittorrent:** responsável pelos downloads de torrents. O caminho de downloads do qBittorrent é separado do caminho que o Sonarr e Radarr usam, pois após o download completo os arquivos são copiados para os HDs.
- **Sonarr / Radarr:** automatizam o gerenciamento de séries e filmes, monitorando pastas e renomeando arquivos.
- **Prowlarr:** gerenciador de indexadores, centralizando pesquisas para Sonarr e Radarr.
- **Bazarr:** gerenciador de legendas, integrado ao Sonarr e Radarr.
- **Jellyseerr:** interface de pedidos de mídia, conectada ao Jellyfin.
- **FlareSolverr:** usado para contornar captchas em serviços de indexadores.
- **Jellycord Bot:** opcional, integra o Jellyseerr ao Discord.

---

## Pré-requisitos

1. **Docker e Docker Compose** instalados no servidor.
2. Criação de pastas locais para armazenar downloads, mídia e configuração dos containers.
3. Um arquivo `.env` com as variáveis sensíveis.

Exemplo mínimo de `.env`:

```env
# Caminhos locais
UPLOAD_LOCATION=/caminho/para/uploads
DB_DATA_LOCATION=/caminho/para/postgres

# Timezone
TZ=America/Sao_Paulo

# Versão do Immich (caso use Immich)
IMMICH_VERSION=release

# Banco de dados
DB_PASSWORD=<SUA_SENHA_AQUI>
DB_USERNAME=postgres
DB_DATABASE_NAME=immich

# NordVPN (para Gluetun)
OPENVPN_USER=<SEU_USUARIO_NORDVPN>
OPENVPN_PASSWORD=<SUA_SENHA_NORDVPN>
```

> Substitua `<SUA_SENHA_AQUI>` e `<SEU_USUARIO_NORDVPN>` pelas suas credenciais reais.

---

## Configuração do Docker Compose

1. Clone ou copie o `docker-compose.yml` para o servidor.
2. Crie e configure o arquivo `.env` como mostrado acima.
3. Ajuste os caminhos das pastas nos volumes do `docker-compose.yml` para refletirem seus diretórios locais.

Exemplo de caminhos genéricos no `docker-compose.yml`:

```yaml
volumes:
  - /caminho/para/docker/qbittorrent:/config
  - /caminho/para/downloads/completos:/data/torrents/completos
  - /caminho/para/downloads/incompletos:/data/torrents/incompletos
```

> Note que o caminho do qBittorrent é **diferente** do caminho usado pelo Sonarr e Radarr (`/downloads`), porque após o término do download os arquivos são copiados para o HD principal.

4. Suba a stack:

```bash
docker-compose up -d
```

5. Verifique se todos os containers estão rodando corretamente:

```bash
docker ps
```

6. Acesse os serviços via browser utilizando as portas definidas no `docker-compose.yml`.

---

## Observações

- Todos os containers que precisam de acesso à internet para baixar conteúdo são protegidos pelo Gluetun (VPN).
- É recomendado criar **usuários específicos no servidor** para rodar os containers com PUID/PGID, garantindo permissões corretas de leitura e escrita.
- O bot Jellycord integra o Jellyseerr ao Discord, permitindo solicitar mídia diretamente via chat.

---

## Referências

Esta configuração foi baseada em várias fontes de aprendizado e experimentação, incluindo:

- Vídeo explicativo sobre ARR Stack: [YouTube](https://www.youtube.com/watch?v=GPouykKLqbE)
- Base para configuração de rede e Docker: [JimsGarage](https://github.com/JamesTurland/JimsGarage)

> Nota: O caminho do qBittorrent é diferente do Sonarr/Radarr. Baixo no qBittorrent e depois faço uma cópia para o HD principal após o término do download.

---

## Licença

Este projeto é apenas para uso pessoal e aprendizado. Use por sua conta e risco.

> [!WARNING]
> **## Nunca execute uma aplicação sem antes enteder o seu funcionamento**
