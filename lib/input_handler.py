import argparse
from datetime import datetime
import dateparser

def get_args():
    parser = argparse.ArgumentParser(description="Eliezer Ticket Report Generator")
    parser.add_argument("-s", "--status", required=True, help="Ticket status: [open or closed]")
    parser.add_argument("-f", "--from_date", required=True, help="Start date (e.g., 1 mar 2025, 01/03/25)")
    parser.add_argument("-t", "--to_date", default=datetime.now().strftime("%d %b %Y"), help="End date (default: today)")

    args = parser.parse_args()

    args.status = args.status.strip().lower()
    if args.status not in {"open", "closed"}:
        parser.error("Status must either be 'open or closed'")

    # Use dateparser to handle flexible formats automatically
    args.from_date = dateparser.parse(args.from_date)
    args.to_date = dateparser.parse(args.to_date)

    if not args.from_date or not args.to_date:
        parser.error("Could not parse date format. Use formats like '1 Mar 2025' or '01/03/25'.")
    
    return args

if __name__ == "__main__":
    args = get_args()
    print(f"Fetching tickets with status: {args.status}")
    print(f"Date range: {args.from_date.strftime('%Y-%m-%d')} to {args.to_date.strftime('%Y-%m-%d')}")