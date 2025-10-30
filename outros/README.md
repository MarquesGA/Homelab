# HomeLab Setup - Guia Genérico

Este guia tem como objetivo fornecer um ponto de partida seguro e organizado para montar um HomeLab utilizando **Proxmox VE** e várias aplicações de mídia, rede e automação, como Tailscale, AdGuard, Unbound, Jellyfin, Immich, Stack ARR, Jellyseerr e outras.

> ⚠️ **Aviso de segurança:** Todos os riscos de execução são de responsabilidade do usuário. Não execute scripts de fontes desconhecidas sem compreender completamente o que está sendo feito.

---

## 1. Referência principal

O ponto de partida recomendado é a página oficial de scripts da comunidade Proxmox:

**[ProxmoxVE Community Scripts](https://community-scripts.github.io/ProxmoxVE/)**

Nesta página você encontrará:

- **Instalação de containers LXC e VMs** pré-configuradas.
- **Scripts seguros** para instalar diversas aplicações:
  - Tailscale (VPN e rede privada)
  - AdGuard (bloqueio de anúncios e DNS)
  - Unbound (resolutor DNS seguro)
  - Jellyfin (media server)
  - Immich (gestão de fotos com AI)
  - Stack ARR (Radarr, Sonarr, Prowlarr, qBittorrent, Bazarr)
  - Jellyseerr (interface de requests para mídia)
- **Guias de configuração de rede**, volumes, permissões e passthrough de GPU.
- **Scripts da comunidade** adicionais para otimização do Proxmox e integração com containers.

> A página está em inglês, mas pode ser traduzida automaticamente pelo Google Translate embutido no navegador.

---

## 2. Configuração recomendada

1. **Instalação base do Proxmox VE**
   - Certifique-se de ter backups e de estar usando hardware compatível.
   - Evite utilizar scripts aleatórios de terceiros sem validação.

2. **Containers e VMs**
   - Prefira **LXC** para aplicações que não exigem kernel próprio, pois são mais leves.
   - Use **VMs** para aplicações que necessitem de isolamento total, como pfSense ou serviços críticos.

3. **Volumes e armazenamento**
   - Defina volumes de mídia, downloads e banco de dados de forma separada.
   - Use **paths genéricos**, substituindo pelos caminhos reais no seu sistema.
   - Exemplo genérico:
     ```text
     /path/to/media
     /path/to/downloads
     /path/to/database
     ```

4. **Rede**
   - Configure IPs estáticos dentro da sua LAN para facilitar reverse proxy e integrações.
   - Utilize **Tailscale** ou VPN própria para acesso remoto seguro.
   - Sempre configure firewall do Proxmox e de cada container/VM.

5. **GPU e Hardware Acceleration**
   - Para containers de mídia (Jellyfin, Immich), siga os guias oficiais de passthrough de GPU.
   - Assegure-se que o host tem drivers instalados e permissões corretas configuradas no LXC.

---

## 3. Docker Compose

Muitas aplicações podem ser instaladas via **Docker Compose**, simplificando futuras alterações:

- **Stack ARR**
- **Jellyseerr**
- **Immich**
- **Bazarr**
- **Flaresolverr**

> Lembre-se: configure volumes e paths de forma genérica e substitua pelos caminhos reais do seu sistema.

---

## 4. Reverse Proxy e SSL

- Pode ser configurado via **Caddy** ou **NGINX**.
- Pode-se usar **Cloudflare** para SSL, ou alternativas gratuitas como **DuckDNS**.
- Certifique-se de que o certificado é válido e que o proxy não expõe portas críticas diretamente à internet.
- Referências úteis:
  - [Caddy com Docker Compose](https://github.com/JamesTurland/JimsGarage/tree/main/Caddy)
  - Vídeo de exemplo: [YouTube - Caddy Reverse Proxy](https://www.youtube.com/watch?v=ZOtUco5EwoI)

---

## 5. Boas práticas de segurança

- Não execute scripts de fontes desconhecidas.
- Faça backups frequentes do Proxmox e de dados importantes.
- Utilize `.env` para armazenar senhas e tokens de forma segura.
- Limite acessos via firewall e VPN.
- Monitore logs de aplicações e containers regularmente.

---

## 6. Observações finais

- Este guia é **genérico e seguro**, serve como base para construir seu próprio HomeLab.
- A **página de scripts da comunidade ProxmoxVE** deve ser seu guia principal, pois oferece métodos confiáveis e testados.
- Ao seguir este guia, você terá um ambiente modular, fácil de manter e seguro, pronto para evoluir com novas aplicações.

> ⚠️ **Lembre-se:** todos os riscos de execução são de responsabilidade do usuário. Sempre revise scripts e configurações antes de aplicar em produção.