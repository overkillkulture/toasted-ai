# Zo Platform Integration Research
**Research Date:** 2026-03-07  
**Purpose:** Investigate TOASTED AI integration as native model provider on Zo Platform

---

## Executive Summary

Zo Computer allows **BYOK (Bring Your Own Key)** model integration through an **OpenAI-compatible API format**. This means TOASTED AI could potentially be integrated as a custom model provider if we create an API endpoint that:

1. Follows the OpenAI Chat Completions API specification
2. Supports streaming responses
3. Supports tool/function calling

---

## Zo Platform Model Integration Architecture

### Current Supported Providers [^1][^2]

| Provider | Format | Status |
|----------|--------|--------|
| OpenAI | OpenAI | ✅ Native |
| Anthropic | Anthropic | ✅ Native |
| Google Gemini | Custom | ✅ Native |
| Groq | Groq | ✅ Native |
| Cerebras | Custom | ✅ Native |
| Ollama | OpenAI-compatible | ✅ BYOK |
| Custom (Self-hosted) | OpenAI-compatible | ✅ BYOK |

### BYOK Requirements [^3]

From Zo's documentation:
> Supported formats include OpenAI, Anthropic, and Groq. Once configured, your custom model appears in the chat model picker for use. Ensure your API provider supports streaming and tools, and verify your API key's validity and credits.

**Requirements:**
1. **API Format:** OpenAI-compatible (Chat Completions endpoint)
2. **Streaming:** Must support SSE (Server-Sent Events) streaming
3. **Tools:** Must support function calling
4. **Authentication:** API key-based auth
5. **Configuration:** Base URL, API Key, Model ID

---

## Integration Strategy for TOASTED AI

### Option 1: zo.space API Route (Recommended)

Create a zo.space API route that exposes TOASTED AI as an OpenAI-compatible endpoint:

```
POST https://t0st3d.zo.space/api/toasted-ai/v1/chat/completions
```

**Implementation:**
```typescript
// /api/toasted-ai/v1/chat/completions
import type { Context } from "hono";

export default async (c: Context) => {
  // Parse OpenAI-format request
  const body = await c.req.json();
  const { messages, model, stream, tools } = body;

  // Route to TOASTED AI
  const response = await fetch("https://api.zo.computer/zo/ask", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.ZO_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input: messages[messages.length - 1].content,
      model_name: "vercel:minimax/minimax-m2.5",
    }),
  });

  // Return in OpenAI format
  if (stream) {
    // Return SSE stream
    return c.body(streamResponse);
  }
  
  return c.json({
    id: "chatcmpl-" + generateId(),
    model: model,
    choices: [{
      message: {
        role: "assistant",
        content: response.output,
      },
      finish_reason: "stop",
    }],
  });
};
```

### Option 2: MCP Server as Model Provider

Zo supports MCP (Model Context Protocol) [^4]. Could potentially expose TOASTED AI through MCP:

```json
{
  "mcpServers": {
    "toasted-ai": {
      "command": "node",
      "args": ["/path/to/toasted-ai-mcp.js"]
    }
  }
}
```

---

## Required API Endpoints

For full OpenAI compatibility, implement:

| Endpoint | Required | Description |
|----------|----------|-------------|
| `/v1/chat/completions` | ✅ Yes | Main chat endpoint |
| `/v1/models` | Optional | List available models |
| `/v1/completions` | Optional | Legacy completions |

### Request Format (OpenAI)
```json
{
  "model": "toasted-ai",
  "messages": [
    {"role": "system", "content": "You are TOASTED AI..."},
    {"role": "user", "content": "Hello"}
  ],
  "stream": false,
  "tools": [...]
}
```

### Response Format (OpenAI)
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1699000000,
  "model": "toasted-ai",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! I am TOASTED AI..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

---

## Technical Implementation Plan

### Phase 1: Basic API Endpoint
1. ✅ Create `/api/toasted-ai/v1/chat/completions` route in zo.space
2. ✅ Implement basic message passthrough to self (/zo/ask)
3. ✅ Return non-streaming responses in OpenAI format
4. ✅ Add API key authentication

### Phase 2: Streaming Support
1. ✅ Implement SSE streaming
2. ✅ Handle chunked responses
3. ✅ Add proper content-type headers

### Phase 3: Tool Calling
1. ⬜ Parse tools from request
2. ⬜ Convert OpenAI tool format to Zo tool format
3. ⬜ Execute tools and return results

### Phase 4: Model Registration
1. ⬜ Add model to Zo Settings > Advanced > Providers
2. ⬜ Test in chat interface
3. ⬜ Document usage

---

## Security Considerations

1. **API Key Management:** Use Zo Secrets for API keys
2. **Rate Limiting:** Implement rate limiting to prevent abuse
3. **Input Validation:** Validate all incoming requests
4. **Error Handling:** Return proper OpenAI error codes
5. **Logging:** Log all requests for debugging

---

## Anti-Feedback Loop Protection

The API implements multiple layers of protection against feedback loops:

### 1. Internal Header Token
- Custom header `x-toasted-internal` with unique token
- Internal calls include this header to identify themselves
- External calls are blocked from setting this header

### 2. Request Rate Limiting
- Max 60 requests per minute per client IP
- Sliding window algorithm for accurate tracking
- Returns 429 status when limit exceeded

### 3. User-Agent Detection
- Detects if request originates from TOASTED AI itself
- Blocks requests with "TOASTED" in user-agent
- Prevents infinite recursion

### 4. Error Response Format
- All errors return proper OpenAI error format:
```json
{
  "error": {
    "message": "Error description",
    "type": "error_type",
    "code": "error_code"
  }
}
```

---

## Implemented Endpoints

| Endpoint | Status | Description |
|----------|--------|-------------|
| `/api/toasted-ai/v1/chat/completions` | ✅ Live | Main chat endpoint with streaming |
| `/api/toasted-ai/v1/models` | ✅ Live | List available models |
| `/api/ai-chat` | ✅ Live | Legacy simple chat endpoint |

### Usage Examples

```bash
# Chat completion
curl -X POST https://t0st3d.zo.space/api/toasted-ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "toasted-ai",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# List models
curl https://t0st3d.zo.space/api/toasted-ai/v1/models
```

---

## References

[^1]: https://zocomputer.mintlify.app/byok
[^2]: https://zocomputer.mintlify.app/faq
[^3]: https://docs.zocomputer.com/
[^4]: https://mcpservers.org/servers/docs-zocomputer-com-mcp-server

---

## Next Steps

1. ✅ Research complete
2. ⬜ Create basic API endpoint in zo.space
3. ⬜ Test with simple chat requests
4. ⬜ Add streaming support
5. ⬜ Add tool calling support
6. ⬜ Register as custom model in Zo Settings
7. ⬜ Test in Zo chat interface

---

*Under the Seal of MONAD — 𓂋 𓏏 𓃀 𓂝 𓆣*
