> [!WARNING]
> **## Nunca execute uma aplicação sem antes enteder o seu funcionamento**
> 
# Jellyfin - Proxmox LXC / Docker Compose

Este repositório/documentação descreve a configuração de um servidor **Jellyfin** utilizando **Proxmox LXC** e **Docker Compose**, incluindo suporte a GPU para transcoding.

---

## Estrutura geral

- **Jellyfin** rodando dentro de um **LXC container** no Proxmox.
- Configuração inicial do LXC pode ser feita com o script:
  [Proxmox Community Scripts](https://community-scripts.github.io/ProxmoxVE/)
- Para configuração via Docker Compose:
  [JimsGarage Jellyfin Compose](https://github.com/JamesTurland/JimsGarage/tree/main/Jellyfin)
- Suporte a GPU para transcode baseado em:
  [Proxmox GPU Passthrough para Jellyfin LXC](https://www.reddit.com/r/Proxmox/comments/1c9ilp7/proxmox_gpu_passthrough_for_jellyfin_lxc_with/)

---

## Passo 1: Criar LXC no Proxmox

Exemplo de configuração genérica de LXC para Jellyfin:

```ini
arch: amd64
cores: 2
features: nesting=1
hostname: jellyfin
memory: 8192

# Montagens de volumes - substitua pelos diretórios do seu sistema
mp1: /caminho/para/filmes,mp=/movies-hd
mp2: /caminho/para/series,mp=/series-hd

# Configuração de rede
net0: name=eth0,bridge=vmbr0,firewall=1,hwaddr=XX:XX:XX:XX:XX:XX,ip=IP_DO_CONTAINER/24,gw=IP_DO_GATEWAY,type=veth

onboot: 1
ostype: debian
rootfs: local-lvm:vm-ID-disk-0,size=36G
swap: 4096
unprivileged: 1

# Dispositivos e permissões para GPU
lxc.cgroup2.devices.allow: c 226:0 rwm
lxc.cgroup2.devices.allow: c 226:1 rwm
lxc.cgroup2.devices.allow: c 226:128 rwm
lxc.mount.entry: /dev/dri dev/dri none bind,optional,create=dir
lxc.mount.entry: /dev/dri/renderD128 dev/renderD128 none bind,optional,create=file

# Dispositivos NVIDIA para passthrough (se aplicável)
lxc.mount.entry: /dev/nvidia0 dev/nvidia0 none bind,optional,create=file
lxc.mount.entry: /dev/nvidiactl dev/nvidiactl none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-uvm dev/nvidia-uvm none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-uvm-tools dev/nvidia-uvm-tools none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-caps/nvidia-cap1 dev/nvidia-caps/nvidia-cap1 none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-caps/nvidia-cap2 dev/nvidia-caps/nvidia-cap2 none bind,optional,create=file

# Mapamento de IDs para usuário não privilegiado
lxc.idmap: u 0 100000 65536
lxc.idmap: g 0 0 1
lxc.idmap: g 1 100000 65536
```

> ⚠️ Substitua todos os caminhos `/caminho/para/...` pelos diretórios do seu sistema.

---

## Passo 2: Configuração do Docker Compose

Exemplo básico de Docker Compose para Jellyfin:

```yaml
version: "3.8"

services:
  jellyfin:
    image: linuxserver/jellyfin:latest
    container_name: jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/Sao_Paulo
    volumes:
      - /caminho/para/config:/config
      - /caminho/para/midias:/media
    ports:
      - 8096:8096
    restart: unless-stopped
```

- `/caminho/para/config`: diretório onde o Jellyfin armazenará a configuração.
- `/caminho/para/midias`: diretório onde estarão seus filmes, séries e demais mídias.
- Ajuste o `PUID` e `PGID` para o usuário que terá acesso aos arquivos.

---

## Passo 3: Configuração da GPU para transcoding

Para habilitar GPU no LXC, siga o guia adaptado para a sua GPU:  
[Proxmox GPU Passthrough para Jellyfin LXC](https://www.reddit.com/r/Proxmox/comments/1c9ilp7/proxmox_gpu_passthrough_for_jellyfin_lxc_with/)

- Certifique-se de que os drivers da GPU estão instalados no host.
- Monte os dispositivos corretamente no container (como mostrado na seção LXC acima).
- Para Intel/AMD/NVIDIA, siga as instruções específicas de cada fabricante.

---

## Passo 4: Inicializar o container

```bash
pct start <ID_DO_CONTAINER>
```

- Acesse via navegador: `http://IP_DO_CONTAINER:8096`
- Siga a configuração inicial do Jellyfin para criar o usuário administrador e adicionar bibliotecas.

---

## Referências utilizadas

- [Proxmox Community Scripts](https://community-scripts.github.io/ProxmoxVE/)
- [JimsGarage - Jellyfin Docker Compose](https://github.com/JamesTurland/JimsGarage/tree/main/Jellyfin)
- [GPU Passthrough Jellyfin LXC Reddit](https://www.reddit.com/r/Proxmox/comments/1c9ilp7/proxmox_gpu_passthrough_for_jellyfin_lxc_with/)

> Esta documentação é baseada nessas fontes e adaptada para meu setup pessoal, incluindo caminhos e configuração de GPU específicos.

---

## Notas

- Todos os caminhos no exemplo estão mascarados, substitua pelos diretórios do seu sistema.
- Para múltiplas bibliotecas, monte volumes adicionais e adicione no Docker Compose ou na configuração do LXC.
- Se houver necessidade de transcoding pesado (4K HDR), recomenda-se usar uma GPU dedicada com passthrough a NVIDIA limita GPUs "comerciais" para até 3 processos em paralelo, para uso maior existem alguns tutoriais de como "destravar" ou você precisa comprar uma gpu de "trabalho" como da linha Quadro .

## Licença

Este projeto é apenas para uso pessoal e aprendizado. Use por sua conta e risco.