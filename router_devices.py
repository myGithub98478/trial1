import requests
from bs4 import BeautifulSoup
import json
import sys
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import re
import subprocess
import platform

# Disable SSL warnings
urllib3.disable_warnings(InsecureRequestWarning)

class RouterScanner:
    def __init__(self, router_ip="192.168.0.1", username="admin", password="admin"):
        self.router_ip = router_ip
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification
        
    def get_local_devices(self):
        """Get list of devices using ARP table"""
        devices = []
        try:
            # Get ARP table using system command
            if platform.system() == "Windows":
                arp_output = subprocess.check_output("arp -a", shell=True).decode()
                # Parse ARP output
                for line in arp_output.split('\n'):
                    if self.router_ip in line:
                        continue
                    match = re.search(r'([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})', line)
                    if match:
                        mac = match.group(1)
                        ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                        ip = ip_match.group(1) if ip_match else "Unknown"
                        devices.append({
                            'name': f"Device-{len(devices) + 1}",
                            'mac': mac,
                            'ip': ip
                        })
            else:
                print("This script currently only supports Windows systems")
                return []
                
            return devices
                
        except Exception as e:
            print(f"Error getting local devices: {str(e)}")
            return []

    def get_router_devices(self):
        """Try to get devices from router interface"""
        try:
            # Common router URLs for device lists
            urls = [
                f"http://{self.router_ip}/connected_devices",
                f"http://{self.router_ip}/dhcp_clients",
                f"http://{self.router_ip}/status/connected_devices",
                f"http://{self.router_ip}/status/dhcp_clients"
            ]
            
            for url in urls:
                try:
                    response = self.session.get(url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # Look for common patterns in router interfaces
                        devices = []
                        
                        # Try different common table patterns
                        tables = soup.find_all('table')
                        for table in tables:
                            rows = table.find_all('tr')
                            for row in rows:
                                cols = row.find_all(['td', 'th'])
                                if len(cols) >= 2:
                                    device = {}
                                    for col in cols:
                                        text = col.text.strip()
                                        if re.match(r'([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})', text):
                                            device['mac'] = text
                                        elif re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text):
                                            device['ip'] = text
                                        elif text and not text.startswith('IP') and not text.startswith('MAC'):
                                            device['name'] = text
                                    
                                    if 'mac' in device:
                                        if 'name' not in device:
                                            device['name'] = f"Device-{len(devices) + 1}"
                                        if 'ip' not in device:
                                            device['ip'] = "Unknown"
                                        devices.append(device)
                        
                        if devices:
                            return devices
                except:
                    continue
            
            return []
                
        except Exception as e:
            print(f"Error getting router devices: {str(e)}")
            return []

    def display_devices(self, devices):
        """Display the list of connected devices"""
        if not devices:
            print("No devices found or unable to fetch device information.")
            return
            
        print("\nConnected Devices:")
        print("-" * 60)
        print(f"{'Device Name':<20} {'MAC Address':<20} {'IP Address':<15}")
        print("-" * 60)
        
        for device in devices:
            print(f"{device['name']:<20} {device['mac']:<20} {device['ip']:<15}")

def main():
    # Create scanner instance
    scanner = RouterScanner()
    
    print("Scanning for connected devices...")
    
    # First try to get devices from router interface
    devices = scanner.get_router_devices()
    
    # If no devices found from router, try local ARP table
    if not devices:
        print("Could not get devices from router interface, trying local ARP table...")
        devices = scanner.get_local_devices()
    
    # Display devices
    scanner.display_devices(devices)

if __name__ == "__main__":
    main() 