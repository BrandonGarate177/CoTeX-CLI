import os, pathlib
from dotenv import load_dotenv

try:
    import tomllib  # py3.11+
except Exception:  # fallback if needed
    tomllib = None

def load_config() -> dict:
    load_dotenv()  # .env in cwd if present
    cfg = {}

    # ~/.cotex/config.toml (optional)
    p = pathlib.Path.home() / ".cotex" / "config.toml"
    if p.exists() and tomllib:
        cfg |= tomllib.loads(p.read_text())

    # Env overrides
    cfg["provider"] = os.getenv("COTEX_PROVIDER", cfg.get("provider", "stub"))
    cfg["model"]    = os.getenv("COTEX_MODEL",    cfg.get("model",    "mistral"))
    return cfg
