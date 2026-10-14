"""The shared state passed between graph nodes. This is the contract
between the backend and frontend, so agree on changes together."""
from typing import TypedDict


class GuardianState(TypedDict, total=False):
    message: str         # the suspicious message (untrusted!)
    entities: dict       # urls, phones, emails, claimed_brand, red_flags
    link_results: list   # from the link investigator
    research_results: list  # from the Tavily investigator
    verdict: dict        # verdict, risk, scam_type, reasons, sources
    reply: str           # final text sent back to the user
