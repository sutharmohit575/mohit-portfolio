"""
╔══════════════════════════════════════════════════════════════════╗
║     MOHIT.EXE Chatbot — CLI Demo & Test Suite                    ║
╚══════════════════════════════════════════════════════════════════╝
Run:
    python test_chatbot.py          # full demo
    python test_chatbot.py --repl   # interactive REPL
"""

import sys
import time
from chatbot_engine import ChatbotEngine, Trie, LRUCache, FuzzyScorer

GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def banner():
    print(f"""
{GREEN}╔══════════════════════════════════════════════════════════════╗
║       MOHIT.EXE — AI Chatbot (DSA Edition)  v1.0            ║
║       Trie · LRU Cache · Min-Heap · BFS Graph · Deque       ║
╚══════════════════════════════════════════════════════════════╝{RESET}
""")


def fmt_response(result: dict):
    print(f"\n{CYAN}[MOHIT.EXE]{RESET} {BOLD}Intent:{RESET} {YELLOW}{result['intent']}{RESET}")
    print(f"\n{result['text']}")
    if result["suggestions"]:
        print(f"\n{DIM}💡 You might also ask about: {', '.join(result['suggestions'])}{RESET}")
    trace = result.get("dsa_trace", {})
    print(f"{DIM}[DSA] Trie hit: {trace.get('trie_hit')}  "
          f"| Cache: {trace.get('cache_ratio')}  "
          f"| From cache: {result['from_cache']}{RESET}")
    print()


# ── UNIT TESTS ─────────────────────────────────────────────────
def run_tests():
    print(f"{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}  UNIT TESTS{RESET}")
    print(f"{BOLD}{'═'*60}{RESET}\n")

    passed = failed = 0

    def test(name: str, condition: bool):
        nonlocal passed, failed
        if condition:
            print(f"  {GREEN}✓{RESET}  {name}")
            passed += 1
        else:
            print(f"  {RED}✗{RESET}  {name}")
            failed += 1

    # ── Trie ──────────────────────────────────────────────────
    print(f"{CYAN}Trie{RESET}")
    t = Trie()
    t.insert("hello", "greeting")
    t.insert("help", "help")
    t.insert("hi there", "greeting")
    t.insert("project", "projects")

    test("Trie: exact phrase match",    t.contains_phrase("hello world") == "greeting")
    test("Trie: mid-string match",      t.contains_phrase("say hello to mohit") == "greeting")
    test("Trie: prefix match 'hel'",    t.search_prefix("hello") == "greeting")
    test("Trie: multi-word phrase",     t.contains_phrase("hi there how are you") == "greeting")
    test("Trie: miss → None",           t.contains_phrase("xyz unknown") is None)

    # ── LRU Cache ─────────────────────────────────────────────
    print(f"\n{CYAN}LRU Cache{RESET}")
    cache = LRUCache(capacity=3)
    cache.put("a", 1); cache.put("b", 2); cache.put("c", 3)
    test("LRU: get existing key",       cache.get("a") == 1)
    cache.put("d", 4)   # evicts "b" (LRU after "a" was accessed)
    test("LRU: eviction of LRU item",   cache.get("b") is None)
    test("LRU: recently used survives", cache.get("d") == 4)
    test("LRU: capacity respected",     len(cache.cache) == 3)

    # ── FuzzyScorer ───────────────────────────────────────────
    print(f"\n{CYAN}FuzzyScorer (Min-Heap){RESET}")
    from chatbot_engine import KEYWORD_MAP
    scorer = FuzzyScorer(KEYWORD_MAP)
    results = scorer.score("tell me about python skills", top_n=3)
    intents = [r[1] for r in results]
    test("Fuzzy: python query hits 'python'",  "python" in intents)
    test("Fuzzy: python query hits 'skills'",  "skills" in intents)
    test("Fuzzy: returns <= top_n",            len(results) <= 3)
    test("Fuzzy: scores sorted desc",          all(results[i][0] >= results[i+1][0] for i in range(len(results)-1)))

    # ── ConversationGraph / BFS ───────────────────────────────
    print(f"\n{CYAN}BFS Conversation Graph{RESET}")
    engine_test = ChatbotEngine()
    path = engine_test.graph.bfs_next("skills", "contact")
    test("BFS: finds path skills→contact",     len(path) > 0)
    test("BFS: path starts at 'skills'",       path[0] == "skills")
    test("BFS: path ends at 'contact'",        path[-1] == "contact")
    path2 = engine_test.graph.bfs_next("greeting", "greeting")
    test("BFS: same node path is trivial",     path2 == ["greeting"])

    # ── Full Engine ───────────────────────────────────────────
    print(f"\n{CYAN}ChatbotEngine (end-to-end){RESET}")
    eng = ChatbotEngine()
    r1 = eng.respond("hello")
    test("Engine: greeting intent",            r1["intent"] == "greeting")
    r2 = eng.respond("what are his skills")
    test("Engine: skills intent",              r2["intent"] == "skills")
    r3 = eng.respond("what are his skills")   # repeated — should hit cache
    test("Engine: LRU cache hit on repeat",    r3["from_cache"] == True)
    r4 = eng.respond("show me projects")
    test("Engine: projects intent",            r4["intent"] == "projects")
    r5 = eng.respond("how to contact mohit")
    test("Engine: contact intent",             r5["intent"] == "contact")
    r6 = eng.respond("tell me about neuralchat")
    test("Engine: project-specific intent",    r6["intent"] == "neuralchat")
    r7 = eng.respond("qwerty zxcvb gibberish")
    test("Engine: unknown fallback",           r7["intent"] == "unknown")
    r8 = eng.respond("is he available for hire")
    test("Engine: hire/availability intent",   r8["intent"] in ["hire", "availability"])
    r9 = eng.respond("what data structures are used")
    test("Engine: dsa intent",                 r9["intent"] == "dsa")

    print(f"\n{'─'*40}")
    status = f"{GREEN}ALL PASSED{RESET}" if failed == 0 else f"{RED}{failed} FAILED{RESET}"
    print(f"  Results: {GREEN}{passed} passed{RESET}, {status}")
    print(f"{'═'*60}\n")
    return failed == 0


