FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y git && pip install --no-cache-dir -r requirements.txt

COPY blogger_mcp.py .
COPY credentials.json .

# Set environment variables for OAuth and your blog ID.
# You will replace YOUR_RENDER_URL and YOUR_BLOG_ID later.
ENV OAUTH_REDIRECT="https://YOUR_RENDER_URL/oauth2callback"
ENV BLOG_ID="YOUR_BLOG_ID"

EXPOSE 8000
CMD ["uvicorn", "blogger_mcp:app", "--host", "0.0.0.0", "--port", "8000"]
