from typing import Optional

from cawdrey import frozendict

def context_to_dict(context: frozendict) -> dict:
    keys = [key for key in context.keys()]
    context_dict = {}
    for key in sorted(keys):
        context_dict[key] = context.get(key)
    return context_dict


def dict_to_context(context_dict: Optional[dict]) -> Optional[frozendict]:
    if not context_dict:
        return None
    return frozendict(**context_dict)