# ── DEMO CONVERSATION ──────────────────────────────────────────
def run_demo():
    print(f"{BOLD}{'═'*60}{RESET}")
    print(f"{BOLD}  DEMO CONVERSATION{RESET}")
    print(f"{BOLD}{'═'*60}{RESET}\n")

    engine = ChatbotEngine()
    demo_queries = [
        "Hello!",
        "Tell me about Mohit",
        "What are his skills?",
        "Show me some projects",
        "Tell me about NeuralChat",
        "How to contact him?",
        "Can I hire him for freelance?",
        "What is this chatbot built with?",
        "What are his skills?",    # should be cached
    ]

    for q in demo_queries:
        print(f"{YELLOW}YOU: {q}{RESET}")
        t0 = time.perf_counter()
        result = engine.respond(q)
        elapsed = (time.perf_counter() - t0) * 1000
        fmt_response(result)
        print(f"{DIM}  (responded in {elapsed:.3f}ms){RESET}\n")
        time.sleep(0.1)

    stats = engine.stats()
    print(f"{CYAN}{'─'*40}{RESET}")
    print(f"{CYAN}Engine Stats:{RESET}")
    for k, v in stats.items():
        print(f"  {k}: {v}")


# ── REPL ──────────────────────────────────────────────────────
def run_repl():
    banner()
    print(f"Type your message and press Enter. Type {YELLOW}quit{RESET} to exit.\n")
    engine = ChatbotEngine()
    while True:
        try:
            user_input = input(f"{YELLOW}YOU: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! 👋")
            break
        if user_input.lower() in ("quit", "exit", "bye", "q"):
            print(f"\n{GREEN}MOHIT.EXE:{RESET} Goodbye! Feel free to reach out at mohit@dev.io 👋")
            break
        if not user_input:
            continue
        result = engine.respond(user_input)
        fmt_response(result)
        if user_input.lower() == "stats":
            for k, v in engine.stats().items():
                print(f"  {k}: {v}")


# ── Entry ─────────────────────────────────────────────────────
if __name__ == "__main__":
    banner()
    if "--repl" in sys.argv:
        run_repl()
    else:
        ok = run_tests()
        run_demo()
        sys.exit(0 if ok else 1)
