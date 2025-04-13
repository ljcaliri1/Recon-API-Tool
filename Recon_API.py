from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import subprocess
import nmap
import os
import json
from datetime import datetime


app = FastAPI()

# Add Health check endpoint
@app.get("/healthcheck")
def healthcheck():
    return {
        "status": "online",
        "version": "1.0",
        "timestamp": datetime.utcnow().isoformat()
    }
         

# Define the input model for scan options

class ScanOptions(BaseModel):
    host: str                    # IP address or domain to scan
    aggressive: bool = False     # Use -A for full aggressive scan
    os_detection: bool = False   # Use -O for OS detection
    ports: str | None = None     # Port range (e.g, "1-1000", "80-443")

# Main endpoint to perform a scan

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pentest API"}
@app.post("/scan/")
def scan_target(options: ScanOptions):
    try:
        # Build the Nmap command based on user input
        cmd = ["nmap", "-sV"] #Basic version detection
        
        if options.aggressive:
            cmd.append("-A")
        if options.os_detection:
            cmd.append("-O")
        if options.ports:
            cmd.extend(["-P", options.ports])
            
        cmd.append(options.host)
        # Run the Scan
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        output = result.stdout
        #save output to a timestamped file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_{options.host.replace('.', '_')}_{timestamp}.txt"
        output_dir = "scan_reports"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w") as f:
            f.write(output)
            
         # Return scan preview and report path
        return JSONResponse(content={
            "message": "Scan complete",
            "output_preview": output[:500],  #Limit preview lenght
            "report_file": filepath
        })
    
    except Exception as e:
        # Catch any return errors
        return JSONResponse(content={"error": str(e)}, status_code=500)
