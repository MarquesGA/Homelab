# Proxmox VE - HomeLab Installation Guide

Este guia fornece instruções passo a passo para instalar o Proxmox VE, criar containers LXC e preparar a infraestrutura para um HomeLab seguro. Este guia é genérico e seguro, sem utilizar scripts aleatórios da internet.

## 1. Preparação

Antes de começar, tenha em mãos:

- Um servidor ou PC compatível com virtualização.
- A ISO mais recente do Proxmox VE: [https://www.proxmox.com/en/proxmox-ve/downloads](https://www.proxmox.com/en/proxmox-ve/downloads)
- Conexão com internet para atualizações.

> **Nota:** Leia a documentação oficial antes de iniciar: [Proxmox Documentation](https://pve.proxmox.com/wiki/Main_Page)

## 2. Instalação do Proxmox VE

1. Grave a ISO em um pendrive (Rufus, balenaEtcher ou similar).  
2. Configure a BIOS para inicializar pelo pendrive.  
3. Siga o assistente de instalação do Proxmox VE:  
   - Escolha o disco para instalação.  
   - Configure a senha de root e e-mail.  
   - Configure a interface de rede com IP estático recomendado.  
4. Após reinicialização, acesse o Proxmox via navegador: `https://<IP_DO_SERVIDOR>:8006`.

## 3. Configuração inicial

- Atualize o Proxmox VE:

```bash
apt update && apt full-upgrade -y
```

- Configure o repositório não-subscription (opcional):

```bash
nano /etc/apt/sources.list
# Comente a linha do enterprise e adicione:
deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription
apt update && apt full-upgrade -y
```

## 4. Criando LXC Containers

1. No Proxmox Web UI, clique em **Create CT**.  
2. Configure:
   - Hostname, password do root.
   - Template (Debian/Ubuntu recomendado).  
   - Recursos (CPU, RAM, Storage).  
3. Configure armazenamento e diretórios montados (`mp0`, `mp1`, etc) para montar pastas do host.  
4. Configure rede com IP estático ou DHCP conforme sua topologia.  
5. Finalize a criação e inicie o container.

### 4.1. Notas sobre GPU

Se quiser utilizar GPU para transcode (Jellyfin, Immich, etc.):

- Siga este guia adaptado para sua GPU: [Proxmox GPU Passthrough for LXC](https://www.reddit.com/r/Proxmox/comments/1c9ilp7/proxmox_gpu_passthrough_for_jellyfin_lxc_with/)  
- Configure corretamente os dispositivos e permissões.

## 5. Próximos passos

Após instalar o Proxmox e criar os containers LXC, você pode instalar:

- Jellyfin, Immich, ARR stack, Jellyseerr, Tailscale, AdGuard, Unbound, entre outros.  
- Utilize Docker ou Docker Compose dentro do LXC, conforme sua preferência.  
- Sempre siga boas práticas de segurança: backups, permissões corretas, atualizações regulares.

## 6. Referências

- [Proxmox VE Official Documentation](https://pve.proxmox.com/wiki/Main_Page)  
- [Proxmox GPU Passthrough (Reddit)](https://www.reddit.com/r/Proxmox/comments/1c9ilp7/proxmox_gpu_passthrough_for_jellyfin_lxc_with/)  
- [Community Scripts ProxmoxVE](https://community-scripts.github.io/ProxmoxVE/)

> ⚠️ Todos os riscos de execução são de responsabilidade do usuário. Não execute scripts desconhecidos sem entender o que fazem.
---