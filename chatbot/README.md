# 🤖 Mohit.exe — AI Chatbot (DSA Edition)

A portfolio chatbot built entirely from classical Data Structures & Algorithms.
No external AI APIs. No ML models. Pure Python logic.

## Data Structures Used

| Structure | Purpose | Complexity |
|---|---|---|
| **Trie** | Intent prefix matching | O(m) per lookup |
| **LRU Cache** | Memoize repeated queries | O(1) get/put |
| **Min-Heap** | Ranked fuzzy keyword scoring | O(k log k) |
| **BFS Graph** | Conversation flow navigation | O(V + E) |
| **Deque** | Bounded context window | O(1) push/pop |
| **HashMap** | Knowledge base lookup | O(1) |

## Files

```
chatbot/
├── chatbot_engine.py   ← DSA brain (pure Python, zero dependencies)
├── server.py           ← FastAPI REST API wrapper
├── test_chatbot.py     ← 26 unit tests
├── requirements.txt    ← fastapi + uvicorn only
└── README.md
```

## How to Run

**IMPORTANT: always run from inside the chatbot/ folder.**

```bash
# Step 1 — go into the chatbot folder
cd mohit_portfolio/chatbot

# Step 2 — start the server
uvicorn server:app --reload --port 8001

# Step 3 — verify it works (open in browser)
# http://localhost:8001/health   → {"status": "online", ...}
# http://localhost:8001/docs     → Swagger UI to test chat
```

## Test the chat endpoint

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "what are his skills?"}'
```

## Run tests

```bash
# From inside chatbot/ folder
python test_chatbot.py
# Expected: 26 passed, ALL PASSED
```

## API Endpoints

| Method | URL | Description |
|---|---|---|
| `GET` | `/` | Redirects to `/docs` |
| `POST` | `/chat` | Send message, get response |
| `GET` | `/health` | Check server is running |
| `GET` | `/stats` | DSA engine statistics |
| `GET` | `/docs` | Swagger UI |

## Embed the widget in index.html

Copy the contents of `chatbot_widget.html` and paste it
just before `</body>` in your `app/templates/index.html`.

The widget works **standalone in the browser** with no server needed.
To connect to the Python API instead, change the fetch URL inside
the widget's `CHATBOT.send()` function to `http://localhost:8001/chat`.
