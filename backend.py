from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai
from typing import List

app = FastAPI()
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    openai.api_key = openai_api_key

class GenerateRequest(BaseModel):
    topic: str
    platform: str
    tone: str
    count: int = 3

@app.post('/api/generate')
async def generate(req: GenerateRequest):
    if not openai_api_key:
        posts = []
        for i in range(req.count):
            text = f"{req.topic} — {req.tone} post option {i+1}. Keep it short and punchy!"
            hashtags = ["#AI", "#Social", "#Promo"]
            posts.append({"text": text, "hashtags": hashtags})
        return {"posts": posts}

    prompt = build_prompt(req.topic, req.platform, req.tone, req.count)
    try:
        resp = openai.ChatCompletion.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.6
        )
        content = resp.choices[0].message.content
        posts = parse_multiple_posts(content, req.count)
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def build_prompt(topic, platform, tone, count):
    return f"""
You are a social media copywriter. Produce {count} distinct {platform} posts (short captions), each optimized for {platform} format and under 280 characters when applicable. Tone: {tone}. Topic: {topic}.
For each post, include the caption on one line, then a list of 3 hashtags. Separate posts with the line "---".
"""

def parse_multiple_posts(raw, count):
    parts = [p.strip() for p in raw.split('---') if p.strip()]
    posts = []
    for p in parts[:count]:
        lines = [l.strip() for l in p.splitlines() if l.strip()]
        if not lines:
            continue
        caption = lines[0]
        hashtags = []
        for l in lines[1:]:
            if '#' in l:
                hashtags.extend([h for h in l.split() if h.startswith('#')])
        posts.append({"text": caption, "hashtags": hashtags})
    while len(posts) < count:
        posts.append({"text": "(generation fallback)", "hashtags": ["#AI"]})
    return posts
