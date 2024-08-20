from operator import index

import pandas as pd
import streamlit as st
import sqlite3

from streamlit import columns

conn = sqlite3.connect('railway.db')
c = conn.cursor()

# Creating databases
def create_db():
    c.execute("create table if not exists users (username TEXT, password TEXT)")
    c.execute("create table if not exists employees(employee_id TEXT, password TEXT, designation TEXT)")
    c.execute("create table if not exists trains(train_number TEXT, train_name TEXT, departure_date TEXT, start_destination TEXT, end_destination TEXT)")

create_db()

# Searching the trains
def search_train(train_number):
    train_query = c.execute("select * from trains where train_number = ?", (train_number,))
    train_data = train_query.fetchone()
    return train_data

# Train destination search
def train_dest(start_dest, end_dest):
    train_query = c.execute("select * from trains where start_destination = ? AND end_destination = ?", (start_dest, end_dest))
    train_data = train_query.fetchone()
    return train_data

# Add train
def add_train(train_number, train_name, departure_date, starting_dest, ending_dest):
    c.execute("insert into trains (train_number, train_name, departure_date, start_destination, end_destination)"
              "values (?, ?, ?, ?, ?)", (train_number, train_name, departure_date, starting_dest, ending_dest))
    conn.commit()
    create_seat_table(train_number)

# Delete train
def delete_train(train_num, departure_date):
    train_query = c.execute("select * from trains where train_number = ?", (train_num,))
    train_data = train_query.fetchone()

    if train_data:
        c.execute("delete from trains where train_number = ? AND departure_date = ?", (train_num, departure_date))
        conn.commit()
        st.success(f"TRAIN IS DELETED SUCCESSFULLY !!")

# Create seat table for the train
def create_seat_table(train_num):
    c.execute(f"create table if not exists seats_{train_num} (seat_number INTEGER PRIMARY KEY, seat_type TEXT, booked INTEGER, passenger_name TEXT, passenger_age INTEGER, passenger_gender TEXT)")
    for i in range(1, 51):
        val = categorize_seat(i)
        c.execute(f"insert into seats_{train_num} (seat_number, seat_type, booked, passenger_name, passenger_age, passenger_gender)"
                  "values (?, ?, ?, ?, ?, ?);", (i, val, 0, '', '', ''))
    conn.commit()

# Book tickets
def book_tickets(train_num, passenger_name, passenger_gender, passenger_age, seat_type):
    train_query = c.execute("select * from trains where train_number = ?", (train_num,))
    train_data = train_query.fetchone()

    if train_data:
        seat_number = allocate_next_available_seat(train_num, seat_type)
        if seat_number:
            c.execute(f"update seats_{train_num} set booked = 1, passenger_name = ?, passenger_age = ?, passenger_gender = ? "
                      f"where seat_number = ?", (passenger_name, passenger_age, passenger_gender, seat_number[0]))
            conn.commit()
            st.success("BOOKED SUCCESSFULLY !!")

# Allocate next available seat
def allocate_next_available_seat(train_num, seat_type):
    seat_query = c.execute(f"select seat_number from seats_{train_num} where booked = 0 and seat_type = ?"
                            f"order by seat_number asc", (seat_type,))
    result = seat_query.fetchall()

    if result:
        return result[0]

# Categorize the seat in train
def categorize_seat(seat_num):
    if (seat_num % 10) in [0, 4, 5, 9]:
        return "Window"
    elif (seat_num % 10) in [2, 3, 6, 7]:
        return "Aisle"
    else:
        return "Middle"

# View seats
def view_seats(train_num):
    train_query = c.execute("select * from trains where train_number = ?", (train_num,))
    train_data = train_query.fetchone()

    if train_data:
        seat_query = c.execute(f'''select 'Number: ' || seat_number, 
        '\n Type: ' || seat_type, '\n Name: ' || passenger_name, '\n Age: ' || passenger_age, 
        '\n Gender: ' || passenger_gender as Details, booked from seats_{train_num} 
        order by seat_number asc''')
        result = seat_query.fetchall()

        if result:
            st.dataframe(result)

# Cancel tickets
def cancel_tickets(train_num, seat_number):
    train_query = c.execute("select * from trains where train_number = ?", (train_num,))
    train_data = train_query.fetchone()

    if train_data:
        c.execute(f"update seats_{train_num} set booked = 0, passenger_name = '', passenger_age = '', passenger_gender = '' "
                  f"where seat_number = ?",
                  (seat_number,))
        conn.commit()

        st.success("CANCELLED SUCCESSFULLY !!")

# Applying the above functions
def train_functions():
    st.title("Train Administration")
    functions = st.sidebar.selectbox("Select train functions ", ["Add train", "View train", "Search train", "Delete train",
                                                                 "Book tickets", "Cancel tickets", "View seats"])

    if functions == "Add train":
        st.header("Add a new train...")
        with st.form(key='new_train_details'):
            train_number = st.text_input("Train Number")
            train_name = st.text_input("Train Name")
            departure_date = st.date_input("Date")
            start_destination = st.text_input("Start Destination")
            end_destination = st.text_input("End Destination")
            submitted = st.form_submit_button("Add Train")
            if submitted and train_name != "" and train_number != "" and start_destination != "" and end_destination != "":
                add_train(train_number, train_name, departure_date, start_destination, end_destination)
                st.success("Train Added Successfully !!")

    elif functions == "View train":
        st.title("View train...")
        train_query = c.execute("Select * from trains")
        trains = train_query.fetchall()

        if trains:
            df = pd.DataFrame(trains, columns = ["Train Number", "Name", "Departure Date", "Start_Dest", "End_Dest"])
            st.dataframe(df, hide_index=True)
        else:
            st.write("No trains found !!")

    elif functions == "Search train":
        st.title("Search a train...")
        train_number = st.text_input("Enter the train number")

        if st.button("Search"):
            if train_number:
                train = search_train(train_number)
                if train:
                    st.write(f"Train Number: {train[0]}")
                    st.write(f"Train Name: {train[1]}")
                    st.write(f"Departure Date: {train[2]}")
                    st.write(f"Start Destination: {train[3]}")
                    st.write(f"End Destination: {train[4]}")
                else:
                    st.error("Train not found")

    elif functions == "Delete train":
        st.title("Delete a train...")
        train_number = st.text_input("Enter the train number")
        departure_date = st.date_input("Enter the date")

        if st.button("Delete Train"):
            if train_number:
                c.execute(f"drop table if exists seats_{train_number}")
                delete_train(train_number, departure_date)

    elif functions == "Book tickets":
        st.title("Book a train ticket...")
        train_number = st.text_input("Train Number")
        seat_type = st.selectbox("Seat Types", ["Window", "Aisle", "Middle"], index=0)
        passenger_name = st.text_input("Passenger Name")
        passenger_age = st.number_input("Passenger Age", min_value=1)
        passenger_gender = st.selectbox("Passenger Gender", ["Male", "Female"], index=0)

        if st.button("Book Ticket"):
            if train_number and passenger_name and passenger_gender and passenger_age:
                book_tickets(train_number, passenger_name, passenger_gender, passenger_age, seat_type)

    elif functions == "Cancel tickets":
        st.title("Cancel the tickets...")
        train_number = st.text_input("Enter the train number")
        seat_number = st.number_input("Enter seat number", min_value=1)

        if st.button("Cancel Ticket"):
            if train_number and seat_number:
                cancel_tickets(train_number, seat_number)

    elif functions == "View seats":
        st.title("View the seats...")
        train_number = st.text_input("Enter the train number")

        if st.button("View Seat"):
            if train_number:
                view_seats(train_number)

train_functions()
