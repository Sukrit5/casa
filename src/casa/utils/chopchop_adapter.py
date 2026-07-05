"""Adapter to use ChopChop RealizabilityChecker with CASA."""

from llm.realizability import RealizabilityChecker
from core.lark.from_lark import parse_attribute_grammar
from core.grammar import Application
from importlib.resources import files

pkg = "demo"
grammar_text = files(pkg).joinpath("new_grammar.lark").read_text()
ast_text = files(pkg).joinpath("new_abstract_syntax.py").read_text()
rewrite_text = files(pkg).joinpath("typed_pruner.py").read_text()

ns = {}
exec(ast_text, ns)
constructors = [
    c for c in ns.values()
    if isinstance(c, type) and issubclass(c, Application) and c.__module__ == "builtins"
]

exec(rewrite_text, ns)
pruner = ns["pruner"]

lexer_spec, parser = parse_attribute_grammar(
    constructors, grammar_text, "start"
).build_parser()

_chopchop_checker = RealizabilityChecker(pruner, parser, lexer_spec)


def check_tokens_realizable(token_ids, tokenizer, _unused=None):
    """
    Check if token sequence is realizable using ChopChop.

    Args:
        token_ids: torch.Tensor of token IDs
        tokenizer: HuggingFace tokenizer
        _unused: Ignored (for compatibility with old API)

    Returns:
        bool: True if realizable, False otherwise
    """
    text = tokenizer.decode(token_ids)
    return _chopchop_checker.realizable(text)
