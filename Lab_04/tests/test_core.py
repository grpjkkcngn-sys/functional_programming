from copy import deepcopy

from expr_tree import (
    Add,
    Expr,
    Mul,
    Num,
    Sub,
    build_repeated_expr,
    count_nodes,
    eval_expr,
    eval_expr_iterative,
    eval_expr_memo,
    tree_height,
)


def sample_expression() -> Expr:
    sub_expr = Sub(Num(10), Num(4))
    return Mul(Add(Num(2), sub_expr), sub_expr)


def test_eval_basic_and_order_of_subtraction() -> None:
    assert eval_expr(Num(5)) == 5
    assert eval_expr(Sub(Num(10), Num(3))) == 7
    assert eval_expr_iterative(Sub(Num(10), Num(3))) == 7


def test_eval_and_iterative_parity_without_mutation() -> None:
    expr = sample_expression()
    snapshot = deepcopy(expr)
    expected = (2 + (10 - 4)) * (10 - 4)

    assert eval_expr(expr) == expected
    assert eval_expr_iterative(expr) == expected
    assert expr == snapshot


def test_tree_metrics() -> None:
    leaf = Num(7)
    assert count_nodes(leaf) == 1
    assert tree_height(leaf) == 1

    expr = sample_expression()
    assert count_nodes(expr) == 9
    assert tree_height(expr) == 4


def test_memoization_on_repeated_subexpressions() -> None:
    eval_expr_memo.cache_clear()
    expr = build_repeated_expr(12)

    result = eval_expr_memo(expr)
    info = eval_expr_memo.cache_info()

    assert result == 4096
    assert info.hits >= 12

    eval_expr_memo.cache_clear()
    assert eval_expr_memo.cache_info().currsize == 0


def test_iterative_deep_linear_tree() -> None:
    node: Expr = Num(0)
    for _ in range(1500):
        node = Add(node, Num(1))
    assert eval_expr_iterative(node) == 1500
