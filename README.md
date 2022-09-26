# NetBackup

## Usage
- Simple tool to export backups of a few network devices to a git repository
- Copy `config.sample.yml` to `config.yml` and configure your git credentials and devices
- Build the container, mount the config file to /app/config.yml and run the container

## Supported Devices
- pfSense (SSH)
- OPNsense (SSH)
- OpenWrt (Web)
- Switch OS (Web)
- Router OS (SSH)
- D-Link Smart Managed Switches (tested with DGS-1100-08) (Web)
