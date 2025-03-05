from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

# models/flight.py
class Flight:
    def __init__(self, flight_number: str, origin: 'Airport', destination: 'Airport',
                 departure_time: datetime, arrival_time: datetime):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.seats: Dict[str, bool] = self._initialize_seats()
        
    def _initialize_seats(self) -> Dict[str, bool]:
        seats = {}
        for row in range(1, 31):
            for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
                seat_number = f"{row}{letter}"
                seats[seat_number] = True  # True means available
        return seats
    
    def is_seat_available(self, seat_number: str) -> bool:
        return self.seats.get(seat_number, False)
    
    def book_seat(self, seat_number: str) -> bool:
        if self.is_seat_available(seat_number):
            self.seats[seat_number] = False
            return True
        return False
    
    def get_available_seats(self) -> List[str]:
        return [seat for seat, available in self.seats.items() if available]

# models/passenger.py
class Passenger:
    def __init__(self, passenger_id: str, name: str, email: str, phone: str):
        self.passenger_id = passenger_id
        self.name = name
        self.email = email
        self.phone = phone
        self.tickets: List['Ticket'] = []
    
    def add_ticket(self, ticket: 'Ticket') -> None:
        self.tickets.append(ticket)
    
    def get_booking_history(self) -> List['Ticket']:
        return self.tickets.copy()

# models/airport.py
class Airport:
    def __init__(self, code: str, name: str, city: str, country: str):
        self.code = code
        self.name = name
        self.city = city
        self.country = country

# models/payment.py
class PaymentStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Payment:
    def __init__(self, amount: float, payment_method: str):
        self.amount = amount
        self.payment_method = payment_method
        self.status = PaymentStatus.PENDING
        self.timestamp = datetime.now()
    
    def process(self) -> bool:
        # Simulate payment processing
        self.status = PaymentStatus.COMPLETED
        return True

# models/ticket.py
class Ticket:
    def __init__(self, ticket_number: str, flight: 'Flight', 
                 passenger: 'Passenger', seat_number: str, payment: 'Payment'):
        self.ticket_number = ticket_number
        self.flight = flight
        self.passenger = passenger
        self.seat_number = seat_number
        self.payment = payment
        self.status = "CONFIRMED" if payment.status == PaymentStatus.COMPLETED else "PENDING"
    
    def get_details(self) -> dict:
        return {
            "ticket_number": self.ticket_number,
            "passenger_name": self.passenger.name,
            "flight_number": self.flight.flight_number,
            "from": self.flight.origin.city,
            "to": self.flight.destination.city,
            "departure_time": self.flight.departure_time,
            "seat_number": self.seat_number,
            "status": self.status
        }

# managers/flight_manager.py
class FlightManager:
    def __init__(self):
        self.flights: Dict[str, 'Flight'] = {}
        self.passengers: Dict[str, 'Passenger'] = {}
        self.tickets: Dict[str, 'Ticket'] = {}
    
    def add_flight(self, flight: 'Flight') -> None:
        self.flights[flight.flight_number] = flight
    
    def add_passenger(self, passenger: 'Passenger') -> None:
        self.passengers[passenger.passenger_id] = passenger
    
    def search_flights(self, origin_city: str, destination_city: str) -> List['Flight']:
        return [
            flight for flight in self.flights.values()
            if flight.origin.city.lower() == origin_city.lower()
            and flight.destination.city.lower() == destination_city.lower()
        ]
    
    def book_flight(self, passenger_id: str, flight_number: str, 
                   seat_number: str, payment_method: str) -> Optional['Ticket']:
        passenger = self.passengers.get(passenger_id)
        flight = self.flights.get(flight_number)
        
        if not passenger or not flight:
            return None
        
        if not flight.is_seat_available(seat_number):
            return None
        
        # Process payment
        payment = Payment(200.0, payment_method)  # Simple fixed price
        if payment.process():
            # Book seat
            if flight.book_seat(seat_number):
                # Create ticket
                ticket_number = f"TKT{len(self.tickets) + 1}"
                ticket = Ticket(ticket_number, flight, passenger, seat_number, payment)
                self.tickets[ticket_number] = ticket
                passenger.add_ticket(ticket)
                return ticket
        
        return None

# interactive_booking.py
import time

