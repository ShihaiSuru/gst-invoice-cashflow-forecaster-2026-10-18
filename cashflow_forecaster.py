#!/usr/bin/env python3
"""
GST Invoice Cash-Flow Forecaster
Starter tool for Indian MSMEs

Analyzes sample GST invoices to produce aging reports,
cash-flow forecasts, and working capital estimates.

No external dependencies — pure Python standard library.
"""

from datetime import datetime, timedelta
from typing import List, Dict
import json


# ---------------------------------------------------------------------------
# Sample GST Invoice Data (replace with real exports from GST portal / Tally)
# ---------------------------------------------------------------------------
SAMPLE_INVOICES = [
    {
        "invoice_no": "INV-2026-0101",
        "buyer": "ABC Traders",
        "invoice_date": "2026-07-15",
        "due_date": "2026-08-14",
        "amount": 45000,
        "gst_amount": 8100,
        "status": "unpaid",
        "historical_avg_delay_days": 45,  # learned from past payments
    },
    {
        "invoice_no": "INV-2026-0128",
        "buyer": "XYZ Enterprises",
        "invoice_date": "2026-08-20",
        "due_date": "2026-09-19",
        "amount": 80000,
        "gst_amount": 14400,
        "status": "unpaid",
        "historical_avg_delay_days": 30,
    },
    {
        "invoice_no": "INV-2026-0142",
        "buyer": "PQR Suppliers",
        "invoice_date": "2026-09-01",
        "due_date": "2026-09-30",
        "amount": 125000,
        "gst_amount": 22500,
        "status": "unpaid",
        "historical_avg_delay_days": 20,
    },
    {
        "invoice_no": "INV-2026-0155",
        "buyer": "LMN Retail",
        "invoice_date": "2026-09-25",
        "due_date": "2026-10-25",
        "amount": 55000,
        "gst_amount": 9900,
        "status": "unpaid",
        "historical_avg_delay_days": 15,
    },
    {
        "invoice_no": "INV-2026-0089",
        "buyer": "Old Client Co",
        "invoice_date": "2026-06-10",
        "due_date": "2026-07-10",
        "amount": 20000,
        "gst_amount": 3600,
        "status": "unpaid",
        "historical_avg_delay_days": 90,
    },
]

# Fixed monthly outflows (customize for your MSME)
MONTHLY_OUTFLOWS = {
    "salaries": 80000,
    "rent": 25000,
    "suppliers_advance": 30000,
    "gst_payable_estimate": 15000,
    "other": 10000,
}


def parse_date(date_str: str) -> datetime:
    """Parse YYYY-MM-DD string to datetime."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def days_between(d1: datetime, d2: datetime) -> int:
    return (d2 - d1).days


def aging_bucket(days_overdue: int) -> str:
    if days_overdue <= 0:
        return "current"
    elif days_overdue <= 30:
        return "0-30"
    elif days_overdue <= 60:
        return "31-60"
    elif days_overdue <= 90:
        return "61-90"
    else:
        return "90+"


def forecast_payment_date(invoice: Dict, today: datetime) -> datetime:
    """
    Simple forecast: due_date + historical average delay.
    In a production system this would use ML or more buyer-specific history.
    """
    due = parse_date(invoice["due_date"])
    delay = invoice.get("historical_avg_delay_days", 30)
    return due + timedelta(days=delay)


def analyze_invoices(invoices: List[Dict], today: datetime = None) -> Dict:
    if today is None:
        today = datetime.now()

    aging = {"current": 0, "0-30": 0, "31-60": 0, "61-90": 0, "90+": 0}
    aging_count = {k: 0 for k in aging}
    forecasts = {30: 0, 60: 0, 90: 0}
    priority = []

    total_outstanding = 0

    for inv in invoices:
        if inv["status"] != "unpaid":
            continue

        amount = inv["amount"]
        total_outstanding += amount

        due = parse_date(inv["due_date"])
        days_overdue = days_between(due, today)
        bucket = aging_bucket(days_overdue)
        aging[bucket] += amount
        aging_count[bucket] += 1

        # Forecast inflow
        expected_pay = forecast_payment_date(inv, today)
        days_to_pay = days_between(today, expected_pay)

        if days_to_pay <= 30:
            forecasts[30] += amount
        if days_to_pay <= 60:
            forecasts[60] += amount
        if days_to_pay <= 90:
            forecasts[90] += amount

        # Priority if significantly overdue
        if days_overdue > 60:
            priority.append({
                "invoice_no": inv["invoice_no"],
                "buyer": inv["buyer"],
                "amount": amount,
                "days_overdue": days_overdue,
            })

    # Working capital gap (simple: next 30 days outflows minus forecasted inflows)
    monthly_outflow = sum(MONTHLY_OUTFLOWS.values())
    next_30_outflow = monthly_outflow  # assume monthly cycle
    working_capital_gap = max(0, next_30_outflow - forecasts[30])

    return {
        "today": today.strftime("%Y-%m-%d"),
        "total_outstanding": total_outstanding,
        "aging": aging,
        "aging_count": aging_count,
        "forecasts": forecasts,
        "working_capital_gap": working_capital_gap,
        "priority_collections": sorted(priority, key=lambda x: -x["days_overdue"]),
        "monthly_outflows": MONTHLY_OUTFLOWS,
    }


def print_report(result: Dict):
    print("=" * 50)
    print("GST Invoice Cash-Flow Forecast")
    print("=" * 50)
    print(f"As of: {result['today']}\n")

    print("Aging Summary (Outstanding Receivables):")
    for bucket in ["current", "0-30", "31-60", "61-90", "90+"]:
        amt = result["aging"][bucket]
        cnt = result["aging_count"][bucket]
        if amt > 0:
            print(f"  {bucket:10s}: ₹{amt:>10,} ({cnt} invoices)")

    print(f"\nTotal Outstanding: ₹{result['total_outstanding']:,}")

    print("\nForecasted Cash Inflows:")
    print(f"  Next 30 days : ₹{result['forecasts'][30]:,}")
    print(f"  Next 60 days : ₹{result['forecasts'][60]:,}")
    print(f"  Next 90 days : ₹{result['forecasts'][90]:,}")

    print(f"\nEstimated Working Capital Gap (next 30 days): ₹{result['working_capital_gap']:,}")

    if result["priority_collections"]:
        print("\nPriority Collections (60+ days overdue):")
        for p in result["priority_collections"]:
            print(f"  - {p['invoice_no']} ({p['buyer']}) — {p['days_overdue']} days overdue, ₹{p['amount']:,}")
    else:
        print("\nNo invoices currently 60+ days overdue.")

    print("\n" + "=" * 50)


def main():
    # Use a fixed "today" for reproducible demo output; remove for live use
    demo_today = datetime(2026, 10, 18)
    result = analyze_invoices(SAMPLE_INVOICES, today=demo_today)
    print_report(result)

    # Optional: export JSON for further processing
    with open("cashflow_report.json", "w") as f:
        # Convert datetime objects if any remain
        json.dump(result, f, indent=2, default=str)
    print("\nReport also saved to cashflow_report.json")


if __name__ == "__main__":
    main()
