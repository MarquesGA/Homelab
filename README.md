# 🧠 Projeto HomeLab & Raspberry Pi — Gabriel Marques

> **Aviso Legal:**  
> Este projeto foi criado **exclusivamente para uso pessoal e educacional**.  
> Não há qualquer intuito comercial, e o autor **não se responsabiliza por qualquer uso indevido** do material aqui descrito.  
> Todos os dados sensíveis (IPs, tokens, chaves, senhas) foram **intencionalmente ocultados ou substituídos**.
___
> Este projeto foi desenvolvimento durante muitos meses, como hobby, eu não sou especialista na área, apenas uma pessoa curiosa e que gosta de resolver problemas. Todo o projeto foi pensado para ser gratuito ou o mais barato possivel, o gasto feito foi apenas em peças de hardware, um domínio para SSL (Opcional), assinatura da VPN (Opcional mas altamente recomendado) e tempo livre.
> 
> O hardware foi comprado usado ou com excelentes descontos, você não precisa de nada parecido para começar, eu iniciei com uma IPX3060E uma placa mãe com processador integrado de 2 cores e 2 Threads de 2016 com 1gb de ram usando CasaOS, gastei 50 reais, e o gabinete era a própria caixa. 

---

### 💾 Hardware Base

- **CPU:** AMD Ryzen 5 5600  
- **RAM:** 32 GB DDR4 (2x16GB 3200)  
- **Placa-mãe:** MSI A520 A-PRO  
- **GPU:** RTX 3050 (usada para transcoding e IA no Immich)  
- **Armazenamento:**  
  - SSD SanDisk Ultra 3D 500 gb → Sistema + LXC + VMs  
  - SSD SanDisk 1 TB → Dados do Immich
  - SSD SanDisk 500 gb → Backup e Snapshots
  - HDD 4 TB → Biblioteca de mídia do Jellyfin (disco usado)  
- Raspberry Pi 3 modelo B+
  - SSD Kingston 120 gb
  - MicroSD 64gb

---

## 🎯 Objetivo

Este projeto nasceu do desejo de aprender e compartilhar conhecimento sobre **Home Labs**, **virtualização**, **automação**, **armazenamento de mídia**, **backup** e **infraestrutura doméstica**.  
O conteúdo aqui documentado foi pensado especialmente para **falantes de português**, já que a maior parte do material disponível sobre o tema está em **inglês**.

A intenção é **ajudar iniciantes** a compreender o processo de criação de um ambiente funcional com **Proxmox VE**, **containers LXC não privilegiados**, **pfSense virtualizado** e um **Raspberry Pi** usado como nó auxiliar para automações e mídia.

---

## 🧩 Estrutura Geral

### 🖥️ HomeLab Proxmox

| Tipo | Nome | Função | Notas |
|------|------|--------|-------|
| VM | pfSense | Firewall, VLANs, DHCP e bloqueios IP | 2 vCPUs / 8GB RAM, passthrough de rede WAN |
| LXC | Jellyfin | Servidor de mídia com aceleração GPU | HDD 4TB exclusivo |
| LXC | ARR Stack | qBittorrent (Gluetun + NordVPN), Radarr, Sonarr, Prowlarr, Bazarr, Jellyseerr | Jellyseerr integrado com Discord via API |
| LXC | Immich | Backup e IA para fotos | SSD 1TB dedicado e Servidor de mídia com aceleração GPU |
| LXC | Tailscale | Acesso remoto seguro | Integração com o sistema para acesso externo |
| LXC | AdGuard (prod) | DNS filtrado | Adblock, bloqueio de aplicativos e filtros |
| LXC | AdGuard (testes) | Ambiente de testes | Utilizado para testes como a latência do Unbound, filtros... |
| LXC | Unbound | DNS recursivo com DNSSEC | Integrado ao AdGuard |
| LXC | Caddy | Proxy reverso e HTTPS (Cloudflare (Grey cloud) + Certbot) | Utilizo apenas para certificado SSL |
| LXC | Backup-Server | Snapshots e sincronizações | Scripts automáticos |
| Outros | Containers auxiliares | Scripts, monitoramento e testes | Use para testes e aprendizado |

---

### 🧠 Arquitetura e Segurança

