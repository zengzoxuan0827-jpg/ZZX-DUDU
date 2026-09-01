export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (env.ASSETS) {
      const response = await env.ASSETS.fetch(request);
      if (response.status !== 404) return response;
    }
    if (url.pathname === "/" || url.pathname === "/index.html") {
      return new Response("嘟嘟今天吃什么", {
        headers: { "content-type": "text/plain; charset=utf-8" }
      });
    }
    return new Response("Not found", { status: 404 });
  }
};
