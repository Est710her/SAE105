import csv

INPUT_FILE = "DumpFile.txt"
OUTPUT_CSV = "tcpdump_parsed.csv"

# Conversion des noms de services en ports numériques
SERVICE_PORTS = {
    "ssh": "22",
    "domain": "53",
    "http": "80",
    "https": "443"
}

def extract_ip_port(token):
    """
    Transforme :
    - BP-Linux8.ssh
    - 192.168.190.130.50019
    - ns1.lan.rt.domain
    en (ip/host, port)
    """
    token = token.replace(":", "").strip()
    parts = token.split(".")

    if len(parts) < 2:
        return token, "?"

    last = parts[-1]
    host = ".".join(parts[:-1])

    # Si le dernier élément est un nom de service (ssh, domain…)
    if last in SERVICE_PORTS:
        port = SERVICE_PORTS[last]
    else:
        port = last

    return host, port

def parse_line(line):
    if " IP " not in line or "Flags" not in line:
        return None

    parts = line.split()
    if len(parts) < 5:
        return None

    time = parts[0]
    proto = parts[1]

    src_token = parts[2]
    dst_token = parts[4]

    src_ip, src_port = extract_ip_port(src_token)
    dst_ip, dst_port = extract_ip_port(dst_token)

    # Flags
    flag_start = line.find("[")
    flag_end = line.find("]")
    flags = line[flag_start+1:flag_end] if flag_start != -1 else "?"

    # Length
    length = "0"
    if "length" in line:
        try:
            length = line.split("length")[-1].strip().split()[0]
        except:
            pass

    return {
        "time": time,
        "proto": proto,
        "src_ip": src_ip,
        "src_port": src_port,
        "dst_ip": dst_ip,
        "dst_port": dst_port,
        "flags": flags,
        "length": length
    }

def main():
    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            parsed = parse_line(line)
            if parsed:
                rows.append(parsed)

    fieldnames = ["time", "proto", "src_ip", "src_port", "dst_ip", "dst_port", "flags", "length"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV propre généré : {OUTPUT_CSV} ({len(rows)} lignes)")

if __name__ == "__main__":
    main()
