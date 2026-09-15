# SPDX-FileCopyrightText: Copyright (C) 2026 Ömer Rasim Sak <contact@oemersak.me>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BankAccount, Transaction
from .services import perform_transaction


class TransactionServiceTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", password="password")
        self.authorizer = User.objects.create_user("authorizer", password="password")
        self.account = BankAccount.objects.create(
            user=self.owner,
            account_number="10000001",
            balance=Decimal("100.00"),
        )

    def test_deposit_updates_balance_and_records_transaction(self):
        transaction = perform_transaction(
            self.account.id,
            Decimal("25.50"),
            Transaction.Type.DEPOSIT,
            self.authorizer,
        )

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("125.50"))
        self.assertEqual(transaction.balance_before, Decimal("100.00"))
        self.assertEqual(transaction.balance_after, Decimal("125.50"))
        self.assertEqual(transaction.status, Transaction.Status.SUCCESS)

    def test_withdrawal_updates_balance_and_records_transaction(self):
        transaction = perform_transaction(
            self.account.id,
            Decimal("25.50"),
            Transaction.Type.WITHDRAWAL,
            self.authorizer,
        )

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("74.50"))
        self.assertEqual(transaction.transaction_type, Transaction.Type.WITHDRAWAL)

    def test_withdrawal_rejects_insufficient_funds_without_recording(self):
        with self.assertRaisesMessage(ValidationError, "Insufficient funds."):
            perform_transaction(
                self.account.id,
                Decimal("100.01"),
                Transaction.Type.WITHDRAWAL,
                self.authorizer,
            )

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("100.00"))
        self.assertFalse(Transaction.objects.exists())

    def test_invalid_amount_is_rejected(self):
        with self.assertRaisesMessage(ValidationError, "Amount must be greater than zero."):
            perform_transaction(
                self.account.id,
                Decimal("0.00"),
                Transaction.Type.DEPOSIT,
                self.authorizer,
            )


class PageRouteTests(TestCase):
    def test_dashboard_renders(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Total Young Citizens")

    def test_modern_pages_render(self):
        for route_name in (
            "modern-dashboard",
            "modern-customers",
            "modern-credit",
            "modern-login",
            "modern-payment",
            "modern-settings",
        ):
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
