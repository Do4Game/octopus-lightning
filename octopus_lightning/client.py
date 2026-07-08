import requests
from typing import Optional, Any

class LightningClient:
    """
    Client for Octopus Lightning (SaaS API)
    High-performance In-Memory Cache for AI Agents.
    """
    def __init__(self, api_key: str, base_url: str = "https://api.octopusclass.pl/v1/lightning"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> bool:
        """Stores a value in the memory cache."""
        payload = {"value": value, "ttl_seconds": ttl_seconds}
        try:
            response = requests.post(f"{self.base_url}/{key}", json=payload, headers=self.headers)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print("[Lightning] Error: Rate Limit Exceeded (429). Upgrade your SaaS plan.")
            elif response.status_code == 401:
                print("[Lightning] Error: Unauthorized (401). Invalid API Key.")
            else:
                print(f"[Lightning] HTTP Error: {e}")
            return False
        except Exception as e:
            print(f"[Lightning] Network Error: {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """Retrieves a value from the memory cache."""
        try:
            response = requests.get(f"{self.base_url}/{key}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("value")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return None
            print(f"[Lightning] HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"[Lightning] Network Error: {e}")
            return None

    def delete(self, key: str) -> bool:
        """Deletes a value from the memory cache."""
        try:
            response = requests.delete(f"{self.base_url}/{key}", headers=self.headers)
            response.raise_for_status()
            return True
        except Exception:
            return False
