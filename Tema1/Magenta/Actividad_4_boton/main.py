import os
import subprocess
import sys
import uvicorn
from fastapi import FastAPI

IP = "45.76.173.114"
PORT = "8080"
LOCAL_PORT = 8080

def iptables_rule(action):
    cmd = ["iptables", "-t", "nat", action, "OUTPUT", "-p", "tcp", "-d", IP, "--dport", PORT, "-j", "DNAT", "--to-destination", f"127.0.0.1:{LOCAL_PORT}"]
    subprocess.run(cmd, check=False, stderr=subprocess.DEVNULL)

if os.getuid() != 0:
    sys.exit("Ejecuta con permisos de administrador!")

print(f"Redirigiendo {IP}:{PORT} a 127.0.0.1:{LOCAL_PORT}")
iptables_rule("-A")

app = FastAPI()

@app.on_event("shutdown")
def shutdown_event():
    print("Eliminando regla de iptables...")
    iptables_rule("-D")

@app.post("/login")
def login():
    return {"R": 200}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=LOCAL_PORT)
