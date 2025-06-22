from fast_mcp import FastMCP
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import json

def get_blogger_service():
    creds_path = 'credentials.json'
    token_path = 'token.json'
    flow = Flow.from_client_secrets_file(
        creds_path,
        scopes=['https://www.googleapis.com/auth/blogger.readonly'],
        redirect_uri=os.environ.get('OAUTH_REDIRECT')
    )
    creds = None
    if os.path.exists(token_path):
        with open(token_path) as f:
            info = json.load(f)
        creds = flow.credentials.from_authorized_user_info(info)
    else:
        auth_url, _ = flow.authorization_url(prompt='consent')
        print('Go to this URL to authorize:', auth_url)
        code = input('Enter the authorization code: ')
        flow.fetch_token(code=code)
        creds = flow.credentials
        with open(token_path, 'w') as f:
            f.write(creds.to_json())
    return build('blogger', 'v3', credentials=creds)

def create_server():
    mcp = FastMCP(
        name="Blogger MCP",
        instructions=(
            "Use search(query) to find blog posts by keyword. "
            "Use fetch(id) to retrieve full post text and metadata."
        )
    )
    service = get_blogger_service()
    blog_id = os.environ.get('BLOG_ID')

    @mcp.tool()
    async def search(query: str):
        resp = service.posts().list(blogId=blog_id, q=query, maxResults=50).execute()
        results = []
        for post in resp.get('items', []):
            results.append({
                'id': post['id'],
                'title': post['title'],
                'text': post.get('content', '')[:200],
                'url': post.get('url')
            })
        return {'results': results}

    @mcp.tool()
    async def fetch(id: str):
        post = service.posts().get(blogId=blog_id, postId=id).execute()
        return {
            'id': post['id'],
            'title': post['title'],
            'text': post.get('content', ''),
            'url': post.get('url'),
            'metadata': {
                'published': post.get('published'),
                'updated': post.get('updated'),
                'author': post.get('author', {}).get('displayName')
            }
        }

    return mcp

app = create_server()

if __name__ == '__main__':
    from uvicorn import run
    run('blogger_mcp:app', host='0.0.0.0', port=8000)
