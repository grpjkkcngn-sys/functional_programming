from __future__ import annotations

from typing import Dict, List

from core import (
    CommissionFn,
    MinAmountFilterFn,
    ProcessingSummary,
    RateFn,
    Transaction,
    make_transaction_processor,
)


def build_uah_converter(rates: Dict[str, float]) -> RateFn:
    def convert(amount: float, currency: str) -> float:
        rate = rates.get(currency.upper(), 1.0)
        return amount * rate

    return convert


def build_commission_policy(fee_percent: float, flat_fee: float) -> CommissionFn:
    def commission(amount: float, tx_type: str) -> float:
        base = amount * fee_percent
        return base + flat_fee if tx_type == "international" else base

    return commission


def build_min_amount_filter(min_uah: float) -> MinAmountFilterFn:
    def accept(amount: float) -> bool:
        return amount >= min_uah

    return accept


def render_report(summary: ProcessingSummary) -> None:
    print("=== Звіт по успішних банківських транзакціях ===")
    for tx in summary["transactions"]:
        print(
            f"ID #{tx['id']} [{tx['tx_type']}]: "
            f"{tx['amount']} {tx['currency']} -> {tx['converted_amount']} UAH "
            f"(комісія: {tx['commission']} UAH, підсумок: {tx['final_amount']} UAH)"
        )
    print(f"Оброблено транзакцій: {summary['count']}")
    print(f"Загальний обсяг (після комісії): {summary['total_volume']} UAH")
    print(f"Сумарна комісія банку: {summary['total_commission']} UAH")


def main() -> None:
    sample_transactions: List[Transaction] = [
        {
            "id": 101,
            "tx_type": "card",
            "amount": 150.0,
            "currency": "USD",
            "status": "success",
        },
        {
            "id": 102,
            "tx_type": "transfer",
            "amount": 40.0,
            "currency": "EUR",
            "status": "failed",
        },
        {
            "id": 103,
            "tx_type": "international",
            "amount": 300.0,
            "currency": "EUR",
            "status": "success",
        },
        {
            "id": 104,
            "tx_type": "card",
            "amount": 500.0,
            "currency": "UAH",
            "status": "success",
        },
        {
            "id": 105,
            "tx_type": "transfer",
            "amount": 2500.0,
            "currency": "UAH",
            "status": "success",
        },
    ]

    rates = {"UAH": 1.0, "USD": 41.5, "EUR": 45.0}
    processor = make_transaction_processor(
        convert_currency=build_uah_converter(rates),
        calc_commission=build_commission_policy(fee_percent=0.015, flat_fee=25.0),
        accept_amount=build_min_amount_filter(1000.0),
    )

    result = processor(sample_transactions)
    render_report(result)


if __name__ == "__main__":
    main()
