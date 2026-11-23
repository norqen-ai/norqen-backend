"""Expanded research universe for the PIT study (frozen 12 Oct 2026).

CORE_40 is the original pre-registered universe (config/universe.json, frozen 6 Aug 2026)
and is always reported as a subset. EXT adds 30 US mega/large caps and 30 NSE large caps (NIFTY-50 members)
with continuous Yahoo history over 2022-09..2026-10. Membership is
today's large caps, so the sample carries survivorship bias (stated in the paper).
"""
from __future__ import annotations

import json
from pathlib import Path

_CFG = json.loads((Path(__file__).resolve().parents[2] / "config" / "universe.json").read_text())
CORE_US: list[str] = _CFG["US"]
CORE_NSE: list[str] = _CFG["NSE"]

EXT_US = ["AVGO", "LLY", "COST", "ORCL", "NFLX", "CRM", "ABBV", "MRK", "CVX", "ADBE",
          "AMD", "CSCO", "TMO", "ABT", "MCD", "ACN", "INTC", "QCOM", "TXN", "IBM",
          "GS", "MS", "CAT", "HON", "NKE", "PFE", "T", "VZ", "CMCSA", "LIN"]

EXT_NSE = ["ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS",
           "BEL.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS",
           "GRASIM.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "INDUSINDBK.NS",
           "JSWSTEEL.NS", "M&M.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
           "POWERGRID.NS", "SBILIFE.NS", "SHRIRAMFIN.NS", "TATACONSUM.NS", "TATASTEEL.NS",
           "TECHM.NS", "TRENT.NS", "BRITANNIA.NS", "DIVISLAB.NS", "BPCL.NS"]

US = CORE_US + EXT_US
NSE = CORE_NSE + list(dict.fromkeys(EXT_NSE))
CORE_40 = set(CORE_US + CORE_NSE)
INDEX = {"US": "^GSPC", "IN": "^NSEI"}


def region(ticker: str) -> str:
    return "IN" if ticker.upper().endswith(".NS") else "US"


def all_tickers() -> list[str]:
    return list(dict.fromkeys(US + NSE))
