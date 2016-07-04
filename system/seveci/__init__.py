from . import simpleparser
from . import tokenizer
from . import utils
import os


def eval_and_exec(source):
    path = os.path.abspath(source)
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    tokens = None
    parsed = None

    tokens = [tok for tok in tokenizer.tokenize(content) if utils.is_ok(tok)]
    parsed = [p for p in [simpleparser.parse(content, toks) for toks in tokens] if utils.is_ok(p)]
    env = utils.standard_env()
    for line in parsed:
        val = simpleparser.evaluate(line, env)
        if val:
            yield utils.mtoa(val)
    yield None