- Todos os containers LXC são **unprivileged**, garantindo isolamento e segurança.  
- O **pfSense** está virtualizado e realiza segmentação via **VLANs**: LAN, Mídia, IoT, Serviços, Testes.  
- **AdGuard + Unbound**: controle DNS com resolução local, bloqueios por categorias e segurança DNSSEC.  
- **Caddy** atua como proxy reverso com HTTPS automatizado usando Cloudflare + Certbot.  
- **Tailscale** oferece acesso remoto privado, sem necessidade de port forwarding (ideal para usuários sob CGNAT).  
- **Backups automáticos** com scripts e Proxmox Backup Server (PBS).  

---
## 🍓 Raspberry Pi — Nó Auxiliar
### 🧩 Objetivo
O Raspberry Pi (Raspberry Pi 3b+) foi usado inicialmente como plataforma de **testes de boot múltiplo** e aprendizado com **PINN**, evoluindo depois para um ambiente de mídia e automação leve com **DietPi + Kodi** em SSD.

### 🔹 Fase 1 — PINN e experimentação
- Uso do PINN para instalar e testar múltiplos sistemas (DietPi, LibreELEC, Raspberry Pi OS).  
- Entendimento de partições, boots múltiplos e comportamento do Pi.  
- Experimentos de rede e desempenho via microSD.

### 🔹 Fase 2 — Migração para SSD + DietPi
- Instalação do **DietPi** em SSD USB (melhor performance e durabilidade).  
- Instalação do **Kodi** como media center conectado à TV via HDMI.  
- Montagem automática das mídias remotas do Jellyfin via SMB/NFS.  
- Integração com o tailscale para acesso remoto
- Integração futura com Home Assistant e Pi-hole (em testes).  

---

## ⚙️ Scripts e Docker Compose

- Alguns containers foram criados via **docker-compose**, outros diretamente pelo Proxmox LXC.
- Scripts de instalação e manutenção adaptados de:  
  🔗 [Community Scripts for Proxmox VE](https://community-scripts.github.io/ProxmoxVE/)  
- Arquivos `docker-compose.yml` incluem integrações com VPN (Gluetun), automação do ARR Stack, e Immich.  
- Informações sensíveis foram substituídas por placeholders `<REDACTED_...>`.

---

## 🌐 Comunidade e Referências

O projeto foi desenvolvido com base em conhecimento adquirido de múltiplas fontes, incluindo criadores de conteúdo e comunidades técnicas, com muitos meses de estudos e dedicação e bastante IA para o troubleshooting:

### 📺 YouTube
- [Jim’s Garage](https://www.youtube.com/@Jims-Garage)  
- [Wolfgang’s Channel](https://www.youtube.com/@WolfgangsChannel)  
- [Hardware Haven](https://www.youtube.com/@HardwareHaven)  
- [Techno Tim](https://www.youtube.com/@TechnoTim)  
- [SauberLab](https://www.youtube.com/@SauberLab)

### 💬 Comunidades e Fóruns
- [Reddit — GPU passthrough for Jellyfin LXC](https://www.reddit.com/r/Proxmox/comments/1c9ilp7/proxmox_gpu_passthrough_for_jellyfin_lxc_with/)  
- [StackOverflow](https://stackoverflow.com)  
- [Proxmox Forums](https://forum.proxmox.com)  
- [r/homelab](https://www.reddit.com/r/homelab)  
- [r/selfhosted](https://www.reddit.com/r/selfhosted)

### 📘 Projetos e Documentações Oficiais
- [Proxmox VE](https://www.proxmox.com/)  
- [Immich](https://immich.app/)  
- [DietPi](https://dietpi.com)  
- [PINN](https://github.com/procount/pinn)  
- [Jellyfin](https://jellyfin.org)  
- [Radarr](https://radarr.video) / [Sonarr](https://sonarr.tv) / [Prowlarr](https://prowlarr.com)

---

## 🙌 Objetivo Comunitário

O principal propósito deste projeto é **ampliar o acesso a conteúdo técnico em língua portuguesa**, criando uma ponte entre o conhecimento global (majoritariamente em inglês) e a comunidade lusófona interessada em tecnologia, homelabs e automação.

> 💡 Se este repositório te ajudou, considere contribuir com melhorias, traduções ou feedbacks para torná-lo ainda mais útil a outros iniciantes.

---

## 📜 Licença

Distribuído sob a licença **MIT** — uso e modificação livres para fins pessoais e educacionais, mantendo créditos ao autor.

**Autor:** Gabriel Marques 🇧🇷  
