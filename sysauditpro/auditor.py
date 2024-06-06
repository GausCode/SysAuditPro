import os
import platform
import socket
import subprocess
from datetime import datetime

def gather_system_info():
    """Sammelt grundlegende Informationen über das Betriebssystem."""
    info = {
        'Plattform': platform.system(),
        'Plattform-Release': platform.release(),
        'Plattform-Version': platform.version(),
        'Architektur': platform.machine(),
        'Hostname': platform.node(),
        'Prozessor': platform.processor()
    }
    return info

def check_security_settings():
    """Überprüft die Sicherheitseinstellungen des Systems, einschließlich Firewall und Antivirusstatus."""
    settings = {}
    os_type = platform.system().lower()

    if os_type == 'windows':
        try:
            firewall_status = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True, encoding='cp1252', errors='replace').stdout
            settings['Firewall Status'] = "Enabled" if "EIN" in firewall_status else "Disabled"
            
            antivirus_status = subprocess.run(['wmic', '/Namespace:\\\\root\\SecurityCenter2', 'Path', 'AntiVirusProduct', 'get', 'displayName,productState'], capture_output=True, text=True, encoding='cp1252', errors='replace').stdout
            settings['Antivirus'] = "Active" if "productState" in antivirus_status and "262144" in antivirus_status else "Inactive or Not Found"
        except Exception as e:
            settings['Error'] = str(e)

    elif os_type == 'linux':
        try:
            firewall_status = subprocess.run(['ufw', 'status'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
            settings['Firewall Status'] = "Active" if "active" in firewall_status.lower() else "Inactive"

            antivirus_status = subprocess.run(['clamscan', '--version'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
            settings['Antivirus'] = "Installed" if antivirus_status else "Not Installed or Not Found"
        except Exception as e:
            settings['Error'] = str(e)

    return settings

def get_network_info():
    """Erfasst Netzwerkinformationen einschließlich IP-Konfigurationen und Netzwerkverbindungen."""
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        ip_config = subprocess.run(['ipconfig' if platform.system().lower() == 'windows' else 'ifconfig'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
        open_ports = subprocess.run(['netstat', '-an'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
        return {
            'Hostname': host_name,
            'IP Address': ip_address,
            'IP Configuration': ip_config,
            'Open Ports': open_ports
        }
    except Exception as e:
        return {'Error': str(e)}

def get_installed_software():
    """Listet installierte Software auf (Beispiel für Windows-basierte Systeme)."""
    try:
        software_list = subprocess.run(['wmic', 'product', 'get', 'name,version'], capture_output=True, text=True, encoding='cp1252', errors='replace')
        installed_software = software_list.stdout
        return {'Installed Software': installed_software}
    except Exception as e:
        return {'Error': str(e)}

def get_installed_patches():
    """Listet installierte Patches und Updates auf."""
    try:
        if platform.system().lower() == 'windows':
            patches = subprocess.run(['wmic', 'qfe', 'list'], capture_output=True, text=True, encoding='cp1252', errors='replace').stdout
        else:
            patches = subprocess.run(['dpkg', '-l'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
        return {'Installed Patches': patches}
    except Exception as e:
        return {'Error': str(e)}

def get_services():
    """Listet laufende und gestoppte Dienste auf."""
    try:
        if platform.system().lower() == 'windows':
            services = subprocess.run(['sc', 'query', 'type=', 'service', 'state=', 'all'], capture_output=True, text=True, encoding='cp1252', errors='replace').stdout
        else:
            services = subprocess.run(['systemctl', 'list-units', '--type=service', '--all'], capture_output=True, text=True, encoding='utf-8', errors='replace').stdout
        return {'Services': services}
    except Exception as e:
        return {'Error': str(e)}

def get_user_info():
    """Holt Informationen über Systembenutzer und prüft, ob Passwörter funktionieren."""
    os_type = platform.system().lower()
    try:
        if os_type == 'windows':
            users = subprocess.run(['wmic', 'useraccount', 'get', 'name'], capture_output=True, text=True, encoding='cp1252', errors='replace')
        else:
            users = subprocess.run(['cut', '-d:', '-f1', '/etc/passwd'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        user_list = users.stdout
        return {'System Users': user_list}
    except Exception as e:
        return {'Error': str(e)}

def get_system_logs():
    """Zieht die letzten Einträge aus den Systemprotokollen."""
    os_type = platform.system().lower()
    try:
        if os_type == 'windows':
            logs = subprocess.run(['powershell', 'Get-WinEvent', '-LogName', 'System', '|', 'Select-Object', '-First', '10'], capture_output=True, text=True, encoding='cp1252', errors='replace')
        else:
            logs = subprocess.run(['tail', '/var/log/syslog'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        return {'System Logs': logs.stdout}
    except Exception as e:
        return {'Error': str(e)}

def get_hardware_info():
    """Sammelt detaillierte Informationen über die Hardwarekonfiguration."""
    os_type = platform.system().lower()
    try:
        if os_type == 'windows':
            cpu_info = subprocess.run(['wmic', 'cpu', 'get', 'Name'], capture_output=True, text=True, encoding='cp1252', errors='replace')
            mem_info = subprocess.run(['systeminfo'], capture_output=True, text=True, encoding='cp1252', errors='replace')
        else:
            cpu_info = subprocess.run(['lscpu'], capture_output=True, text=True, encoding='utf-8', errors='replace')
            mem_info = subprocess.run(['free', '-h'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        return {
            'CPU Info': cpu_info.stdout,
            'Memory Info': mem_info.stdout
        }
    except Exception as e:
        return {'Error': str(e)}

def perform_audit():
    """Führt das gesamte Sicherheitsaudit durch und sammelt die Ergebnisse."""
    audit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_info = gather_system_info()
    security_settings = check_security_settings()
    network_info = get_network_info()
    software_info = get_installed_software()
    patches_info = get_installed_patches()
    services_info = get_services()
    user_info = get_user_info()
    system_logs = get_system_logs()
    hardware_info = get_hardware_info()

    audit_results = {
        'Audit Time': audit_time,
        'System Information': system_info,
        'Security Settings': security_settings,
        'Network Information': network_info,
        'Installed Software': software_info,
        'Installed Patches': patches_info,
        'Services': services_info,
        'User Information': user_info,
        'System Logs': system_logs,
        'Hardware Information': hardware_info
    }
    return audit_results
