import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv
import os
import datetime
import appointment as app


class BookingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Appointment Booking System")
        # Set the background color
        self.root.configure(bg="lightblue")
        self.appointments = []

        self.frame = tk.Frame(self.root, padx=30, pady=30)
        self.frame.pack()

        self.name_label = tk.Label(self.frame, text="Patient Name", font=("Helvetica", 14))
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.frame, font=("Helvetica", 14), width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.date_label = tk.Label(self.frame, text="Appointment Date", font=("Helvetica", 14))
        self.date_label.grid(row=0, column=2, padx=10, pady=10)
        self.date_entry = DateEntry(self.frame, font=("Helvetica", 14), width=28)
        self.date_entry.grid(row=0, column=3, padx=10, pady=10)

        self.time_label = tk.Label(self.frame, text="Appointment Time", font=("Helvetica", 14))
        self.time_label.grid(row=1, column=0, padx=10, pady=10)
        self.time_entry = tk.Entry(self.frame, font=("Helvetica", 14), width=30)
        self.time_entry.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self.frame, text="Book Appointment", command=self.book_appointment,
                                       font=("Helvetica", 14), width=30, height=2, cursor="hand2")
        # Bind the events
        self.submit_button.bind("<Enter>", self.on_button_hover)
        self.submit_button.bind("<Leave>", self.on_button_leave)
        self.submit_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        self.update_button = tk.Button(self.frame, text="Update Selected Appointment", command=self.update_appointment,
                                       font=("Helvetica", 14), width=30, height=2, cursor="hand2")
        # Bind the events
        self.update_button.bind("<Enter>", self.on_button_hover)
        self.update_button.bind("<Leave>", self.on_button_leave)
        self.update_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(self.frame, text="Delete Selected Appointment", command=self.delete_appointment,
                                       font=("Helvetica", 14), width=30, height=2, cursor="hand2")
        # Bind the events
        self.delete_button.bind("<Enter>", self.on_button_hover)
        self.delete_button.bind("<Leave>", self.on_button_leave)
        self.delete_button.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        self.display_button = tk.Button(self.frame, text="Display Appointments", command=self.display_appointments,
                                        font=("Helvetica", 14), width=30, height=2, cursor="hand2")
        # Bind the events
        self.display_button.bind("<Enter>", self.on_button_hover)
        self.display_button.bind("<Leave>", self.on_button_leave)
        self.display_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.search_label = tk.Label(self.frame, text="Search Patient", font=("Helvetica", 14))
        self.search_label.grid(row=1, column=2, padx=10, pady=10)
        self.search_entry = tk.Entry(self.frame, font=("Helvetica", 14), width=30)
        self.search_entry.grid(row=1, column=3, padx=10, pady=10)
        self.search_button = tk.Button(self.frame, text="Search", command=self.search_appointments,
                                       font=("Helvetica", 14), width=30, height=2, cursor="hand2")
        # Bind the events
        self.search_button.bind("<Enter>", self.on_button_hover)
        self.search_button.bind("<Leave>", self.on_button_leave)
        self.search_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        clear_button = tk.Button(self.frame, text="Clear Entry Fields", command=self.clear_entry_fields,
                                 font=("Helvetica", 14), width=30, height=2, cursor="hand2")
        clear_button.grid(row=4, column=2, columnspan=2, padx=10, pady=10)

        # Create treeview for displaying the appointments in a table
        self.tree = ttk.Treeview(self.frame, column=("column1", "column2", "column3"), show='headings')
        self.tree.heading("#1", text="Patient Name")
        self.tree.heading("#2", text="Appointment Date")
        self.tree.heading("#3", text="Appointment Time")

        # Create a vertical scrollbar for the treeview
        # self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        # self.scrollbar.grid(row=4, column=3, padx=10, pady=10, sticky='ns')
        # self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Increase the font size of the data displayed inside Treeview widget and column headers
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14))

        # The column headers don't respond to the Treeview style configuration.
        # They have to be configured with the Treeview.Heading style.
        style.configure("Treeview.Heading", font=("Helvetica", 14))

        # Read appointments from file at the start of the program
        self.load_appointments()

    def search_appointments(self):
        # First clear the existing data in the tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        search_term = self.search_entry.get().lower()

        for idx, appointment in enumerate(self.appointments):
            if search_term in appointment.name.lower():
                self.tree.insert('', 'end', iid=idx + 1, values=(appointment.name, appointment.date, appointment.time))

        if not self.tree.get_children():
            messagebox.showinfo("No Results", "No appointments found for the provided name.")

    def book_appointment(self):
        name = self.name_entry.get()
        date = self.date_entry.get_date()
        time = self.time_entry.get()

        if not name or not date or not time:
            messagebox.showerror("Error", "All fields must be filled.")
        else:
            self.appointments.append(app.Appointment(name, date.strftime('%Y-%m-%d'), time))
            self.name_entry.delete(0, tk.END)
            self.date_entry.set_date("")
            self.time_entry.delete(0, tk.END)
            self.display_appointments()  # Display updated appointments
            messagebox.showinfo("Success", "Appointment booked successfully!")

    def update_appointment(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "No appointment selected.")
            return

        # Get the selected appointment's details
        selected_appointment = self.appointments[int(selected[0]) - 1]
        selected_name = selected_appointment.name
        selected_date = selected_appointment.date

        new_time = self.time_entry.get()

        if not new_time:
            messagebox.showerror("Error", "Time field must be filled.")
        else:
            # Update the appointment with the new time, keeping the name and date unchanged
            self.appointments[int(selected[0]) - 1] = app.Appointment(selected_name, selected_date, new_time)
            messagebox.showinfo("Success", "Appointment updated successfully!")

    def delete_appointment(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "No appointment selected.")
            return

        del self.appointments[int(selected[0]) - 1]
        # self.display_appointments()
        messagebox.showinfo("Success", "Appointment deleted successfully!")

    def display_appointments(self):
        # Create a new toplevel window
        window = tk.Toplevel(self.root)
        window.title("Appointments")

        # Create treeview for displaying the appointments in a table in the new window
        tree = ttk.Treeview(window, column=("column1", "column2", "column3"), show='headings')
        tree.heading("#1", text="Patient Name")
        tree.heading("#2", text="Appointment Date")
        tree.heading("#3", text="Appointment Time")
        tree.pack(pady=10)

        # Increase the fontsize of the data displayed inside Treeview widget
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 14))

        # Populate the treeview with appointments
        for idx, appointment in enumerate(self.appointments):
            tree.insert('', 'end', iid=idx + 1, values=(appointment.name, appointment.date, appointment.time))

    def load_appointments(self):
        if os.path.isfile('appointments.csv'):
            with open('appointments.csv', newline='') as f:
                reader = csv.reader(f)
                self.appointments = [app.Appointment(row[0], row[1], row[2]) for row in reader]

    def save_appointments(self):
        with open('appointments.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for appointment in self.appointments:
                writer.writerow([appointment.name, appointment.date, appointment.time])

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.save_appointments()
        self.root.destroy()

    def clear_entry_fields(self):
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def on_button_hover(self, event):
        event.widget.configure(bg="lightblue")

    def on_button_leave(self, event):
        event.widget.configure(bg="SystemButtonFace")
