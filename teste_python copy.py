import ntplib
import re
import subprocess
import shlex

def extract_ips(result):
    # Expressão regular para encontrar os IPs IPv4
    ipv4_ip_pattern = re.compile(r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}')

    # Expressão regular para encontrar os IPs IPv6
    ipv6_ip_pattern = re.compile(r'([\da-fA-F:]+(?:::[\da-fA-F]*)?)')

    ips = []

    #ips.extend(ipv6_ip_pattern.findall(result))
    
    ips.extend(ipv4_ip_pattern.findall(result))

    return ips

ips=[]

#ips2 = ['177.124.130.31','177.36.137.30']

try:
    with open('dns_ips.txt', 'r') as file:
        for line in file:
            ips.extend(extract_ips(line.strip()))
except FileNotFoundError:
    print("Arquivo 'ips.txt' não encontrado.")
    exit()

print("Buscando...")
with open('resultado.txt', 'w') as file:
    for ip in ips:
        command = f"dig @{ip} www.google.com"
        try:
            result = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            if result.returncode == 0:
                response = result.stdout.decode('utf-8').strip()
                #print("Response:", response)
                match = re.search(r'ANSWER:\s+(\d+)', response)
                if match:
                    answer_count = int(match.group(1))
                    if answer_count >= 1:
                        file.write(f"IP: {ip}, ANSWER count: {answer_count}\n")
            else:
                print("Command execution failed with error:", result.stderr.decode('utf-8').strip())
        except subprocess.TimeoutExpired:
            print("Timeout occurred while executing the command")
        except OSError as e:
            print(f"Error executing command: {e}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
        #print("--"*15)

print("rodei até aqui")
