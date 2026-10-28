# Security Policy

## Security Scope

This project is a simulated payment integration service intended for educational purposes. The security features implemented are representative patterns for learning and demonstration.

### What is NOT in scope:
- No real payment processing
- No database storage of sensitive data
- No network-level security controls
- No PCI-DSS compliance (simulated service)

### What IS covered:
- Input validation and sanitization
- HMAC signature verification for webhooks
- Environment-based secret management
- Secure Docker configuration
- Dependency vulnerability scanning

## Known Limitations

1. **Simulated Gateway**: This service simulates payment processing. No real money transactions occur.
2. **Development Secrets**: Default secrets are provided for testing only. Always change in production.
3. **No Rate Limiting**: The prototype lacks rate limiting controls.
4. **No Audit Logging**: Production systems should log all payment events.
5. **In-Memory Storage**: Transaction state is not persisted.

## Reporting Security Issues

Since this is an educational prototype without a live deployment:

1. Review the code in this repository
2. Any security concerns should be documented in project logs
3. Use Bandit and pip-audit for code scanning

## Security Measures Implemented

### Input Validation
- Transaction ID validated with regex pattern
- Amount validated for range (0 < amount <= 100,000,000 IDR)
- Request body parsed safely with exception handling

### Webhook Security
- HMAC-SHA256 signature verification
- Constant-time comparison to prevent timing attacks
- Signature format: `sha256=<hex_digest>`

### Secrets Management
- Secrets loaded from environment variables
- `.env` files excluded from version control
- No hardcoded secrets in source code

### Container Security
- Non-root user execution
- Multi-stage build reducing attack surface
- Minimal base image (python:3.12-slim)

## Security Scan Commands

```bash
# Run SAST scan
bandit -r app/ -f txt -o evidence/bandit_initial.txt

# Run dependency vulnerability scan
pip-audit -r requirements.txt -f txt -o evidence/pip_audit_initial.txt
```

## Security Best Practices Followed

1. Principle of least privilege (non-root Docker user)
2. Explicit timeouts for HTTP operations
3. No sensitive data in logs
4. Secure secret handling
5. Dependency version pinning