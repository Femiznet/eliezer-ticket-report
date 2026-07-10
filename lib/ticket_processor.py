import json
from collections import defaultdict
from pydantic import ValidationError
from .ticket_model import TicketModel 
from bs4 import BeautifulSoup

def _clean_html(html_content: str) -> str:
    if not html_content:
        return ""
    return BeautifulSoup(html_content, "html.parser").get_text()

def process_tickets(tickets_data: list[dict], target_owners:set|None = None):
    
    # Assuming raw.json structure is a list of tickets
    grouped_tickets = defaultdict(list)
    
    for item in tickets_data:
        try:
            ticket = TicketModel.model_validate(item)
            owner = ticket.TicketOwner.lower() or "unassigned"

            if target_owners and owner not in target_owners:
                continue

            ticket.Description = _clean_html(ticket.Description)

            grouped_tickets[owner].append(ticket.model_dump())

        except ValidationError as e:
            print(f"Skipping ticket due to error: {e}")
            
    return dict(grouped_tickets)
