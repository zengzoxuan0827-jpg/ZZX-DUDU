from pathlib import Path
import json
import base64

root = Path(__file__).resolve().parents[1]
html = (root / "dist" / "index.html").read_text(encoding="utf-8")
asset_paths = [
    path
    for folder in [
        root / "dist" / "assets" / "baby-moods",
        root / "dist" / "assets" / "clean-ingredients",
        root / "dist" / "assets" / "clean-rice-amount",
        root / "dist" / "assets" / "clean-icons",
    ]
    for path in folder.glob("*.png")
]
assets = {
    "/" + path.relative_to(root / "dist").as_posix(): {
        "type": "image/png",
        "body": base64.b64encode(path.read_bytes()).decode("ascii"),
    }
    for path in asset_paths
}

worker = f"""const INDEX_HTML = {json.dumps(html, ensure_ascii=False)};
const ASSETS = {json.dumps(assets)};

function decodeBase64(value) {{
  const binary = atob(value);
  const bytes = new Uint8Array(binary.length);
  for (let index = 0; index < binary.length; index += 1) bytes[index] = binary.charCodeAt(index);
  return bytes;
}}

export default {{
  async fetch(request, env) {{
    const url = new URL(request.url);
    if (url.pathname === "/" || url.pathname === "/index.html") {{
      return new Response(INDEX_HTML, {{ headers: {{ "content-type": "text/html; charset=utf-8" }} }});
    }}
    const asset = ASSETS[url.pathname];
    if (asset) {{
      return new Response(decodeBase64(asset.body), {{ headers: {{ "content-type": asset.type, "cache-control": "public, max-age=31536000" }} }});
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
