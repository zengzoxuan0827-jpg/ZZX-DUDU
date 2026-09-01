from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
html = (root / "dist" / "index.html").read_text(encoding="utf-8")
worker = f"""const INDEX_HTML = {json.dumps(html, ensure_ascii=False)};

export default {{
  async fetch(request, env) {{
    const url = new URL(request.url);
    if (url.pathname === "/" || url.pathname === "/index.html") {{
      return new Response(INDEX_HTML, {{ headers: {{ "content-type": "text/html; charset=utf-8" }} }});
    }}
    if (env.ASSETS) {{
      const response = await env.ASSETS.fetch(request);
      if (response.status !== 404) return response;
    }}
    return new Response("Not found", {{ status: 404 }});
  }}
}};
"""
(root / "dist" / "server" / "index.js").write_text(worker, encoding="utf-8")