class InteractiveBooking:
    def __init__(self, flight_manager: 'FlightManager'):
        self.manager = flight_manager
        self.current_passenger: Optional['Passenger'] = None
        self.selected_flight: Optional['Flight'] = None
        
    def clear_screen(self):
        print("\n" * 50)
        
    def display_welcome(self):
        print("=" * 50)
        print("Welcome to the Flight Booking System")
        print("=" * 50)
        print("\nWe'll guide you through the booking process step by step.")
        time.sleep(1)
        
    def get_user_input(self, prompt: str, valid_options: Optional[List] = None) -> str:
        while True:
            response = input(f"\n{prompt}: ").strip()
            if not valid_options or response.upper() in valid_options:
                return response
            print(f"Please enter a valid option from: {', '.join(valid_options)}")
            
    def collect_passenger_info(self):
        print("\nFirst, we need some information about you.")
        name = self.get_user_input("What is your full name?")
        email = self.get_user_input("What is your email address?")
        phone = self.get_user_input("What is your phone number?")
        
        passenger_id = f"P{len(self.manager.passengers) + 1}"
        self.current_passenger = Passenger(passenger_id, name, email, phone)
        self.manager.add_passenger(self.current_passenger)
        
        print("\nThank you for providing your information!")
        time.sleep(1)
        
    def search_flights(self):
        print("\nLet's find a flight for you.")
        origin = self.get_user_input("Which city are you departing from?")
        destination = self.get_user_input("Which city are you traveling to?")
        
        available_flights = self.manager.search_flights(origin, destination)
        
        if not available_flights:
            print("\nSorry, no flights found for this route.")
            return False
            
        print("\nAvailable Flights:")
        for i, flight in enumerate(available_flights, 1):
            print(f"\nFlight {i}:")
            print(f"  Flight Number: {flight.flight_number}")
            print(f"  From: {flight.origin.city} ({flight.origin.code})")
            print(f"  To: {flight.destination.city} ({flight.destination.code})")
            print(f"  Departure: {flight.departure_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Arrival: {flight.arrival_time.strftime('%Y-%m-%d %H:%M')}")
            
        choice = int(self.get_user_input(
            "Please enter the flight number (1, 2, etc.)",
            [str(i) for i in range(1, len(available_flights) + 1)]
        ))
        
        self.selected_flight = available_flights[choice - 1]
        return True
        
    def select_seat(self) -> Optional[str]:
        print("\nLet's select your seat.")
        available_seats = self.selected_flight.get_available_seats()
        
        if not available_seats:
            print("Sorry, no seats available on this flight.")
            return None
            
        print("\nAvailable Seats:")
        seats_per_row = 6
        current_row = ""
        current_row_num = -1
        
        for seat in sorted(available_seats):
            row_num = int(seat[:-1])
            if row_num != current_row_num:
                if current_row:
                    print(current_row)
                current_row = f"\nRow {row_num:2d}: "
                current_row_num = row_num
            current_row += f"{seat[-1]} "
            
        if current_row:
            print(current_row)
            
        while True:
            seat_choice = self.get_user_input("\nPlease enter your desired seat (e.g., 12A)")
            if seat_choice in available_seats:
                return seat_choice
            print("That seat is not available. Please choose from the available seats.")
            
    def process_payment(self) -> Optional['Payment']:
        print("\nTime to process your payment.")
        print("Available payment methods:")
        print("1. Credit Card")
        print("2. Debit Card")
        print("3. PayPal")
        
        payment_methods = {"1": "credit_card", "2": "debit_card", "3": "paypal"}
        choice = self.get_user_input(
            "Please select your payment method (1-3)",
            ["1", "2", "3"]
        )
        
        payment = Payment(200.0, payment_methods[choice])
        if payment.process():
            print("\nPayment processed successfully!")
            return payment
        print("\nPayment processing failed. Please try again.")
        return None
        
    def display_booking_confirmation(self, ticket: 'Ticket'):
        self.clear_screen()
        print("\n" + "=" * 50)
        print("Booking Confirmation")
        print("=" * 50)

        details = ticket.get_details()
        print(f"\nTicket Number: {details['ticket_number']}")
        print(f"Passenger Name: {details['passenger_name']}")
        print(f"Flight Number: {details['flight_number']}")
        print(f"From: {details['from']}")
        print(f"To: {details['to']}")
        print(f"Departure Time: {details['departure_time'].strftime('%Y-%m-%d %H:%M')}")
        print(f"Arrival Time: {ticket.flight.arrival_time.strftime('%Y-%m-%d %H:%M')}")  # Add arrival time
        print(f"Seat Number: {details['seat_number']}")
        print(f"Status: {details['status']}")
        print("\nThank you for booking with us!")   

        
    def run_booking_process(self):
        self.clear_screen()
        self.display_welcome()
        
        # Collect passenger information
        self.collect_passenger_info()
        
        # Search and select flight
        if not self.search_flights():
            print("\nSorry, we couldn't proceed with the booking.")
            return
            
        # Select seat
        seat = self.select_seat()
        if not seat:
            print("\nSorry, we couldn't proceed with the booking.")
            return
            
        # Process payment
        payment = self.process_payment()
        if not payment:
            print("\nSorry, we couldn't proceed with the booking.")
            return
            
        # Create ticket
        ticket = self.manager.book_flight(
            self.current_passenger.passenger_id,
            self.selected_flight.flight_number,
            seat,
            payment.payment_method
        )
        
        if ticket:
            self.display_booking_confirmation(ticket)
        else:
            print("\nSorry, there was an error processing your booking.")

def main():
    # Create airports
    jfk = Airport("JFK", "John F Kennedy", "New York", "USA")
    lhr = Airport("LHR", "Heathrow", "London", "UK")
    cdg = Airport("CDG", "Charles de Gaulle", "Paris", "France")
    dxb = Airport("DXB", "Dubai International", "Dubai", "UAE")
    sin = Airport("SIN", "Changi", "Singapore", "Singapore")
    
    # Create sample flights
    flights = [
        Flight("FL101", jfk, lhr, datetime(2024, 11, 5, 10, 0), datetime(2024, 11, 5, 22, 0)),
        Flight("FL102", lhr, cdg, datetime(2024, 11, 5, 14, 0), datetime(2024, 11, 5, 16, 0)),
        Flight("FL103", jfk, cdg, datetime(2024, 11, 5, 11, 0), datetime(2024, 11, 5, 23, 0)),
        Flight("FL104", cdg, dxb, datetime(2024, 11, 6, 9, 0), datetime(2024, 11, 6, 18, 0)),
        Flight("FL105", dxb, sin, datetime(2024, 11, 6, 22, 0), datetime(2024, 11, 7, 10, 0)),
        Flight("FL106", lhr, dxb, datetime(2024, 11, 5, 20, 0), datetime(2024, 11, 6, 6, 0))
    ]
    
    # Initialize flight manager and add flights
    manager = FlightManager()
    for flight in flights:
        manager.add_flight(flight)
    
    # Create and run interactive booking system
    booking_system = InteractiveBooking(manager)
    booking_system.run_booking_process()

if __name__ == "__main__":
    main()