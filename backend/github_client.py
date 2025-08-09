import time, jwt, httpx, hashlib, hmac
from typing import Dict, Any, Optional, List
from config import settings

GITHUB_API = "https://api.github.com"

def verify_signature(secret: str, raw_body: bytes, signature_header: str) -> bool:
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    digest = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={digest}", signature_header)

def _app_jwt() -> str:
    now = int(time.time())
    payload = {"iat": now - 60, "exp": now + 9 * 60, "iss": settings.github_app_id}
    return jwt.encode(payload, settings.github_private_key_pem, algorithm="RS256")

async def _installation_token(installation_id: int) -> str:
    jwt_token = _app_jwt()
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{GITHUB_API}/app/installations/{installation_id}/access_tokens",
            headers={"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github+json"},
        )
        r.raise_for_status()
        return r.json()["token"]

async def list_changed_files(owner: str, repo: str, pr_number: int, token: str) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        files = []
        page = 1
        while True:
            r = await client.get(
                f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files",
                headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
                params={"per_page": 100, "page": page},
            )
            r.raise_for_status()
            batch = r.json()
            files.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        return files

async def get_repo_file(owner: str, repo: str, path: str, token: str) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            headers={"Authorization": f"token {token}", "Accept": "application/vnd.github.raw+json"},
        )
        if r.status_code == 200:
            return r.text
        return None

async def list_issue_comments(owner: str, repo: str, pr_number: int, token: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues/{pr_number}/comments",
            headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
            params={"per_page": 100},
        )
        r.raise_for_status()
        return r.json()

async def create_or_update_comment(owner: str, repo: str, pr_number: int, token: str, body: str, marker: str):
    # Try to update an existing bot comment to avoid spam
    comments = await list_issue_comments(owner, repo, pr_number, token)
    target = next((c for c in comments if marker in c.get("body", "")), None)

    async with httpx.AsyncClient() as client:
        if target:
            r = await client.patch(
                f"{GITHUB_API}/repos/{owner}/{repo}/issues/comments/{target['id']}",
                headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
                json={"body": body},
            )
        else:
            r = await client.post(
                f"{GITHUB_API}/repos/{owner}/{repo}/issues/{pr_number}/comments",
                headers={"Authorization": f"token {token}", "Accept": "application/vnd.github+json"},
                json={"body": body},
            )
        r.raise_for_status()

    return True
