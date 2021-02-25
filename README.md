# openwnms

## Scapy
```bash
sudo ln -s -f /usr/lib64/libc.a /usr/lib64/liblibc.a
```

# Install Docker
```bash
 sudo pacman -S docker docker-composer
 sudo usermod -aG docker $USER
 ```

 # Windows WMI
 ```bash
 SELECT * FROM Win32_Service WHERE State = Running
 wql = 'SELECT * FROM Win32_Service WHERE State = "Running"'
 ```