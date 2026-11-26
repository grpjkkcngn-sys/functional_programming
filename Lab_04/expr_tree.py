from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Union


@dataclass(frozen=True)
class Num:
    value: int


@dataclass(frozen=True)
class Add:
    left: Expr
    right: Expr
    _cached_hash: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        h = hash(("+", self.left, self.right))
        object.__setattr__(self, "_cached_hash", h)

    def __hash__(self) -> int:
        return self._cached_hash


@dataclass(frozen=True)
class Sub:
    left: Expr
    right: Expr
    _cached_hash: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        h = hash(("-", self.left, self.right))
        object.__setattr__(self, "_cached_hash", h)

    def __hash__(self) -> int:
        return self._cached_hash


@dataclass(frozen=True)
class Mul:
    left: Expr
    right: Expr
    _cached_hash: int = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        h = hash(("*", self.left, self.right))
        object.__setattr__(self, "_cached_hash", h)

    def __hash__(self) -> int:
        return self._cached_hash


Expr = Union[Num, Add, Sub, Mul]


def eval_expr(expr: Expr) -> int:
    if isinstance(expr, Num):
        return expr.value
    if isinstance(expr, Add):
        return eval_expr(expr.left) + eval_expr(expr.right)
    if isinstance(expr, Sub):
        return eval_expr(expr.left) - eval_expr(expr.right)
    if isinstance(expr, Mul):
        return eval_expr(expr.left) * eval_expr(expr.right)
    raise TypeError("Unsupported expression node")


@lru_cache(maxsize=None)
def eval_expr_memo(expr: Expr) -> int:
    if isinstance(expr, Num):
        return expr.value
    if isinstance(expr, Add):
        return eval_expr_memo(expr.left) + eval_expr_memo(expr.right)
    if isinstance(expr, Sub):
        return eval_expr_memo(expr.left) - eval_expr_memo(expr.right)
    if isinstance(expr, Mul):
        return eval_expr_memo(expr.left) * eval_expr_memo(expr.right)
    raise TypeError("Unsupported expression node")


def count_nodes(expr: Expr) -> int:
    if isinstance(expr, Num):
        return 1
    if isinstance(expr, (Add, Sub, Mul)):
        return 1 + count_nodes(expr.left) + count_nodes(expr.right)
    raise TypeError("Unsupported expression node")


def tree_height(expr: Expr) -> int:
    if isinstance(expr, Num):
        return 1
    if isinstance(expr, (Add, Sub, Mul)):
        return 1 + max(tree_height(expr.left), tree_height(expr.right))
    raise TypeError("Unsupported expression node")


def eval_expr_iterative(expr: Expr) -> int:
    stack: List[object] = [expr]
    values: List[int] = []
    while stack:
        current = stack.pop()
        if isinstance(current, Num):
            values.append(current.value)
        elif isinstance(current, str):
            rhs = values.pop()
            lhs = values.pop()
            if current == "+":
                values.append(lhs + rhs)
            elif current == "-":
                values.append(lhs - rhs)
            elif current == "*":
                values.append(lhs * rhs)
        elif isinstance(current, Add):
            stack.append("+")
            stack.append(current.right)
            stack.append(current.left)
        elif isinstance(current, Sub):
            stack.append("-")
            stack.append(current.right)
            stack.append(current.left)
        elif isinstance(current, Mul):
            stack.append("*")
            stack.append(current.right)
            stack.append(current.left)
        else:
            raise TypeError("Unsupported expression node")
    return values[-1] if values else 0


def build_repeated_expr(depth: int) -> Expr:
    current: Expr = Num(1)
    for _ in range(depth):
        current = Add(current, current)
    return current
