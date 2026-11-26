from __future__ import annotations

import time

from expr_tree import (
    Add,
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


def main() -> None:
    sub_expr = Sub(Num(10), Num(4))
    sample = Mul(Add(Num(2), sub_expr), sub_expr)

    print("=== Дерево математичного виразу ===")
    print(f"Рекурсивне обчислення: {eval_expr(sample)}")
    print(f"Ітеративне обчислення: {eval_expr_iterative(sample)}")
    print(f"Кількість вузлів: {count_nodes(sample)}")
    print(f"Висота дерева: {tree_height(sample)}")

    deep_shared = build_repeated_expr(18)

    t0 = time.perf_counter()
    res_plain = eval_expr(deep_shared)
    dt_plain = (time.perf_counter() - t0) * 1000.0

    eval_expr_memo.cache_clear()
    t1 = time.perf_counter()
    res_memo = eval_expr_memo(deep_shared)
    dt_memo = (time.perf_counter() - t1) * 1000.0
    info = eval_expr_memo.cache_info()

    print("=== Порівняння часу на повторних підвиразах (глибина 18) ===")
    print(f"Без мемоізації: {res_plain} ({dt_plain:.3f} мс)")
    print(f"З @lru_cache:   {res_memo} ({dt_memo:.3f} мс, hits={info.hits})")


if __name__ == "__main__":
    main()
