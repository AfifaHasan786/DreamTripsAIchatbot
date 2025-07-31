import json

def lambda_handler(event, context):
    try:
        intent_name = event['sessionState']['intent']['name']
        
        # Get slot values
        slots = event['sessionState']['intent']['slots']
        
        def get_slot(slot_name):
            slot = slots.get(slot_name)
            if slot and 'value' in slot:
                return slot['value'].get('interpretedValue')
            return None
        
        room_type = get_slot('roomType')
        num_days = get_slot('numDays')
        check_in = get_slot('checkInDate')
        num_guests = get_slot('numGuests')
        name = get_slot('customerName')
        
        # Fallback defaults
        room_type = room_type if room_type else "a room"
        num_days = num_days if num_days else "some"
        check_in = check_in if check_in else "an unspecified date"
        num_guests = num_guests if num_guests else "some"
        name = name if name else "Guest"

        # Optional pricing
        room_prices = {
            "Classic": 2000,
            "Deluxe": 3000,
            "Suite": 5000
        }
        price_per_day = room_prices.get(room_type, 2000)
        total_price = price_per_day * int(num_days) if num_days and num_days.isdigit() else "Unknown"

        # Confirmation message
        message = f"Booking confirmed! {name}, you've booked a {room_type} room for {num_days} days starting {check_in} for {num_guests} guest(s)."
        if isinstance(total_price, int):
            message += f" Total cost: ₹{total_price}."

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent_name,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": message
                }
            ]
        }

    except Exception as e:
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": event['sessionState']['intent']['name'],
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Something went wrong while processing your request. Please try again later."
                }
            ]
        }


