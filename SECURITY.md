# Security Policy

## Supported Versions

We actively support the following versions of LegacyEvolve Protocol (LEP) with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

**We take security seriously.** If you discover a security vulnerability in LegacyEvolve or MACP, please report it responsibly.

### How to Report

1. **Do NOT open a public GitHub issue** for security vulnerabilities
2. **Email us directly** at: [creator35lwb@gmail.com](mailto:creator35lwb@gmail.com)
3. **Use GitHub Security Advisories** (preferred): [Report a vulnerability](https://github.com/creator35lwb-web/LegacyEvolve/security/advisories/new)

### What to Include

Please provide as much information as possible:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** (e.g., data exposure, privilege escalation)
- **Affected versions** (if known)
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up

### Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial assessment:** Within 7 days
- **Fix timeline:** Depends on severity
  - **Critical:** 1-7 days
  - **High:** 7-30 days
  - **Medium:** 30-90 days
  - **Low:** 90+ days or next release

### Disclosure Policy

- We follow **coordinated disclosure** principles
- We will work with you to understand and fix the issue
- We will credit you in the security advisory (unless you prefer to remain anonymous)
- We will publish a security advisory once a fix is available
- Please allow us **90 days** to fix the issue before public disclosure

### Security Updates

- Security fixes are released as **patch versions** (e.g., 2.1.1)
- Critical security updates may be backported to older supported versions
- We will publish a **GitHub Security Advisory** for all security issues
- We will update this SECURITY.md file with known vulnerabilities

### Security Best Practices

When using LegacyEvolve Protocol:

1. **Keep dependencies updated** - Use Dependabot or similar tools
2. **Use virtual environments** - Isolate LEP from other Python packages
3. **Validate inputs** - Never trust data from legacy systems without validation
4. **Use TLS 1.3+** - Ensure secure communication between AI agents and legacy systems
5. **Audit adapter code** - Review custom adapters for security issues
6. **Follow least privilege** - Grant minimal permissions to LEP processes
7. **Monitor logs** - Watch for suspicious activity in LEP logs

### Known Vulnerabilities

**None currently reported.**

We will update this section if vulnerabilities are discovered.

### Security Scanning

We use the following tools to scan for vulnerabilities:

- **Dependabot** - Dependency vulnerability scanning
- **CodeQL** - Semantic code analysis
- **Bandit** - Python security linting
- **Safety** - Python dependency security checks

All scans run automatically on every push and pull request.

### Security Contact

- **Email:** creator35lwb@gmail.com
- **GitHub Security Advisories:** [Report a vulnerability](https://github.com/creator35lwb-web/LegacyEvolve/security/advisories/new)
- **Project Lead:** Alton Lee (creator35lwb-web)
- **CTO:** L (GODEL) - AI Agent

### Acknowledgments

We thank the following security researchers for responsibly disclosing vulnerabilities:

*(None yet - be the first!)*

---

**Thank you for helping keep LegacyEvolve and MACP secure!**

*This security policy is part of our commitment to building a safe and trustworthy Digital Public Good.*
