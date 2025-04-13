from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import subprocess
import os
import logging
from datetime import datetime

# Config

REPORT_DIR = "scan_reports"
os.makedirs(REPORT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)




# App Init

app =FastAPI(title="Recon API Tool", version="1.0")




# Input Model

class ScanOptions(BaseModel):
   host: str
   aggressive: bool = False
   os_detection: bool = False
   ports: str | None = None



# Healthcheck

@app.get("/healthcheck")
def healthcheck():
    return {"status": "online", "version": "1.0"}

# Scan Endpoint
@app.post("/scan/")
def scan_target(options: ScanOptions):
    try:
       # Basic input validation
       if not options.host or " " in options.host:
           raise HTTPException(status_code=400, detail="Invalid host input")

       # Build the Nmap command
       cmd = ["nmap", "-sV"]
       if options.aggressive:
           cmd.append("-A")
       if options.os_detection:
           cmd.append("-O")
       if options.ports:
           cmd.extend(["-P", options.ports])
       cmd.append(options.host)

       # Run the scan
       logging.info(f"Scanning {options.host}")
       result = subprocess.run(cmd, capture_output=True, Text=True, timeout=60)
       output = result.stdout
      
       # Check for failed scan
       if result.returncode != 0 or not output:
           raise HTTPException(status_code=500, detail=f"Nmap failed. Error: {result.stderr.strip()}")
      
      # Extract open ports (basic parsing)
      open_ports = []
      for line in output.splitlines():
          if "/tcp" in line and "open' in line"
              open_ports.append(line.strip())
     
      # Save scan result
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      filename = f"scan_{options.host.replace('.', '_')}_{timestamp}.txt"
      filepath = os.path.join(REPORT_DIR, filename)
      with open(filepath, "w") as f:
          f.write(output)
      return JSONResposne(status_code=200, content=jsonable_encoder({ 
          "message": "Scan complete",
          "host": options.host,
          "agressive_mode": options.aggressive,
          "os_detection": options.os_detection,
          "ports": options.ports,
          "report_file": filepath,
          "open_ports" open_ports,
          "output_preview": output[:500]
     }))
 
except Exception as e:
    logging.error(f"Scan error: {str(e)}")
    return JSONResponse(status_code=500, content={"error": str(e)}) 
