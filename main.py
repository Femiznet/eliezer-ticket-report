from lib import (
    process_tickets , convert_to_excel,
    fetch_data_with_args, get_args,
    OWNERS
    )

def main():
    # get user inputs via cli
    args = get_args()

    # fetch data with those inputs (Zoho_api)
    print("Fetching data...")
    data = fetch_data_with_args(args)

    # process data and get tickets by allowed owners
    allowed_owners = set(owner.strip() for owner in OWNERS.split(","))
    print(allowed_owners)

    print("Processing tickets...")
    processed_tickets = process_tickets(data, allowed_owners)

    # convert to excel
    print("Generating excel...")
    ownerFiles = convert_to_excel(processed_tickets, args)

    for owner in ownerFiles:
        print(f"Owner:{owner} file was saved to {ownerFiles[owner]}")


main()