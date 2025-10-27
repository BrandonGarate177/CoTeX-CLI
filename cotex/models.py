from pydantic import BaseModel
import os, requests

class ModelManager(BaseModel):
    provider: str = "stub"  # "ollama" | "openai" | "anthropic" later
    model: str = "mistral"

    @classmethod
    def from_config(cls, cfg):
        return cls(provider=cfg.get("provider", "stub"),
                   model=cfg.get("model", "mistral"))

    def complete(self, prompt: str, stream: bool=False) -> str:
        # Ollama local API or OpenAI API calls
        if self.provider == "ollama":
            r = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=120
            )
            r.raise_for_status()
            return r.json().get("response","")
        elif self.provider == "openai":
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY missing")
            # Minimal call; you’ll upgrade in Phase 2
            import requests as rq
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key}"}
            body = {"model": self.model, "messages":[{"role":"user","content":prompt}]}
            resp = rq.post(url, headers=headers, json=body, timeout=120)
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        else:
            raise RuntimeError("No model configured (provider=stub).")
