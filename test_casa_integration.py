#!/usr/bin/env python
"""Test CASA sampling with ChopChop integration."""
import sys
sys.path.insert(0, '/Users/sukritmangla/chopchop/casa/src')

from casa import LLM, Grammar, CARS

print("Loading GPT-2 model (lighter for testing)...")
llm = LLM.from_pretrained("gpt2", is_chat_model=False)

# Create a grammar compatible with llguidance (without ChopChop annotations)
print("Creating grammar...")
grammar_str = """
start: expr

expr: bool
     | "if" expr "then" expr "else" expr
     | ZERO
     | "succ" expr
     | "pred" expr
     | "iszero" expr

bool: TRUE
    | FALSE

TRUE: /true/
FALSE: /false/
ZERO: /0/
WS: /\\s+/

%ignore WS
"""
grammar = Grammar.from_string(grammar_str, llm.tokenizer)

prompt = """Generate a valid expression in this simple typed language:

Grammar rules:
- Booleans: true, false
- Numbers: 0, succ <expr>, pred <expr>
- Conditionals: if <expr> then <expr> else <expr>
- Type check: iszero <expr>

Examples:
- if true then false else true
- if iszero 0 then succ 0 else 0
- pred succ succ 0

Generate one valid expression: """

print("Testing CARS sampling with ChopChop integration...")
sampler = CARS(llm, grammar, max_new_tokens=50, verbose=True)
results = sampler.sample(prompt, n_samples=3, max_attempts=100)

print(f"\n{'='*60}")
print(f"Generated {len(results)} samples:")
print(f"{'='*60}")
for i, result in enumerate(results, 1):
    print(f"\n{i}. Text: '{result.text}'")
    print(f"   Token IDs: {result.token_ids}")
    print(f"   Tokens: {result.tokens}")
    print(f"   Attempts: {result.n_attempts}")
    print(f"   Raw logprob: {result.raw_logprob:.3f}")
