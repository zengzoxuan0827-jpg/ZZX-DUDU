export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (env.ASSETS) {
      const assetUrl = new URL(request.url);
      if (assetUrl.pathname === "/") assetUrl.pathname = "/index.html";
      const response = await env.ASSETS.fetch(new Request(assetUrl, request));
      if (response.status !== 404) return response;
    }
    if (url.pathname === "/" || url.pathname === "/index.html") return Response.redirect(`${url.origin}/index.html`, 302);
    return new Response("Not found", { status: 404 });
  }
};
