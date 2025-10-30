# pfSense VM Installation Guide on Proxmox

Este guia descreve como criar e instalar uma VM pfSense no Proxmox VE.

## 1. Preparação

- ISO pfSense: [https://www.pfsense.org/download/](https://www.pfsense.org/download/)  
- Proxmox VE já instalado e acessível.  
- Planejamento de IPs para WAN/LAN.

## 2. Criando a VM

1. No Proxmox Web UI, clique em **Create VM**.  
2. Configure:
   - Nome da VM (ex.: pfSense).  
   - ISO do pfSense.  
   - Sistema de BIOS (OVMF/UEFI recomendado).  
   - Disco: armazenamento e tamanho conforme necessidade.  
   - CPU: mínimo 2 cores.  
   - RAM: mínimo 4 GB.
3. Configure **rede**:
   - NIC1 → WAN (pode ser passthrough de placa de rede física).  
   - NIC2 → LAN (bridge interna do Proxmox).  
4. Finalize a criação.

## 3. Instalação do pfSense

1. Inicie a VM e abra o console no Proxmox.  
2. Siga o assistente de instalação do pfSense.  
   - Configure senha do admin.  
   - Configure interfaces WAN/LAN.  
3. Após instalação, acesse via browser: `https://<IP_LAN>:443`

## 4. Pós-instalação

- Atualize o pfSense para a versão mais recente.  
- Configure regras de firewall, NAT e DHCP conforme sua rede.  
- Para acesso remoto seguro, utilize VPN (OpenVPN, WireGuard) em vez de abrir portas públicas.

## 5. Referências

- [pfSense Official Documentation](https://docs.netgate.com/pfsense/en/latest/)  
- [Proxmox VE Official Documentation](https://pve.proxmox.com/wiki/Main_Page)

> ⚠️ Todos os riscos de execução são de responsabilidade do usuário. Não execute configurações sem entender o impacto na rede.

