from copy import deepcopy
from typing import List

from core import (
    Transaction,
    calc_final_amount,
    is_successful,
    make_transaction_processor,
    with_calculated_fields,
)


def sample_data() -> List[Transaction]:
    return [
        {
            "id": 1,
            "tx_type": "card",
            "amount": 100.0,
            "currency": "USD",
            "status": "success",
        },
        {
            "id": 2,
            "tx_type": "card",
            "amount": 200.0,
            "currency": "USD",
            "status": "declined",
        },
        {
            "id": 3,
            "tx_type": "transfer",
            "amount": 200.0,
            "currency": "UAH",
            "status": "success",
        },
    ]


def test_referential_transparency() -> None:
    txs = sample_data()
    proc = make_transaction_processor(
        convert_currency=lambda a, c: a * 40.0 if c == "USD" else a,
        calc_commission=lambda a, _t: a * 0.02,
        accept_amount=lambda a: a >= 500.0,
    )
    assert proc(txs) == proc(txs)


def test_no_mutation() -> None:
    txs = sample_data()
    snapshot = deepcopy(txs)
    proc = make_transaction_processor(
        convert_currency=lambda a, c: a * 40.0 if c == "USD" else a,
        calc_commission=lambda _a, _t: 10.0,
        accept_amount=lambda a: a >= 0.0,
    )
    proc(txs)
    assert txs == snapshot


def test_callable_policies_and_filtering() -> None:
    txs = sample_data()
    proc = make_transaction_processor(
        convert_currency=lambda a, c: a * 40.0 if c == "USD" else a,
        calc_commission=lambda a, _t: a * 0.05,
        accept_amount=lambda a: a >= 1000.0,
    )
    res = proc(txs)
    assert res["count"] == 1
    assert res["total_volume"] == 3800.0
    assert res["total_commission"] == 200.0
    assert res["transactions"][0]["final_amount"] == 3800.0


def test_empty_and_unsuccessful_transactions() -> None:
    proc = make_transaction_processor(
        convert_currency=lambda a, _c: a,
        calc_commission=lambda a, _t: a * 0.01,
        accept_amount=lambda a: a >= 0.0,
    )
    failed_only: List[Transaction] = [
        {
            "id": 10,
            "tx_type": "card",
            "amount": 500.0,
            "currency": "UAH",
            "status": "failed",
        }
    ]
    assert proc([]) == {
        "count": 0,
        "total_volume": 0.0,
        "total_commission": 0.0,
        "transactions": [],
    }
    assert proc(failed_only)["count"] == 0


def test_pure_helper_functions() -> None:
    tx: Transaction = {
        "id": 7,
        "tx_type": "card",
        "amount": 100.0,
        "currency": "UAH",
        "status": "Success",
    }
    assert is_successful(tx) is True
    assert calc_final_amount(1000.0, 15.5) == 984.5

    updated = with_calculated_fields(tx, converted=100.0, commission=2.0, final=98.0)
    assert updated is not tx
    assert "final_amount" not in tx
    assert updated["final_amount"] == 98.0
