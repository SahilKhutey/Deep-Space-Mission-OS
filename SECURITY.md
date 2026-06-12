# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| v3.0.x | ✅ Yes |
| v2.0.x | ⚠️ Security fixes only |
| < v2.0 | ❌ No |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not open a public GitHub issue**.

Instead, report it privately via:
- **Email**: (maintainer contact via GitHub profile)
- **GitHub Private Security Advisory**: Use the "Report a vulnerability" button on the Security tab

We will acknowledge your report within 48 hours and aim to release a patch within 14 days for confirmed vulnerabilities.

## Security Best Practices for Deployment

- Run the server behind a reverse proxy (nginx/caddy) in production
- Do not expose the FastAPI `/docs` Swagger interface on public-facing deployments without authentication
- Validate all numeric inputs before passing to physics solvers (the API does this internally, but apply additional rate-limiting externally)
- Use HTTPS in any internet-facing deployment
