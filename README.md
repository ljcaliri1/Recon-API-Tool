# Recon API Tool

The Recon API Tool is a FastAPI-based application designed to assist penetration testers, red teamers, and cybersecurity enthusiasts in performing reconnaissance and enumeration tasks through a lightweight and modular REST API. It provides customizable endpoints for scanning, data gathering, and target profiling in pre-engagement and post-exploitation phases.

## Features

- FastAPI-powered web interface with Swagger UI for interactive testing
- Domain and IP-based reconnaissance functionality
- Modular structure for easily adding new recon modules
- Clean JSON responses for integration into automation pipelines
- Designed for both beginner and advanced use in cybersecurity environments

---


## Setup

### Clone the repository
```bash
git clone https://github.com/ljcaliri1/Recon-API-Tool.git
cd Recon-API-Tool
```
### Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```

---


## Running the Tool
```bash
uvicorn app.main:app --reload
```
Visit the Swagger UI to test API endpoints interactively:

```
http://127.0.0.1:8000/docs
```

---


## Project Structure

```

Recon-API-Tool/
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── api/
│   │   └── routes_scan.py     # Recon logic
│   └── models/
│       └── scan.py            # Pydantic schemas
├── requirements.txt
└── README.md
```

---


## Example Usage POST/scan/domain

### Request(JSON)
```json

{
  "target": "example.com",
  "scan_type": "subdomain"
}
```
### Rsponse:
```json
{
  "status": "success",
  "target": "example.com",
  "scan_type": "subdomain",
  "results": ["dev.example.com", "mail.example.com"]
}
```


---

## Roadmap
- Add Nmap port scanning module
- Integrate Shodan or VirusTotal APIs
- Add logging and file ouput support
- Create unit tests and validation logic


---

## Contributing 

Pull requests and issue reports are welcome.
Please fork the repository to submit your changes
through a feature branch.

---


## License 

This project is licensed under the MIT License. 


---

## Disclaimer

This tool was created strictly for **educational purposes** and authorized **penetration testing** only.

**Unauthourized or malicious use is prohibited.**

The developer is **not responsible** for any misuse or damage caused by this tool.
