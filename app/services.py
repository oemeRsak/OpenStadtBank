# SPDX-FileCopyrightText: Copyright (C) 2026 Ömer Rasim Sak <contact@oemersak.me>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Business operations for bank accounts."""

from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import BankAccount, Transaction


@transaction.atomic
def perform_transaction(account_id, amount, txn_type, authorization, description=""):
    """Apply a deposit or withdrawal and record its atomic result."""
    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValidationError("Amount must be a valid decimal value.") from exc

    if amount <= 0:
        raise ValidationError("Amount must be greater than zero.")
    if txn_type not in Transaction.Type.values:
        raise ValidationError("Transaction type is invalid.")

    account = BankAccount.objects.select_for_update().get(id=account_id)
    if not account.is_active or account.status != BankAccount.Status.ACTIVE:
        raise ValidationError("Account is not active.")

    balance_before = account.balance
    if txn_type == Transaction.Type.WITHDRAWAL:
        if balance_before < amount:
            raise ValidationError("Insufficient funds.")
        balance_after = balance_before - amount
    else:
        balance_after = balance_before + amount

    account.balance = balance_after
    account.save(update_fields=["balance", "updated_at"])

    return Transaction.objects.create(
        account=account,
        transaction_type=txn_type,
        amount=amount,
        balance_before=balance_before,
        balance_after=balance_after,
        authorization=authorization,
        description=description,
        status=Transaction.Status.SUCCESS,
    )
