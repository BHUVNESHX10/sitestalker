 
import tkinter as tk
from tkinter import scrolledtext, messagebox
import whois
import socket
import dns.resolver
import requests

def perform_osint(domain):
    result = ""

    # WHOIS Info
    try:
        w = whois.whois(domain)
        result += f"📄 WHOIS Info:\n"
        for key, value in w.items():
            result += f"{key}: {value}\n"
    except Exception as e:
        result += f"❌ WHOIS error: {e}\n\n"

    # IP Address
    try:
        ip = socket.gethostbyname(domain)
        result += f"\n🌐 IP Address: {ip}\n"
    except Exception as e:
        result += f"❌ IP Lookup error: {e}\n\n"

    # DNS Records
    try:
        result += f"\n🧾 DNS Records:\n"
        for record_type in ['A', 'MX', 'NS', 'TXT']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                for rdata in answers:
                    result += f"{record_type}: {rdata}\n"
            except:
                result += f"{record_type}: Not found\n"
    except Exception as e:
        result += f"❌ DNS error: {e}\n\n"

    # SSL Info (basic check using requests)
    try:
        r = requests.get(f'https://{domain}', timeout=5)
        result += f"\n🔒 SSL Status: Available (Status Code: {r.status_code})\n"
    except:
        result += f"\n🔒 SSL Status: Not reachable via HTTPS\n"

    return result


def on_scan_click():
    domain = domain_entry.get().strip()
    if not domain:
        messagebox.showwarning("Input Error", "Please enter a domain.")
        return

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"🔍 Scanning {domain}...\n\n")
    root.update()

    result = perform_osint(domain)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, result)


# GUI Setup
root = tk.Tk()
root.title("SiteStalker - OSINT GUI Tool")
root.geometry("700x600")

tk.Label(root, text="Enter Domain:", font=("Arial", 12)).pack(pady=5)
domain_entry = tk.Entry(root, font=("Arial", 12), width=50)
domain_entry.pack(pady=5)

tk.Button(root, text="Scan Domain", command=on_scan_click, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

output_box = scrolledtext.ScrolledText(root, font=("Consolas", 11), wrap=tk.WORD)
output_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
