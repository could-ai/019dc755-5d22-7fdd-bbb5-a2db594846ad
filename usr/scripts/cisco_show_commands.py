#!/usr/bin/env python3
import argparse
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def run_show_commands(device, commands):
    try:
        print(f"Connecting to {device['host']}...")
        net_connect = ConnectHandler(**device)
        
        # If an enable secret is provided, enter enable mode
        if device.get('secret'):
            net_connect.enable()
        
        for cmd in commands:
            print(f"\n{'='*50}")
            print(f"Output for '{cmd}' on {device['host']}")
            print(f"{'='*50}")
            output = net_connect.send_command(cmd)
            print(output)
            
        net_connect.disconnect()
        print(f"\nDisconnected from {device['host']}")
        
    except NetmikoAuthenticationException:
        print(f"Authentication failed for {device['host']}")
    except NetmikoTimeoutException:
        print(f"Connection timed out for {device['host']}")
    except Exception as e:
        print(f"Error connecting to {device['host']}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run show commands on Cisco devices over a Linux machine")
    parser.add_argument("--host", required=True, help="Device IP or hostname")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--secret", help="Enable secret (optional)", default="")
    parser.add_argument("--commands", nargs="+", default=["show version", "show ip int brief"], help="List of show commands to run (space separated)")
    parser.add_argument("--type", default="cisco_ios", help="Device type (default: cisco_ios). Can be cisco_nxos, cisco_xe, etc.")
    
    args = parser.parse_args()
    
    device = {
        "device_type": args.type,
        "host": args.host,
        "username": args.username,
        "password": args.password,
        "secret": args.secret,
    }
    
    run_show_commands(device, args.commands)
