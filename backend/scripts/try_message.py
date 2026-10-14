"""Step 2: run one message through the full graph from your terminal.
Usage: python -m scripts.try_message "your message here"
"""
import sys

from graph.build import check_message

DEFAULT = ("USPS: Your package is on hold due to an unpaid $1.99 fee. "
           "Pay now to avoid return: http://usps-redelivery-help.top/pay")

print(check_message(sys.argv[1] if len(sys.argv) > 1 else DEFAULT))
