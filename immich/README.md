# Immich Stack - Docker + LXC

Este repositório contém a configuração para rodar o **Immich** usando **Docker Compose** dentro de um container **LXC** no Proxmox. O stack inclui:

* Immich Server
* Immich Machine Learning (para reconhecimento facial e IA)
* Redis
* PostgreSQL

---

## Pré-requisitos

Antes de iniciar, certifique-se de:

1. Ter um host Proxmox atualizado.
2. Ter o suporte a GPU habilitado no host, incluindo drivers NVIDIA/Intel conforme necessário.
3. Configurar o LXC para permitir acesso à GPU (veja seção de configuração LXC abaixo).
4. Ter o Docker e Docker Compose instalados dentro do LXC.

---

## Configuração do LXC

Exemplo de configuração genérica do container LXC para o Immich:

```ini
arch: amd64
cores: 4
features: nesting=1
hostname: immich
memory: 8192

# Montagens de disco
mp0: /caminho/para/storage,mp=/mnt/sdb1
mp1: /caminho/para/postgresql,mp=/dados/postgresql
mp2: /caminho/para/uploads,mp=/usr/src/app/upload

# Rede
net0: name=eth0,bridge=vmbr0,firewall=1,hwaddr=<MAC_ADDRESS>,ip=dhcp,type=veth

onboot: 1
ostype: debian
rootfs: local-lvm:vm-105-disk-0,size=20G
swap: 4096
unprivileged: 1

# GPU (Intel/NVIDIA) permissões
lxc.cgroup2.devices.allow: c 226:0 rwm
lxc.cgroup2.devices.allow: c 226:1 rwm
lxc.cgroup2.devices.allow: c 226:128 rwm
lxc.mount.entry: /dev/dri dev/dri none bind,optional,create=dir
lxc.mount.entry: /dev/dri/renderD128 dev/renderD128 none bind,optional,create=file
lxc.cgroup2.devices.allow: c 195:0 rwm
lxc.cgroup2.devices.allow: c 195:255 rwm
lxc.cgroup2.devices.allow: c 235:0 rwm
lxc.cgroup2.devices.allow: c 235:1 rwm
lxc.cgroup2.devices.allow: c 238:1 rwm
lxc.cgroup2.devices.allow: c 238:2 rwm
lxc.mount.entry: /dev/nvidia0 dev/nvidia0 none bind,optional,create=file
lxc.mount.entry: /dev/nvidiactl dev/nvidiactl none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-uvm dev/nvidia-uvm none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-uvm-tools dev/nvidia-uvm-tools none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-caps/nvidia-cap1 dev/nvidia-caps/nvidia-cap1 none bind,optional,create=file
lxc.mount.entry: /dev/nvidia-caps/nvidia-cap2 dev/nvidia-caps/nvidia-cap2 none bind,optional,create=file

# ID mapping
lxc.idmap: u 0 100000 65536
lxc.idmap: g 0 0 1
lxc.idmap: g 1 100000 65536
```

> ⚠️ **Substitua os caminhos e o MAC address pelos corretos do seu ambiente.**

---

## Docker Compose

O `docker-compose.yml` incluído neste projeto define os serviços:

* `immich-server`: Servidor principal do Immich.
* `immich-machine-learning`: Serviço de Machine Learning para reconhecimento facial.
* `redis`: Cache do sistema.
* `database`: PostgreSQL com dados persistentes.

### Variáveis sensíveis

Todas as senhas e caminhos devem ser configurados em um arquivo `.env` no mesmo diretório do `docker-compose.yml`. Exemplo:

```env
# Caminho onde os arquivos enviados (uploads) serão armazenados
# Substitua pelo diretório que você quer usar no seu sistema
UPLOAD_LOCATION=/caminho/para/uploads

# Caminho onde os dados do banco PostgreSQL serão armazenados
# Substitua pelo diretório que você quer usar para persistência
DB_DATA_LOCATION=/caminho/para/postgresql

# Versão do Immich a ser usada, mantenha 'release' ou especifique uma versão específica
IMMICH_VERSION=release

# Nome de usuário do banco de dados
DB_USERNAME=postgres

# Senha do banco de dados
# Substitua por uma senha forte
DB_PASSWORD=sua_senha_aqui

# Nome do banco de dados
DB_DATABASE_NAME=nome_do_banco

```

> ⚠️ Não compartilhe o `.env` publicamente.

### Pontos importantes

1. `UPLOAD_LOCATION` e `DB_DATA_LOCATION` devem apontar para volumes persistentes.
2. A Machine Learning depende de GPU, portanto o host e o container devem estar configurados corretamente.
3. Recomenda-se mapear `/dev/dri` (Intel) ou `/dev/nvidia*` (NVIDIA) no LXC para aceleração de hardware.

---

## Inicialização

1. Entre no LXC:

```bash
pct enter <ID_DO_CONTAINER>
```

2. Instale Docker e Docker Compose.
3. Coloque o `docker-compose.yml` e o `.env` dentro do container.
4. Execute:

```bash
docker compose up -d
```

5. Verifique os logs para garantir que todos os serviços iniciaram:

```bash
docker compose logs -f
```

---

## Referências

Para a criação desta stack e configuração de rede, utilizei como base:

* [YouTube: JimsGarage Immich](https://www.youtube.com/watch?v=URJiQb8PwWo)
* [GitHub: JimsGarage](https://github.com/JamesTurland/JimsGarage)

Outras fontes de documentação foram consultadas para adequar o uso de LXC, Docker e GPU.

---

## Observações

* Certifique-se de que os caminhos do PostgreSQL, uploads e volumes estejam corretos.
* O container **Machine Learning** deve ter acesso à GPU corretamente configurada.
* Caso utilize NVIDIA, instale o **NVIDIA Container Toolkit** dentro do LXC, se necessário.
* Ajuste os recursos (CPU/RAM) do LXC conforme o tamanho do seu acervo e quantidade de usuários.

---
## Licença

Este projeto é apenas para uso pessoal e aprendizado. Use por sua conta e risco.

## Contato

Para dúvidas ou melhorias, consulte a documentação oficial:
* [Immich Quick Start](https://docs.immich.app/overview/quick-start)
