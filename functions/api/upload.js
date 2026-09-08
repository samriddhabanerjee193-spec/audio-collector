export async function onRequestPost(context) {
  try {
    const { request, env } = context;

    // 1. Get audio binary stream from request body
    const audioData = await request.arrayBuffer();
    if (!audioData || audioData.byteLength === 0) {
      return new Response("Empty file payload", { status: 400 });
    }

    // 2. Read word label header (defaults to "unknown")
    const wordLabel = (request.headers.get("X-Word-Label") || "unknown")
      .toLowerCase()
      .replace(/[^a-z0-9]/g, "");

    // 3. Generate structured filename: label_timestamp_random.webm
    const timestamp = Date.now();
    const randomId = Math.random().toString(36).substring(2, 8);
    const fileName = `${wordLabel}_${timestamp}_${randomId}.webm`;

    // 4. Save directly to R2 bucket using binding (NO AWS SDKs or API Keys!)
    // "AUDIO_BUCKET" is the R2 binding variable name configured in Cloudflare
    await env.AUDIO_BUCKET.put(fileName, audioData, {
      httpMetadata: {
        contentType: request.headers.get("Content-Type") || "audio/webm",
      },
      customMetadata: {
        label: wordLabel,
        uploadedAt: new Date().toISOString(),
      },
    });

    return new Response(JSON.stringify({ success: true, key: fileName }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(`Upload Error: ${err.message}`, { status: 500 });
  }
}