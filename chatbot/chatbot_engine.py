"""
╔══════════════════════════════════════════════════════════════════╗
║         MOHIT.EXE — AI CHATBOT ENGINE  (DSA Edition)             ║
║                                                                  ║
║  Data Structures Used:                                           ║
║   • Trie          — O(m) intent prefix matching                  ║
║   • HashMap       — O(1) response lookup                         ║
║   • BFS/Graph     — conversation flow traversal                  ║
║   • Min-Heap      — ranked fuzzy keyword scoring                 ║
║   • Deque         — bounded conversation history (context)       ║
║   • LRU Cache     — memoize repeated query responses             ║
╚══════════════════════════════════════════════════════════════════╝
"""

from collections import deque, defaultdict
import heapq
import time
import re
import math


# ══════════════════════════════════════════════════════════════════
# 1. TRIE — prefix-based intent matching  O(m) per lookup
# ══════════════════════════════════════════════════════════════════
class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.intent: str | None = None          # leaf stores intent key
        self.is_end: bool = False


class Trie:
    """
    Stores known trigger phrases.
    Allows O(m) prefix lookup where m = word length.
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, phrase: str, intent: str) -> None:
        node = self.root
        for ch in phrase.lower():
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True
        node.intent = intent

    def search_prefix(self, text: str) -> str | None:
        """Return intent if any inserted phrase is a prefix of text."""
        node = self.root
        for ch in text.lower():
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.is_end:
                return node.intent
        return None

    def contains_phrase(self, text: str) -> str | None:
        """
        Tokenize text into words, then check each consecutive word-window
        against the Trie to avoid substring false matches
        (e.g. 'hi' inside 'his' or 'skills').
        """
        text_lower = text.lower()
        # Build list of tokens preserving spacing positions
        tokens = re.findall(r"[a-z0-9']+", text_lower)
        n = len(tokens)
        # Try every window length from longest to shortest (greedy)
        for window in range(n, 0, -1):
            for start in range(n - window + 1):
                phrase = " ".join(tokens[start:start + window])
                node = self.root
                matched = True
                for ch in phrase:
                    if ch not in node.children:
                        matched = False
                        break
                    node = node.children[ch]
                if matched and node.is_end:
                    return node.intent
        return None


# ══════════════════════════════════════════════════════════════════
# 2. LRU CACHE — memoize repeated queries  O(1) get/put
# ══════════════════════════════════════════════════════════════════
class LRUNode:
    def __init__(self, key, val):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    """
    Doubly-linked list + HashMap.
    O(1) get and put. Evicts least-recently-used.
    """
    def __init__(self, capacity: int = 64):
        self.cap = capacity
        self.cache: dict[str, LRUNode] = {}
        self.head = LRUNode("HEAD", None)   # sentinel
        self.tail = LRUNode("TAIL", None)   # sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: LRUNode) -> None:
        node.prev.next, node.next.prev = node.next, node.prev

    def _insert_front(self, node: LRUNode) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: str):
        if key not in self.cache:
            return None
        self._remove(self.cache[key])
        self._insert_front(self.cache[key])
        return self.cache[key].val

    def put(self, key: str, val) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = LRUNode(key, val)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# ══════════════════════════════════════════════════════════════════
# 3. FUZZY SCORER — Min-Heap ranked keyword matching  O(k log k)
# ══════════════════════════════════════════════════════════════════
class FuzzyScorer:
    """
    Scores each response category against a query using keyword
    frequency + TF-IDF-style weighting.
    Uses a min-heap to return top-N candidates efficiently.
    """
    def __init__(self, keyword_map: dict[str, list[str]]):
        # keyword_map: {intent: [kw1, kw2, ...]}
        self.km = keyword_map
        # IDF-like weight: rarer keywords across intents score higher
        kw_freq: dict[str, int] = defaultdict(int)
        for kws in keyword_map.values():
            for kw in kws:
                kw_freq[kw] += 1
        total = len(keyword_map)
        self.idf = {kw: math.log(total / freq + 1) for kw, freq in kw_freq.items()}

    def score(self, query: str, top_n: int = 3) -> list[tuple[float, str]]:
        """Return top_n (score, intent) using min-heap. O(k log top_n)"""
        tokens = set(re.findall(r'\w+', query.lower()))
        heap: list[tuple[float, str]] = []   # min-heap by neg score
        for intent, keywords in self.km.items():
            s = 0.0
            for kw in keywords:
                if kw in tokens:
                    s += self.idf.get(kw, 1.0)
            if s > 0:
                # negate score for min-heap → effectively a max-heap
                heapq.heappush(heap, (-s, intent))
        results = []
        for _ in range(min(top_n, len(heap))):
            neg_s, intent = heapq.heappop(heap)
            results.append((-neg_s, intent))
        return results


# ══════════════════════════════════════════════════════════════════
# 4. CONVERSATION GRAPH — BFS flow  O(V+E)
# ══════════════════════════════════════════════════════════════════
class ConversationGraph:
    """
    Directed graph of conversation states.
    BFS finds the shortest path from current state to a target intent.
    Used to suggest a natural next topic to the user.
    """
    def __init__(self):
        self.graph: dict[str, list[str]] = defaultdict(list)

    def add_edge(self, src: str, dst: str) -> None:
        self.graph[src].append(dst)

    def bfs_next(self, current: str, target: str) -> list[str]:
        """BFS shortest path from current → target. O(V+E)"""
        if current == target:
            return [current]
        visited = {current}
        queue = deque([[current]])
        while queue:
            path = queue.popleft()
            node = path[-1]
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    if neighbor == target:
                        return new_path
                    visited.add(neighbor)
                    queue.append(new_path)
        return []

    def suggest_next(self, current: str) -> list[str]:
        """Return direct neighbors of current state."""
        return self.graph.get(current, [])


# ══════════════════════════════════════════════════════════════════
# 5. KNOWLEDGE BASE  (HashMap)  O(1) lookup
# ══════════════════════════════════════════════════════════════════
RESPONSES: dict[str, dict] = {
    "greeting": {
        "text": "Hey! 👋 I'm Mohit.exe — your interactive guide. Ask me anything about Mohit's skills, projects, experience, or how to hire him!",
        "suggestions": ["skills", "projects", "contact"],
    },
    "about": {
        "text": "Mohit is a full-stack developer with 4+ years of experience. He builds AI-powered web apps, scalable backends, and occasionally things that probably shouldn't exist 😄. Currently open to freelance and full-time roles.",
        "suggestions": ["skills", "projects", "contact"],
    },
    "skills": {
        "text": "🛠 Mohit's stack:\n• Frontend: React, Next.js, HTML5, CSS3, Three.js\n• Backend:  Node.js, Python, FastAPI, REST/GraphQL\n• AI/ML:    LangChain, OpenAI API, Pinecone, RAG\n• Database: PostgreSQL, MongoDB, Redis\n• DevOps:   Docker, AWS, CI/CD, Git",
        "suggestions": ["projects", "experience", "contact"],
    },
    "projects": {
        "text": "📁 Notable projects:\n1. NeuralChat   — AI multi-model chat (2k+ users)\n2. PixelMart    — E-commerce + AI recommendations\n3. CryptoVault  — Zero-knowledge password manager\n4. AutoScribe   — Document AI (500+ businesses)\n\nType a project name to learn more!",
        "suggestions": ["neuralchat", "pixelmart", "cryptovault", "autoscribe"],
    },
    "neuralchat": {
        "text": "⚡ NeuralChat\nStack: React · WebSocket · OpenAI API · Redis\nFeatures: Multi-model support, plugin system, custom memory, real-time streaming\nUsers: 2,000+ active\nDemo: neuralchat.mohit.dev",
        "suggestions": ["pixelmart", "contact", "skills"],
    },
    "pixelmart": {
        "text": "🛒 PixelMart\nStack: Next.js · Stripe · PostgreSQL · Vercel\nFeatures: Real-time inventory, AI-powered recommendations, blazing-fast checkout\nDemo: pixelmart.mohit.dev",
        "suggestions": ["neuralchat", "contact", "skills"],
    },
    "cryptovault": {
        "text": "🔐 CryptoVault\nStack: Rust · AES-256 · WebAssembly · SQLite\nFeatures: Zero-knowledge encryption, browser extension, TOTP 2FA\nOpen source: github.com/sutharmohit575/cryptovault",
        "suggestions": ["autoscribe", "contact", "skills"],
    },
    "autoscribe": {
        "text": "🤖 AutoScribe\nStack: Python · LangChain · FastAPI · Pinecone\nFeatures: Extract, summarize, Q&A on any document\nUsers: 500+ businesses\nDemo: autoscribe.mohit.dev",
        "suggestions": ["neuralchat", "contact", "skills"],
    },
    "experience": {
        "text": "📅 Experience:\n• 4+ years full-stack development\n• 24+ shipped production projects\n• Built AI tools used by 500+ companies\n• Open source contributor\n• Specialism: scalable web apps + AI integrations",
        "suggestions": ["skills", "projects", "contact"],
    },
    "contact": {
        "text": "📬 Reach Mohit:\n• Email:    sutharmohit575@gmail.com\n• GitHub:   github.com/sutharmohit575\n• LinkedIn: linkedin.com/in/suthar-mohit575\n• Response: < 24 hours\n\nOr use the ⚔ CONTACT BOSS form on this page!",
        "suggestions": ["projects", "about"],
    },
    "hire": {
        "text": "🚀 Mohit is open to:\n• Freelance projects (any size)\n• Full-time positions\n• Open source collaborations\n• Consulting & technical audits\n\nRates: Let's talk — he's not cheap, but he's worth it 😄\nEmail: sutharmohit575@gmail.com",
        "suggestions": ["skills", "projects", "contact"],
    },
    "education": {
        "text": "🎓 Mohit is mostly self-taught — the internet, open source, and an unhealthy number of side projects. He believes in learning by building.",
        "suggestions": ["skills", "projects", "about"],
    },
    "location": {
        "text": "📍 Based in India (IST — UTC+5:30). Available for remote work worldwide, and occasionally for on-site roles.",
        "suggestions": ["contact", "hire"],
    },
    "ai": {
        "text": "🤖 AI/ML expertise:\n• LangChain, LlamaIndex, RAG pipelines\n• OpenAI, Gemini, Claude API integrations\n• Vector databases: Pinecone, Chroma, Weaviate\n• Fine-tuning, embeddings, prompt engineering\nProject example: AutoScribe uses all of the above!",
        "suggestions": ["autoscribe", "skills", "contact"],
    },
    "python": {
        "text": "🐍 Python is one of Mohit's primary languages:\n• FastAPI / Django for backend APIs\n• Data processing: Pandas, NumPy\n• AI/ML: PyTorch, scikit-learn, Transformers\n• Scripting, automation, and CLI tools\nYou're actually talking to a Python DSA chatbot right now 😄",
        "suggestions": ["skills", "ai", "projects"],
    },
    "javascript": {
        "text": "⚡ JavaScript / TypeScript:\n• React, Next.js, Vue\n• Node.js + Express / Fastify\n• WebSockets, WebRTC, Web APIs\n• Full-stack with TypeScript end-to-end",
        "suggestions": ["skills", "projects", "react"],
    },
    "react": {
        "text": "⚛ React / Next.js:\n• Component architecture, hooks, context\n• Server-side rendering + static generation\n• App Router, edge functions\n• Performance optimization (code-splitting, memoization)",
        "suggestions": ["javascript", "projects", "skills"],
    },
    "dsa": {
        "text": "📐 Fun fact: this chatbot IS a DSA project!\n• Trie       — O(m) intent prefix matching\n• LRU Cache  — O(1) memoization of repeated queries\n• Min-Heap   — ranked fuzzy keyword scoring\n• BFS/Graph  — conversation flow navigation\n• Deque      — bounded context window\n• HashMap    — O(1) response lookup\n\nAll implemented in pure Python 🐍",
        "suggestions": ["python", "skills", "about"],
    },
    "game": {
        "text": "🎮 Mohit's a gamer! Favorite: Hollow Knight (112% completion). The portfolio itself is game-themed — try the terminal, Snake.EXE, or the Konami code (↑↑↓↓←→←→BA)!",
        "suggestions": ["about", "projects"],
    },
    "availability": {
        "text": "✅ Mohit is currently OPEN TO WORK.\nAvailable for:\n• Full-time (remote or hybrid)\n• Freelance & contracts\n• Part-time consulting\nResponse time: < 24 hours",
        "suggestions": ["contact", "hire", "skills"],
    },
    "unknown": {
        "text": "Hmm, I didn't quite catch that 🤔 Try asking about:\n• skills / projects / experience\n• A specific project (NeuralChat, PixelMart...)\n• How to contact or hire Mohit\n• Python, JavaScript, React, AI\n• Or just say 'help'!",
        "suggestions": ["skills", "projects", "contact"],
    },
    "help": {
        "text": "💡 Things you can ask me:\n• 'Tell me about Mohit'\n• 'What are his skills?'\n• 'Show me projects'\n• 'How to contact?'\n• 'Can I hire him?'\n• 'Tell me about NeuralChat'\n• 'What is this chatbot built with?' (dsa)\n• 'Is he available?'",
        "suggestions": ["about", "skills", "contact"],
    },
}

# Intent trigger phrases → Trie
INTENT_PHRASES: list[tuple[str, str]] = [
    ("hello", "greeting"), ("hi", "greeting"), ("hey", "greeting"), ("good morning", "greeting"), ("what's up", "greeting"),
    ("about", "about"), ("who is mohit", "about"), ("tell me about", "about"), ("introduce", "about"),
    ("skill", "skills"), ("technology", "skills"), ("tech stack", "skills"), ("what can", "skills"), ("expertise", "skills"),
    ("project", "projects"), ("portfolio", "projects"), ("work", "projects"), ("built", "projects"),
    ("neural", "neuralchat"), ("neuralchat", "neuralchat"), ("chat app", "neuralchat"), ("neural chat", "neuralchat"),
    ("pixel", "pixelmart"), ("pixelmart", "pixelmart"), ("pixel mart", "pixelmart"), ("ecommerce", "pixelmart"), ("shop", "pixelmart"),
    ("crypto", "cryptovault"), ("cryptovault", "cryptovault"), ("crypto vault", "cryptovault"), ("password", "cryptovault"), ("vault", "cryptovault"), ("security", "cryptovault"),
    ("autoscribe", "autoscribe"), ("auto scribe", "autoscribe"), ("document", "autoscribe"), ("summarize", "autoscribe"),
    ("experience", "experience"), ("years", "experience"), ("background", "experience"),
    ("contact", "contact"), ("email", "contact"), ("reach", "contact"), ("github", "contact"), ("linkedin", "contact"),
    ("hire", "hire"), ("freelance", "hire"), ("job", "hire"), ("salary", "hire"), ("rate", "hire"), ("available", "availability"),
    ("education", "education"), ("study", "education"), ("degree", "education"), ("university", "education"),
    ("location", "location"), ("where", "location"), ("india", "location"), ("remote", "location"),
    ("artificial intelligence", "ai"), ("machine learning", "ai"), ("ai", "ai"), ("ml", "ai"), ("langchain", "ai"), ("openai", "ai"),
    ("python", "python"), ("django", "python"), ("fastapi", "python"),
    ("javascript", "javascript"), ("typescript", "javascript"), ("js", "javascript"),
    ("react", "react"), ("next", "react"), ("nextjs", "react"),
    ("data structure", "dsa"), ("algorithm", "dsa"), ("dsa", "dsa"), ("trie", "dsa"), ("how is this built", "dsa"),
    ("game", "game"), ("gaming", "game"), ("hollow knight", "game"), ("snake", "game"),
    ("help", "help"), ("what can you", "help"), ("commands", "help"),
]

# Keyword map for fuzzy scoring (FuzzyScorer)
KEYWORD_MAP: dict[str, list[str]] = {
    "greeting":    ["hello","hi","hey","morning","evening","greet","start","howdy","sup","yo"],
    "about":       ["mohit","about","who","developer","person","introduce","profile","self","himself","background"],
    "skills":      ["skill","skills","tech","stack","technology","language","framework","know","expertise","use","capable","what","his","does"],
    "projects":    ["project","projects","built","made","created","portfolio","work","show","some","app","application","website","portfolio"],
    "neuralchat":  ["neural","neuralchat","chat","conversation","ai","message","realtime","websocket","openai","talker"],
    "pixelmart":   ["pixel","pixelmart","mart","shop","ecommerce","buy","sell","store","stripe","payment","commerce"],
    "cryptovault": ["crypto","cryptovault","vault","password","secure","encrypt","aes","wasm","manager","safe","security"],
    "autoscribe":  ["auto","autoscribe","scribe","document","pdf","summarize","extract","langchain","vector","doc"],
    "experience":  ["experience","year","years","history","background","career","professional","past","worked","long"],
    "contact":     ["contact","email","reach","message","linkedin","github","social","connect","touch","find","him"],
    "hire":        ["hire","hiring","freelance","job","salary","rate","contract","employ","position","role","work","opportunity"],
    "education":   ["education","study","degree","learn","university","college","school","course","self","taught"],
    "location":    ["location","where","india","remote","timezone","based","live","city","country","place"],
    "ai":          ["ai","ml","artificial","intelligence","machine","learning","neural","model","langchain","openai","gpt","llm","nlp"],
    "python":      ["python","django","fastapi","flask","pip","script","backend","data","numpy","pandas","snake"],
    "javascript":  ["javascript","typescript","js","ts","node","express","frontend","browser","web","nodejs"],
    "react":       ["react","reactjs","next","nextjs","component","hook","jsx","frontend","ui","interface"],
    "dsa":         ["data","structure","algorithm","trie","heap","graph","bfs","cache","lru","complexity","built","chatbot","how","this","dsa"],
    "game":        ["game","gaming","play","snake","hollow","knight","konami","joystick","arcade","gamer","favorite"],
    "availability":["available","open","work","now","hire","status","currently","looking","opportunity","open to"],
    "help":        ["help","guide","tutorial","how","what","can","ask","question","command","options"],
}


# ══════════════════════════════════════════════════════════════════
# 6. MAIN CHATBOT ENGINE
# ══════════════════════════════════════════════════════════════════
class ChatbotEngine:
    """
    Combines all DSA structures into a single inference engine.

    Query resolution pipeline:
      1. Normalize input
      2. LRU cache hit?           → return cached response  O(1)
      3. Trie phrase scan         → direct intent match     O(n·m)
      4. FuzzyScorer (min-heap)   → keyword-based match     O(k log k)
      5. Conversation Graph (BFS) → suggest next topic      O(V+E)
      6. Store in LRU cache       → memoize result          O(1)
    """

    def __init__(self):
        # Build Trie
        self.trie = Trie()
        for phrase, intent in INTENT_PHRASES:
            self.trie.insert(phrase, intent)

        # Build FuzzyScorer
        self.scorer = FuzzyScorer(KEYWORD_MAP)

        # Build Conversation Graph
        self.graph = ConversationGraph()
        edges = [
            ("greeting", "about"), ("greeting", "skills"), ("greeting", "projects"),
            ("about", "skills"), ("about", "experience"), ("about", "contact"),
            ("skills", "projects"), ("skills", "ai"), ("skills", "python"),
            ("projects", "neuralchat"), ("projects", "pixelmart"), ("projects", "cryptovault"), ("projects", "autoscribe"),
            ("neuralchat", "pixelmart"), ("neuralchat", "contact"),
            ("pixelmart", "cryptovault"), ("pixelmart", "contact"),
            ("cryptovault", "autoscribe"), ("cryptovault", "contact"),
            ("autoscribe", "contact"), ("autoscribe", "ai"),
            ("experience", "contact"), ("experience", "hire"),
            ("contact", "hire"), ("hire", "contact"),
            ("ai", "autoscribe"), ("ai", "skills"),
            ("python", "ai"), ("python", "skills"),
            ("javascript", "react"), ("react", "projects"),
            ("dsa", "python"), ("dsa", "skills"),
        ]
        for src, dst in edges:
            self.graph.add_edge(src, dst)

        # LRU Cache
        self.cache = LRUCache(capacity=64)

        # Context window — last N intents (deque)
        self.context: deque[str] = deque(maxlen=8)
        self.last_intent: str = "greeting"

        # Stats
        self.total_queries = 0
        self.cache_hits = 0

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def _resolve_intent(self, text: str) -> str:
        """
        Pipeline (most specific → least specific):
          1. FuzzyScorer   — keyword match with IDF + specificity  O(k log k)
          2. Trie           — exact phrase match                   O(n·m)
          3. Context-aware — check suggestions from last intent
          4. Unknown
        """
        # Specificity rank: more specific intents beat generic ones on tie
        SPECIFICITY: dict[str, int] = {
            "neuralchat": 10, "pixelmart": 10, "cryptovault": 10, "autoscribe": 10,
            "python": 8, "javascript": 8, "react": 8, "ai": 8, "dsa": 8,
            "hire": 7, "availability": 7, "contact": 7, "location": 7, "education": 7,
            "skills": 6, "projects": 6, "experience": 6, "game": 6,
            "about": 4, "help": 3, "greeting": 2,
        }

        results = self.scorer.score(text, top_n=5)

        if results:
            # Boost score by specificity to break ties
            boosted = [(score + SPECIFICITY.get(intent, 0) * 0.01, score, intent)
                       for score, intent in results]
            boosted.sort(key=lambda x: x[0], reverse=True)
            top_score_raw = boosted[0][1]

            # High-confidence: raw score much higher than runner-up → use immediately
            if top_score_raw >= 2.0 and (len(boosted) < 2 or top_score_raw > boosted[1][1] + 0.5):
                return boosted[0][2]

            # Tie or close scores → use specificity-boosted winner
            if top_score_raw >= 0.5:
                return boosted[0][2]

        # Trie phrase scan fallback (catches greetings, short exact phrases)
        trie_intent = self.trie.contains_phrase(text)
        if trie_intent:
            return trie_intent

        # Context-aware fallback
        if self.last_intent in RESPONSES:
            suggestions = RESPONSES[self.last_intent].get("suggestions", [])
            for sug in suggestions:
                if sug in text.split():
                    return sug

        return "unknown"

    def respond(self, user_input: str) -> dict:
        self.total_queries += 1
        normalized = self._normalize(user_input)

        # LRU cache check
        cached = self.cache.get(normalized)
        if cached:
            self.cache_hits += 1
            cached["from_cache"] = True
            cached["context"] = list(self.context)
            return cached

        intent = self._resolve_intent(normalized)
        response_data = RESPONSES.get(intent, RESPONSES["unknown"])

        # BFS: suggest next conversation path
        next_topics = self.graph.suggest_next(intent)

        # Build response
        result = {
            "intent":       intent,
            "text":         response_data["text"],
            "suggestions":  response_data.get("suggestions", []),
            "next_topics":  next_topics[:3],
            "from_cache":   False,
            "context":      list(self.context),
            "query_number": self.total_queries,
            "dsa_trace": {
                "trie_hit":    self.trie.contains_phrase(normalized) is not None,
                "fuzzy_top":   self.scorer.score(normalized, top_n=1),
                "cache_ratio": f"{self.cache_hits}/{self.total_queries}",
            },
        }

        # Update context & cache
        self.context.append(intent)
        self.last_intent = intent
        self.cache.put(normalized, {**result})

        return result

    def stats(self) -> dict:
        return {
            "total_queries": self.total_queries,
            "cache_hits":    self.cache_hits,
            "cache_size":    len(self.cache.cache),
            "context":       list(self.context),
            "last_intent":   self.last_intent,
        }
