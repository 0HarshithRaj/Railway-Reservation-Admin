# Railway Reservation Admin System

This project is a Railway Reservation Admin System built using Streamlit and SQLite. The system allows administrators to manage train schedules, book tickets, view booked seats, and perform various administrative operations. It serves as a basic demonstration of handling railway reservation operations through a simple web interface.

## Features

1. **Add Train**
   - Admins can add a new train to the system by providing details like train number, train name, departure date, start destination, and end destination.
   - This feature also automatically creates a seat table for the newly added train with 50 seats categorized into Window, Aisle, and Middle seats.

2. **View Train**
   - Admins can view all the trains available in the system. The trains' details like train number, name, departure date, start and end destinations are displayed.

3. **Search Train**
   - This feature allows admins to search for a specific train using the train number.

4. **Book Tickets**
   - Admins can book a ticket for a passenger by specifying the train number, seat type (Window, Aisle, Middle), passenger name, age, and gender.
   - The system automatically allocates the next available seat of the specified type.

5. **View Seats**
   - Admins can view the seating arrangement of a specific train. This shows which seats are booked and the details of the passengers occupying them.

6. **Cancel Tickets**
   - Admins can cancel a booking by specifying the train number and seat number. The seat is then marked as available again.

7. **Delete Train**
   - Admins can delete a train from the system by specifying the train number and departure date. This operation also drops the associated seat table for that train.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- pip
- Git

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/0HarshithRaj/Railway-Reservation-Admin.git
   cd Railway-Reservation-Admin

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

3. **Install the Required Packages:**
   ```bash
   pip install -r requirements.txt

4. **Run the Application:**
   ```bash
   streamlit run main.py

## Project Structure
1. **app.py:**
- Main application file containing the Streamlit interface and logic for train management.
2. **railway.db:**
- SQLite database file containing all the tables and data for trains, seats, and users.
3. **requirements.txt:**
- Lists all the dependencies required to run the project.
