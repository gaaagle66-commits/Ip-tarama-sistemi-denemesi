from flask import Flask, render_template, request
from network_utils import tcp_scan, udp_scan, ping_test, packet_test

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    ip1 = request.form["ip1"]
    ip2 = request.form["ip2"]

    protocol = request.form["protocol"]
    port = int(request.form["port"])
    packet_count = int(request.form["packet_count"])
    byte_size = int(request.form["byte_size"])

    logs = []
    logs.append("=== TARANAN IP'LER ===")
    logs.append(f"1. IP → {ip1}")
    logs.append(f"2. IP → {ip2}\n")

    logs.append("=== PORT DURUMU ===")
    if protocol == "tcp":
        logs.append(tcp_scan(ip1, port))
        logs.append(tcp_scan(ip2, port))
    else:
        logs.append(udp_scan(ip1, port))
        logs.append(udp_scan(ip2, port))

    logs.append("\n=== PAKET TESTİ ===")
    logs.extend(packet_test(ip1, port, protocol, packet_count, byte_size))
    logs.extend(packet_test(ip2, port, protocol, packet_count, byte_size))

    logs.append("\n=== PING TESTİ ===")
    logs.append(f"IP1 PING:\n{ping_test(ip1)}")
    logs.append(f"IP2 PING:\n{ping_test(ip2)}")

    return render_template("result.html", logs=logs)


if __name__ == "__main__":
    print("Flask başlatılıyor...")
    app.run(host="0.0.0.0", port=5000, debug=True)
