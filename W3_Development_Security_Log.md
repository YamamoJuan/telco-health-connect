# W3_Development_Security_Log.md

# System Development Log (Cloud Native)

## Dockerfile and Base Image Choice

- **Base Image**: `python:3.12-slim`
- **Multi-stage Build**: Used for production image size optimization
- **Non-root User**: Application runs as UID 1001
- **Exposed Port**: 8000 (standard FastAPI port)

## Simulated Payment Integration Flow

1. **GET /health** - Health check endpoint
2. **POST /payments** - Accept payment request with transaction ID and amount
3. **POST /webhooks/payment** - Receive payment status notifications with HMAC verification

## Local vs Container Environment Consistency

- **Local**: Direct file access, easier debugging
- **Container**: Multi-stage build ensures consistent environment
- **Configuration**: Environment variables via `.env` (ignored by Git)

## Security Audit & Remediation

### Tools Used
- **Bandit**: Static Application Security Testing (SAST)
- **pip-audit**: Software Composition Analysis (SCA)

### Initial Findings

- **Bandit**: 1 Medium, 1 Low severity finding
- **pip-audit**: 28 known vulnerabilities in declared dependencies

### Remediation

- Input validation implemented via Pydantic models
- HMAC-SHA256 signature verification with constant-time comparison
- Secrets managed via environment variables (not hardcoded)
- Docker multi-stage build prevents secret leakage

### Remaining Risks

- Authentication: HTTP Basic (development only, needs OAuth2 for production)
- No rate limiting
- In-memory transaction storage (not persistent)
- No HTTPS/TLS in development mode

### Commands to Verify Project

```bash
# Build Docker image
docker build -t telco-health-connect .

# Run container (example)
docker run -p 8000:8000 -e WEBHOOK_SECRET=mysecret telco-health-connect

# Run tests
pytest tests/ -v

# Run security scans
bandit -r app/ -f txt -o evidence/bandit_initial.txt
pip-audit -r requirements.txt -f txt -o evidence/pip_audit_initial.txt