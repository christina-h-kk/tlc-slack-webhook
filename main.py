from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

# Get the Slack webhook URL from environment variable
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

@app.post("/github")
async def github_webhook(request: Request):
    payload = await request.json()
    pr = payload.get("pull_request")
    
    if payload.get("action") == "closed" and pr and pr.get("merged"):
        msg = {
            "text": f":tada: PR merged: *{pr['title']}* by `{pr['user']['login']}`\n<{pr['html_url']}>"
        }

        async with httpx.AsyncClient() as client:
            await client.post(SLACK_WEBHOOK_URL, json=msg)

    return {"ok": True}
