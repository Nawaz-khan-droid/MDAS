# Security Policy

## Supported Versions

Only the latest published version is currently supported.

## Reporting a Vulnerability

Please do not publicly disclose security vulnerabilities.
Report them privately through GitHub Security Advisories or repository contact.

## Security Audit Results

The following claims are verified against the actual codebase (commit `88d57096`).

### API Input Validation

| Control | Implementation | Verified |
|---------|---------------|----------|
| Max input length | Pydantic `max_length=5000` in `AnalysisRequest` schema (`schemas.py:93`) | Yes |
| Empty input rejected | `min_length=1` in schema + explicit `.strip()` check in handler (`main.py:71`) | Yes |
| Malformed JSON | FastAPI returns 422 automatically; custom handler maps to 400 (`main.py:37-51`) | Yes |
| Oversized payloads | Pydantic `string_too_long` error mapped to HTTP 413 (`main.py:42-46`) | Yes |
| Unsupported language | Returns 400 with clean message, no internal details (`main.py:76-77`) | Yes |

### Error Handling

| Control | Implementation | Verified |
|---------|---------------|----------|
| No stack traces to clients | `traceback.print_exc()` goes to server logs only; client receives generic message (`main.py:84-85`) | Yes |
| No filesystem paths in responses | Error messages are static strings, no `str(e)` with path info | Yes |
| Consistent status codes | 400 (validation), 413 (oversized), 503 (not ready), 500 (internal) | Yes |

### FastAPI Configuration

| Control | Implementation | Verified |
|---------|---------------|----------|
| Default docs disabled | `docs_url=None, redoc_url=None, openapi_url=None` (`main.py:30-32`) | Yes |
| No debug mode in production | `reload=True` only in `if __name__ == "__main__"` block, not in uvicorn start command | Yes |
| Models loaded once at startup | `AnalysisService` initialized in `lifespan()`, shared across requests | Yes |
| No CORS middleware | Same-origin only; HTMX UI and API on same origin | Yes (intentional) |

### Frontend Security

| Control | Implementation | Verified |
|---------|---------------|----------|
| Jinja2 autoescaping | `Jinja2Blocks` inherits default `autoescape=True` for `.html` templates | Yes |
| No `|safe` filter | Grep confirms no `|safe` usage in any template | Yes |
| No `innerHTML` | Grep confirms no `innerHTML` or `dangerouslySetInnerHTML` in templates | Yes |
| User text in templates | `{{ text|default('') }}` — autoescaped by Jinja2 | Yes |
| HTMX targets | Static template blocks, no user-controlled target URLs | Yes |

### Resource Protection

| Control | Implementation | Verified |
|---------|---------------|----------|
| Input size bounded | 5,000 character hard limit | Yes |
| No file upload | Text-only API, no file handling | Yes |
| No shell commands | No `subprocess`, `os.system`, or `eval` from user input | Yes |
| No arbitrary code execution | No `exec`, `eval`, or dynamic code from user input | Yes |
| No user-supplied filesystem paths | Models loaded from fixed `models/` directory | Yes |
| spaCy parser bounded | Input limit prevents unbounded parse trees | Yes |

### Repository Hygiene

| Control | Verified |
|---------|----------|
| No `.env` files committed | Yes |
| No API keys, tokens, passwords | Yes |
| No `.venv/` tracked | Yes (removed, in `.gitignore`) |
| No `__pycache__/` tracked | Yes (removed, in `.gitignore`) |
| No local Windows paths in code | Yes |
| No scratch/artifact files | Yes (removed) |

## Known Limitations

- **No authentication**: The MVP API is unauthenticated. Anyone who discovers the endpoint can call it. The 5,000-character limit bounds per-request resource usage but does not prevent high request volume.
- **No rate limiting**: Not implemented for MVP. Deploy behind a reverse proxy or CDN with rate limiting for production use.
- **No HTTPS enforcement**: Render provides HTTPS at the edge. The application itself does not enforce HSTS.
- **English only**: Non-English text is rejected with HTTP 400.

## Third-Party Components

MDAS depends on third-party libraries and NLP models. Their respective licenses and security advisories apply. Key dependencies: FastAPI, spaCy, scikit-learn, langdetect.

## Disclosure

Report vulnerabilities privately. Do not open public issues for security reports.
