# GST Invoice Cash-Flow Forecaster

**AI-powered tool for Indian MSMEs to analyze GST invoices, identify delayed receivables, and forecast short-term cash flow.**

Built for founders and finance teams at small and medium enterprises who struggle with irregular payments, GST compliance, and working capital gaps.

## Problem

Indian MSMEs frequently face:
- Delayed payments from buyers (often 45–90+ days)
- Poor visibility into upcoming cash inflows from outstanding invoices
- Difficulty estimating working capital needs ahead of GST filing or payroll
- Manual reconciliation of GST invoices with UPI/bank receipts

This leads to unnecessary borrowing, missed opportunities, and cash-flow stress.

## Solution

This repository provides a simple, practical starter for an AI-assisted cash-flow system:

1. **Parse GST invoices** (structured or semi-structured data)
2. **Flag overdue and aging receivables**
3. **Forecast next 30/60/90-day cash inflows** based on historical payment patterns
4. **Estimate working capital gap** against fixed outflows (rent, salaries, GST, suppliers)
5. **Highlight priority follow-ups** for collections

The included Python script demonstrates core logic with sample data and clear comments so you can extend it with real GST exports, UPI statements, or LLM-based invoice extraction.

## Quick Start

```bash
git clone https://github.com/ShihaiSuru/gst-invoice-cashflow-forecaster-2026-10-18.git
cd gst-invoice-cashflow-forecaster-2026-10-18
python3 cashflow_forecaster.py
```

### Requirements
- Python 3.8+
- No external dependencies for the starter script (uses only standard library)

## Usage

1. Replace or extend the sample invoice data in `cashflow_forecaster.py` with your GST invoice export (CSV/JSON from GST portal, Tally, or accounting software).
2. Run the script to generate:
   - Aging report (0–30, 31–60, 61–90, 90+ days)
   - Forecasted cash inflow for the next 30/60/90 days
   - Estimated working capital requirement
3. Integrate with bank/UPI statements for reconciliation (future enhancement).

## Sample Output

```
=== GST Invoice Cash-Flow Forecast ===

Aging Summary:
  0-30 days   : ₹1,25,000 (2 invoices)
  31-60 days  : ₹80,000 (1 invoice)
  61-90 days  : ₹45,000 (1 invoice)
  90+ days    : ₹20,000 (1 invoice)

Forecasted Inflows (next 30 days): ₹1,05,000
Forecasted Inflows (next 60 days): ₹1,85,000
Estimated Working Capital Gap     : ₹62,000

Priority Collections:
  - INV-2026-0142 (Buyer: ABC Traders) — 78 days overdue, ₹45,000
```

## Roadmap

- [ ] CSV/JSON GST invoice importer
- [ ] UPI statement reconciler
- [ ] LLM-based free-text invoice parser (using local or API models)
- [ ] Simple dashboard (Streamlit or Gradio)
- [ ] Integration with Tally / Zoho Books exports
- [ ] GST filing reminder + cash-flow impact calculator

## Why This Matters for MSMEs

Better cash-flow visibility directly improves survival rates, reduces reliance on expensive short-term credit, and helps founders make informed decisions about hiring, inventory, and growth.

## License

MIT — free for commercial and personal use by MSMEs and builders.

---

*Part of practical fintech tools focused on AI cash-flow systems for Indian MSMEs.*
