from pathlib import Path

def file_read(path: str, max_bytes: int = 4000) -> str:
    p = Path(path).resolve()
    text = p.read_bytes()[:max_bytes]
    return text.decode("utf-8", errors="ignore")
