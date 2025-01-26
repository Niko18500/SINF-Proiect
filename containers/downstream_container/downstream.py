import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Log the ip and mac address for each received request
class LoggingHTTPRequestHandler(SimpleHTTPRequestHandler):
    def get_mac_address(self, ip):
        try:
            result = os.popen(f"arp -n {ip}").read()
            for line in result.splitlines():
                if ip in line:
                    parts = line.split()
                    if len(parts) > 3:
                        return parts[3]
        except Exception as e:
            return None
        return None

    def do_GET(self):
        ip = self.client_address[0]
        mac = self.get_mac_address(ip)
        
        print(f"Received request from IP: {ip}, MAC: {mac if mac else 'MAC not found'}", flush=True)
        super().do_GET()

if __name__ == "__main__":
    server_address = ("", 8080)
    server = HTTPServer(server_address, LoggingHTTPRequestHandler)
    
    print("Serving on port 8080...", flush=True)
    server.serve_forever()
