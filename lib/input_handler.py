import argparse
from datetime import datetime
import dateparser

def _to_zoho_date_format(date_string: str):
    """Parses a date string and converts it to Zoho's required format."""
    dt = dateparser.parse(date_string)
    
    # Zoho expects ISO 8601 with Z (UTC)
    # strftime creates the required 2016-06-21T16:16:16.000Z format
    return dt.strftime('%Y-%m-%dT%H:%M:%S.000Z') if dt else None

def get_args():
    parser = argparse.ArgumentParser(description="Eliezer Ticket Report Generator")
    parser.add_argument("-N", "--new", action="store_true", help="Request New data from api")
    parser.add_argument("-s", "--status", required=True, help="Ticket status: [open or closed]")
    parser.add_argument("-f", "--from_date", required=True, help="Start date (e.g., 1 mar 2025, 01/03/25)")
    parser.add_argument("-t", "--to_date", default=datetime.now().strftime("%d %b %Y"), help="End date (default: today)")

    args = parser.parse_args()

    args.status = args.status.strip().lower()
    if args.status not in {"open", "closed"}:
        parser.error("Status must either 'open or closed'")

    # Use dateparser to handle flexible formats automatically
    args.from_date = _to_zoho_date_format(args.from_date)
    args.to_date = _to_zoho_date_format(args.to_date)

    if not args.from_date or not args.to_date:
        parser.error("Could not parse date format. Use formats like '1 Mar 2025' or '01/03/25'.")
    
    return args
