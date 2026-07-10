# Eliezer FM Ticket Report Generator

A lightweight tool to extract tickets from Zoho Desk and export them to Excel for reporting.

## 🚀 Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/Femiznet/eliezer-ticket-report
```

**2. Install requirements**
```bash
pip install -r requirements.txt
```

**3. Run the script**
```bash
python main.py --from_date "1 March 2025" --to_date "31 March 2025"

# NOTE: Use --help for more info
```

**4. Make a new api request**
```bash
# To fetch new data, add the -N or --new arg to the script

python main.py --from_date "1 March 2025" --to_date "31 March 2025" --new
```

## 📂 Project Flow

1. **Authentication** — Uses OAuth tokens to securely connect to Zoho Desk.
2. **Extraction** — Fetches ticket data within the specified date range.
3. **Processing** — Cleans and formats data for analysis.
4. **Export** — Generates an Excel report for easy viewing.

## ⚙️ Configuration

- Ensure your `config.py` and `.env` contain the required `ORG_ID` and API credentials.
- Logs are stored in `logs/error.log` for easy debugging.
