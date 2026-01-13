import csv
from collections import Counter

INPUT_CSV = "tcpdump_parsed.csv"
OUTPUT_MD = "report.md"

def load_csv():
    rows = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            rows.append(row)
    return rows

def top(counter, n=10):
    return counter.most_common(n)

def write_section(f, title, data, headers=("Valeur", "Nombre")):
    f.write(f"## {title}\n\n")
    f.write(f"| {headers[0]} | {headers[1]} |\n")
    f.write("|---|---|\n")
    for key, value in data:
        f.write(f"| {key} | {value} |\n")
    f.write("\n")

def main():
    rows = load_csv()

    src_ips = Counter(r["src_ip"] for r in rows)
    dst_ips = Counter(r["dst_ip"] for r in rows)
    dst_ports = Counter(r["dst_port"] for r in rows)
    flags = Counter(r["flags"] for r in rows)

    ssh_rows = [r for r in rows if r["dst_port"] == "22" or r["src_port"] == "22"]
    dns_rows = [r for r in rows if r["dst_port"] == "53" or r["src_port"] == "53"]
    http_rows = [r for r in rows if r["dst_port"] == "80" or r["src_port"] == "80"]

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# Rapport d'analyse du trafic réseau\n\n")
        f.write(f"Total de paquets analysés : **{len(rows)}**\n\n")

        write_section(f, "Top 10 IP sources", top(src_ips))
        write_section(f, "Top 10 IP destinations", top(dst_ips))
        write_section(f, "Top 10 ports de destination", top(dst_ports), headers=("Port", "Nombre"))
        write_section(f, "Distribution des flags TCP", top(flags), headers=("Flag", "Nombre"))

        f.write("## Analyse SSH (port 22)\n\n")
        f.write(f"Total de paquets SSH : **{len(ssh_rows)}**\n\n")
        write_section(f, "Top IP impliquées dans SSH", top(Counter(r['src_ip'] for r in ssh_rows)))

        f.write("## Analyse DNS (port 53)\n\n")
        f.write(f"Total de paquets DNS : **{len(dns_rows)}**\n\n")
        write_section(f, "Top IP impliquées dans DNS", top(Counter(r['src_ip'] for r in dns_rows)))

        f.write("## Analyse HTTP (port 80)\n\n")
        f.write(f"Total de paquets HTTP : **{len(http_rows)}**\n\n")
        write_section(f, "Top IP impliquées dans HTTP", top(Counter(r['src_ip'] for r in http_rows)))

    print(f"Rapport Markdown généré : {OUTPUT_MD}")

if __name__ == "__main__":
    main()
