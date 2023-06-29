from trpc.client import http_batch_link
from trpc.next import create_trpc_next
from server.routers._app import AppRouter
from typing import Optional

def get_base_url() -> str:
    """
    Returns the base URL based on the current environment.
    """
    if window_exists():
        # Browser should use relative path
        return ''

    if 'VERCEL_URL' in process.env:
        # Reference for vercel.com
        return f"https://{process.env['VERCEL_URL']}"

    if 'RENDER_INTERNAL_HOSTNAME' in process.env:
        # Reference for render.com
        return f"http://{process.env['RENDER_INTERNAL_HOSTNAME']}:{process.env['PORT']}"

    # Assume localhost
    return f"http://localhost:{process.env.get('PORT', 3000)}"


trpc = create_trpc_next[AppRouter]({
    'config': lambda ctx: {
        'links': [
            http_batch_link({
                # If you want to use SSR, you need to use the server's full URL
                # https://trpc.io/docs/ssr
                'url': f"{get_base_url()}/api/trpc",

                # You can pass any HTTP headers you wish here
                'headers': lambda: {
                    # 'authorization': get_auth_cookie(),
                },
            }),
        ],
    },
    # https://trpc.io/docs/ssr
    'ssr': False,
})

