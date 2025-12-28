from __future__ import annotations

import os
from typing import Optional

import httpx


class LLMClient:
    """Thin wrapper around a local Ollama instance.

    If the Ollama host or model is unavailable, calls gracefully return `None`
    instead of raising, so the rest of the tool keeps working.
    """

    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        # self.base_url = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
        self.model = os.getenv("LLM_MODEL", "llama3.1:8b")
        
        async def summarize(self, prompt: str) -> Optional[str]:
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        f"{self.base_url}/api/generate",
                        json={"model": self.model, "prompt": prompt, "stream": False},
                    )
                    print("OLLAMA STATUS:", resp.status_code)
                    print("OLLAMA BODY:", resp.text)
                    resp.raise_for_status()
                    data = resp.json()
                    return data.get("response")
            except httpx.RequestError as e:
                print("OLLAMA REQUEST ERROR:", e)
                return None
            except Exception as e:
                print("OLLAMA GENERIC ERROR:", e)
                return None

    async def summarize01(self, prompt: str) -> str:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
            )
            
        except httpx.RequestError as e:
            print("OLLAMA REQUEST ERROR:", e)
            raise

        print("OLLAMA STATUS:", resp.status_code)
        print("OLLAMA BODY:", resp.text)
        resp.raise_for_status()

        data = resp.json()
        response = data.get("response")
        if not response or not isinstance(response, str):
            raise ValueError("Ollama returned no 'response' text")

        return response

    async def summarize26(self, prompt: str) -> Optional[str]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
            )
        print("OLLAMA STATUS:", resp.status_code)
        print("OLLAMA BODY:", resp.text)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response")
    except httpx.RequestError as e:
        print("OLLAMA REQUEST ERROR:", e)
        return None
    except Exception as e:
        print("OLLAMA GENERIC ERROR:", e)
        return None
        

    async def summarize27(self, prompt: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False},
                )
            resp.raise_for_status()
            data = resp.json()
            return data.get("response")
        except httpx.RequestError:
            # Ollama not reachable -> fail fast, but don’t break API
            return None
        except Exception:
            return None
          
