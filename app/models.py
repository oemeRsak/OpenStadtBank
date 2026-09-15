# SPDX-FileCopyrightText: Copyright (C) 2026 Ömer Rasim Sak <contact@oemersak.me>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import uuid
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class BankAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        DELETED = "DELETED", "Deleted"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_accounts")
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.user.username}"


class Transaction(models.Model):
    class Type(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        REJECTED = "REJECTED", "Rejected"
        SUCCESS = "SUCCESS", "Success"
        REVERSED = "REVERSED", "Reversed"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(
        BankAccount,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    transaction_type = models.CharField(max_length=10, choices=Type.choices)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    authorization = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authorized_transactions",
    )
    reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.account.account_number} - {self.amount}"
