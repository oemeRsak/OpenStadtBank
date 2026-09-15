# SPDX-FileCopyrightText: Copyright (C) 2026 Ömer Rasim Sak <contact@oemersak.me>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import date

from django.shortcuts import render


def dashboard(request):
    return render(request, "dashboard.html", {
        "today": date.today(),
        "stats": {
            "young_citizens": 12482,
            "total_balance": 4892100,
            "active_projects": 42,
            "transactions_today": 894,
        },
        "activities": [
            {
                "title": "Deposit: City Park Fund",
                "subtitle": "Today, 10:42 AM",
                "amount": 1250,
                "status": "Success",
            },
            {
                "title": "Withdrawal: Playground Maintenance",
                "subtitle": "Yesterday",
                "amount": -4800,
                "status": "Completed",
            },
        ]
    })


def modern_template(request, template_name):
    return render(request, f"modern/{template_name}.html")


def modern_dashboard(request):
    return modern_template(request, "dasboard")


def modern_customers(request):
    return modern_template(request, "customer")


def modern_credit(request):
    return modern_template(request, "credit")


def modern_login(request):
    return modern_template(request, "login")


def modern_payment(request):
    return modern_template(request, "payment")


def modern_settings(request):
    return modern_template(request, "settings")