import os, json
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import settings
import github_client as gh
from reviewer import parse_repo_rules, review_changed_files, render_markdown

app = FastAPI(title="AI Code Review Bot", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Code Review Bot is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"ok": True, "service": "ai-code-review-bot"}

@app.post("/webhook")
async def webhook(
    request: Request,
    x_github_event: str = Header(None, convert_underscores=False),
    x_hub_signature_256: str = Header(None, convert_underscores=False),
):
    try:
        raw = await request.body()
        if not gh.verify_signature(settings.github_webhook_secret, raw, x_hub_signature_256):
            raise HTTPException(status_code=401, detail="Invalid signature")

        payload = await request.json()
        # Only react to PR lifecycle events
        if x_github_event != "pull_request":
            return JSONResponse({"ignored": True, "event": x_github_event})

        action = payload.get("action")
        if action not in {"opened", "reopened", "synchronize"}:
            return JSONResponse({"ignored_action": action})

        installation_id = payload["installation"]["id"]
        token = await gh._installation_token(installation_id)

        pr = payload["pull_request"]
        owner = payload["repository"]["owner"]["login"]
        repo = payload["repository"]["name"]
        pr_number = pr["number"]

        # Optional repo rules
        cfg = await gh.get_repo_file(owner, repo, ".aicodereview.yml", token)
        rules = parse_repo_rules(cfg)

        changed = await gh.list_changed_files(owner, repo, pr_number, token)
        result = await review_changed_files(owner, repo, pr_number, changed, rules)
        body = render_markdown(result, settings.bot_comment_tag)

        await gh.create_or_update_comment(owner, repo, pr_number, token, body, settings.bot_comment_tag)
        return {"status": "review-posted", "pr": pr_number, "files_reviewed": len(changed)}
    
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
