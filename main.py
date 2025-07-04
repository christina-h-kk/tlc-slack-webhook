from fastapi import FastAPI, Request
import httpx, os

app = FastAPI()

SLACK_WEBHOOK_URL = os.environ["https://api.slack.com/apps/A094ARD09DG"]

@app.post("/github")
async def github_webhook(request: Request):
    payload = await request.json()
    pr = payload.get("pull_request")
    if payload.get("action") == "closed" and pr and pr.get("merged"):
        msg = {
            "text": f":tada: PR merged: *{pr['title']}* by `{pr['user']['login']}`\n<{pr['html_url']}>"
        }
        await httpx.post(SLACK_WEBHOOK_URL, json=msg)
    return {"ok": True}
