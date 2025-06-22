# Blogger MCP Server

This repo hosts a custom MCP server for your Blogger.com blog, deployed automatically to Render.com via GitHub Actions.

## ⚙️ Setup

1. **Fork or import** this repo into your GitHub account.
2. In **Settings → Secrets and variables → Actions**, add:
   - `RENDER_SERVICE_ID` — your Render service ID
   - `RENDER_API_KEY` — an API key from Render (with deploy rights)
3. Open **Dockerfile** and replace:
   - `YOUR_RENDER_URL` with your actual Render service URL
   - `YOUR_BLOG_ID` with your Blogger blog ID
4. Commit and push to `main`. GitHub Actions will build and deploy automatically.

## 🔗 Connecting to ChatGPT

1. In ChatGPT **Settings → Connectors**, click **Add custom connector**.
2. Enter your Render URL, e.g. `https://your-service.onrender.com`.
3. Fill in OAuth details:
   - **Auth URL**: `https://accounts.google.com/o/oauth2/auth`
   - **Token URL**: `https://oauth2.googleapis.com/token`
   - **Client ID/Secret** from your Google Cloud Console
   - **Redirect URI**: `https://your-service.onrender.com/oauth2callback`
4. Save and test with:
