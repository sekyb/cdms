import argparse
import pymongo
import requests
from pymongo import MongoClient

def print_banner():
    banner = """
   .aMMMb  dMMMMb  dMMMMMMMMb  .dMMMb
  dMP"VMP dMP VMP dMP"dMP"dMP dMP" VP
 dMP     dMP dMP dMP dMP dMP  VMMMb
dMP.aMP dMP.aMP dMP dMP dMP dP .dMP
VMMMP" dMMMMP" dMP dMP dMP  VMMMP"
*------------------------------------*
       Copyright 2024 © Seth KB.
          Version 1.9


    """
    print(banner)

def connect_to_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cdms']
    return db

def get_scryfall_data(card_name):
    url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    response = requests.get(url)
    card = response.json()
    return {
        "name": card.get('name', 'N/A'),
        "mana_cost": card.get('mana_cost', 'N/A'),
        "type_line": card.get('type_line', 'N/A'),
        "oracle_text": card.get('oracle_text', 'N/A'),
        "power": card.get('power', 'N/A'),
        "toughness": card.get('toughness', 'N/A'),
        "loyalty": card.get('loyalty', 'N/A'),
        "rarity": card.get('rarity', 'N/A'),
        "set_name": card.get('set_name', 'N/A'),
        "image_url": card.get('image_uris', {}).get('normal', 'N/A'),
        "price": card.get('prices', {}).get('usd', 'N/A')
    }

def add_card(db, collection_id, card_name, quantity, foil=False, extended_art=False, etched=False, location="Trades"):
    cards = db.cards
    scryfall_data = get_scryfall_data(card_name)
    card = cards.find_one({"name": card_name, "location": location})
    
    if card:
        # Update existing card by combining quantities
        new_quantity = card.get("quantity", 0) + quantity
        cards.update_one({"name": card_name, "location": location}, {
            "$set": {
                "collection_id": collection_id,
                "foil": foil,
                "extended_art": extended_art,
                "etched": etched,
                "scryfall_data": scryfall_data
            },
            "$inc": {
                "quantity": quantity  # Increment the quantity
            }
        })
        print(f"Card '{card_name}' updated with new quantity ({new_quantity}) and location '{location}'.")
    else:
        # Add new card
        cards.insert_one({
            "collection_id": collection_id,
            "name": card_name,
            "quantity": quantity,
            "foil": foil,
            "extended_art": extended_art,
            "etched": etched,
            "location": location,
            "scryfall_data": scryfall_data
        })
        print(f"Card '{card_name}' added to the database at location '{location}'.")

def view_db(db, location=None):
    cards = db.cards
    query = {} if location is None else {"location": location}
    count = cards.count_documents(query)
    if count == 0:
        print(f"No cards found in the database for location '{location}'." if location else "No cards found in the database.")
    else:
        cursor = cards.find(query)
        for card in cursor:
            print(f"Name: {card.get('name', 'N/A')}")
            print(f"Quantity: {card.get('quantity', 'N/A')}")
            print(f"Foil: {card.get('foil', 'N/A')}")
            print(f"Extended Art: {card.get('extended_art', 'N/A')}")
            print(f"Etched: {card.get('etched', 'N/A')}")
            print(f"Location: {card.get('location', 'N/A')}")
            print("---")

def search_local(db, card_name):
    cards = db.cards
    card = cards.find_one({"name": card_name})
    if card:
        print(f"--- Local Card Details ---")
        print(f"Name: {card.get('name', 'N/A')}")
        print(f"Quantity: {card.get('quantity', 'N/A')}")
        print(f"Foil: {card.get('foil', 'N/A')}")
        print(f"Extended Art: {card.get('extended_art', 'N/A')}")
        print(f"Etched: {card.get('etched', 'N/A')}")
        print(f"Location: {card.get('location', 'N/A')}")
        
        # Display Scryfall data
        scryfall_data = card.get('scryfall_data', {})
        print(f"Mana Cost: {scryfall_data.get('mana_cost', 'N/A')}")
        print(f"Type Line: {scryfall_data.get('type_line', 'N/A')}")
        print(f"Oracle Text: {scryfall_data.get('oracle_text', 'N/A')}")
        print(f"Power: {scryfall_data.get('power', 'N/A')}")
        print(f"Toughness: {scryfall_data.get('toughness', 'N/A')}")
        print(f"Loyalty: {scryfall_data.get('loyalty', 'N/A')}")
        print(f"Rarity: {scryfall_data.get('rarity', 'N/A')}")
        print(f"Set Name: {scryfall_data.get('set_name', 'N/A')}")
        print(f"Image URL: {scryfall_data.get('image_url', 'N/A')}")
        print(f"Price: {scryfall_data.get('price', 'N/A')}")
    else:
        print(f"No card found with the name '{card_name}'.")

def search_scryfall(card_name):
    url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    response = requests.get(url)
    card = response.json()

    print("--- Scryfall Card Details ---")
    print(f"Name: {card.get('name', 'N/A')}")
    print(f"Mana Cost: {card.get('mana_cost', 'N/A')}")
    print(f"Type Line: {card.get('type_line', 'N/A')}")
    print(f"Oracle Text: {card.get('oracle_text', 'N/A')}")
    print(f"Power: {card.get('power', 'N/A')}")
    print(f"Toughness: {card.get('toughness', 'N/A')}")
    print(f"Loyalty: {card.get('loyalty', 'N/A')}")
    print(f"Rarity: {card.get('rarity', 'N/A')}")
    print(f"Set Name: {card.get('set_name', 'N/A')}")
    print(f"Image URL: {card.get('image_uris', {}).get('normal', 'N/A')}")
    print(f"Price: {card.get('prices', {}).get('usd', 'N/A')}")
    print(f"Details: {card.get('details', 'N/A')}")

def delete_card(db, card_name):
    cards = db.cards
    result = cards.delete_one({"name": card_name})
    if result.deleted_count > 0:
        print(f"Card '{card_name}' deleted from the database.")
    else:
        print(f"No card found with the name '{card_name}' to delete.")

def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description="CDMS - Card Database Management System",
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command')

    add_card_parser = subparsers.add_parser('add-card', help='Add or update a card in the database')
    add_card_parser.add_argument('--id', type=int, required=True, help='ID of the collection')
    add_card_parser.add_argument('--n', type=str, required=True, help='Name of the card')
    add_card_parser.add_argument('--quantity', type=int, required=True, help='Quantity of the card')
    add_card_parser.add_argument('--foil', action='store_true', help='Card is foil')
    add_card_parser.add_argument('--extended_art', action='store_true', help='Card has extended art')
    add_card_parser.add_argument('--etched', action='store_true', help='Card is etched')
    add_card_parser.add_argument('--location', type=str, default="Trades", help='Location of the card (Trades, Selling, Mass-Stock, Rares)')
    add_card_parser.set_defaults(func=lambda args: add_card(connect_to_db(), args.id, args.n, args.quantity, args.foil, args.extended_art, args.etched, args.location))

    view_db_parser = subparsers.add_parser('view-db', help='View all cards in the database')
    view_db_parser.add_argument('--location', type=str, help='Filter by location (optional)')
    view_db_parser.set_defaults(func=lambda args: view_db(connect_to_db(), args.location))

    search_local_parser = subparsers.add_parser('search-local', help='Search for a card in the local database')
    search_local_parser.add_argument('--n', type=str, required=True, help='Name of the card')
    search_local_parser.set_defaults(func=lambda args: search_local(connect_to_db(), args.n))

    search_scryfall_parser = subparsers.add_parser('search-scryfall', help='Search for a card on Scryfall')
    search_scryfall_parser.add_argument('--n', type=str, required=True, help='Name of the card')
    search_scryfall_parser.set_defaults(func=lambda args: search_scryfall(args.n))

    delete_card_parser = subparsers.add_parser('delete-card', help='Delete a card from the database')
    delete_card_parser.add_argument('--n', type=str, required=True, help='Name of the card')
    delete_card_parser.set_defaults(func=lambda args: delete_card(connect_to_db(), args.n))

    help_parser = subparsers.add_parser('help', help='Show help message')
    help_parser.set_defaults(func=lambda args: parser.print_help())

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
