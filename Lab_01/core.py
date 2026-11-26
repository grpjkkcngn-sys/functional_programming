from __future__ import annotations

from typing import Callable, Iterable, List, Optional, TypedDict


class BaseTransaction(TypedDict):
    id: int
    tx_type: str
    amount: float
    currency: str
    status: str


class Transaction(BaseTransaction, total=False):
    converted_amount: float
    commission: float
    final_amount: float


class ProcessedTransaction(BaseTransaction):
    converted_amount: float
    commission: float
    final_amount: float


class ProcessingSummary(TypedDict):
    count: int
    total_volume: float
    total_commission: float
    transactions: List[ProcessedTransaction]


RateFn = Callable[[float, str], float]
CommissionFn = Callable[[float, str], float]
MinAmountFilterFn = Callable[[float], bool]
ProcessorFn = Callable[[Iterable[Transaction]], ProcessingSummary]


def is_successful(tx: Transaction) -> bool:
    return tx["status"].strip().lower() == "success"


def calc_final_amount(converted: float, commission: float) -> float:
    return round(converted - commission, 2)


def with_calculated_fields(
    tx: Transaction,
    *,
    converted: float,
    commission: float,
    final: float,
) -> ProcessedTransaction:
    return {
        "id": tx["id"],
        "tx_type": tx["tx_type"],
        "amount": tx["amount"],
        "currency": tx["currency"],
        "status": tx["status"],
        "converted_amount": round(converted, 2),
        "commission": round(commission, 2),
        "final_amount": round(final, 2),
    }


def evaluate_transaction(
    tx: Transaction,
    *,
    convert_currency: RateFn,
    calc_commission: CommissionFn,
    accept_amount: MinAmountFilterFn,
) -> Optional[ProcessedTransaction]:
    if not is_successful(tx):
        return None

    converted = round(convert_currency(tx["amount"], tx["currency"]), 2)
    if not accept_amount(converted):
        return None

    commission = round(calc_commission(converted, tx["tx_type"]), 2)
    final = calc_final_amount(converted, commission)

    return with_calculated_fields(
        tx,
        converted=converted,
        commission=commission,
        final=final,
    )


def summarize_transactions(
    transactions: Iterable[ProcessedTransaction],
) -> ProcessingSummary:
    items = list(transactions)
    total_volume = round(sum(tx["final_amount"] for tx in items), 2)
    total_commission = round(sum(tx["commission"] for tx in items), 2)
    return {
        "count": len(items),
        "total_volume": total_volume,
        "total_commission": total_commission,
        "transactions": items,
    }


def make_transaction_processor(
    *,
    convert_currency: RateFn,
    calc_commission: CommissionFn,
    accept_amount: MinAmountFilterFn,
) -> ProcessorFn:
    def process(transactions: Iterable[Transaction]) -> ProcessingSummary:
        processed: List[ProcessedTransaction] = []
        for tx in transactions:
            evaluated = evaluate_transaction(
                tx,
                convert_currency=convert_currency,
                calc_commission=calc_commission,
                accept_amount=accept_amount,
            )
            if evaluated is not None:
                processed.append(evaluated)
        return summarize_transactions(processed)

    return process
