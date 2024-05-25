import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class Car:
    def __init__(self, car_code, year, name, company, rate):
        self.car_code = car_code
        self.year = year
        self.name = name
        self.company = company
        self.rate = rate

class CarRentalApp:
    def __init__(self, catalog_filename):
        self.car_catalog = []
        self.catalog_filename = catalog_filename
        self.load_catalog(catalog_filename)

        self.root = tk.Tk()
        self.root.title("Car Rental System")
        self.create_widgets()

    def load_catalog(self, filename):
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 5:
                        car_code = row[0]
                        year = int(row[1])
                        name = row[2]
                        company = row[3]
                        rate = float(row[4])
                        self.car_catalog.append(Car(car_code, year, name, company, rate))
        except FileNotFoundError:
            messagebox.showerror("Error", f"Failed to open the car catalog file: '{filename}' not found.")
        except IOError:
            messagebox.showerror("Error", "Failed to open the car catalog file: I/O error.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def save_catalog(self):
        try:
            with open(self.catalog_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                for car in self.car_catalog:
                    writer.writerow([car.car_code, car.year, car.name, car.company, car.rate])
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while saving: {e}")

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)

        self.search_book_tab = tk.Frame(self.notebook)

        self.notebook.add(self.search_book_tab, text="Search & Book Cars")

        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_search_book_tab()

    def create_search_book_tab(self):
        self.year_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.company_var = tk.StringVar()

        search_frame = ttk.Frame(self.search_book_tab)
        search_frame.pack(padx=20, pady=20, fill=tk.X)

        tk.Label(search_frame, text="Year:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.year_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(search_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.name_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(search_frame, text="Company:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.company_var).grid(row=2, column=1, padx=5, pady=5)

        search_button = tk.Button(search_frame, text="Search", command=self.perform_search)
        search_button.grid(row=3, columnspan=2, padx=5, pady=10)

        self.car_list_frame = ttk.Frame(self.search_book_tab)
        self.car_list_frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)

        self.car_tree = ttk.Treeview(self.car_list_frame)
        self.car_tree["columns"] = ("year", "name", "company", "rate")
        self.car_tree.heading("#0", text="Code")
        self.car_tree.heading("year", text="Year")
        self.car_tree.heading("name", text="Name")
        self.car_tree.heading("company", text="Company")
        self.car_tree.heading("rate", text="Rate")
        self.car_tree.pack(expand=True, fill=tk.BOTH)

        for car in self.car_catalog:
            self.car_tree.insert("", "end", text=car.car_code, values=(car.year, car.name, car.company, car.rate))

        self.car_tree.bind("<Double-1>", self.on_car_select)

        book_frame = ttk.Frame(self.search_book_tab)
        book_frame.pack(padx=20, pady=20, fill=tk.X)

        tk.Label(book_frame, text="Car Code:").grid(row=0, column=0, padx=5, pady=5)
        self.car_code_entry = tk.Entry(book_frame)
        self.car_code_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(book_frame, text="Legal Name:").grid(row=1, column=0, padx=5, pady=5)
        self.legal_name_entry = tk.Entry(book_frame)
        self.legal_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(book_frame, text="Days:").grid(row=2, column=0, padx=5, pady=5)
        self.days_entry = tk.Entry(book_frame)
        self.days_entry.grid(row=2, column=1, padx=5, pady=5)

        self.book_button = tk.Button(book_frame, text="Book", command=self.book_car)
        self.book_button.grid(row=3, columnspan=2, padx=5, pady=10)

    def perform_search(self):
        try:
            year = int(self.year_var.get()) if self.year_var.get().isdigit() else None
            name = self.name_var.get().lower()
            company = self.company_var.get().lower()

            # Clear previous search results
            for item in self.car_tree.get_children():
                self.car_tree.delete(item)

            # Perform search
            results = self.search_cars(year, name, company)
            if results:
                for car in results:
                    self.car_tree.insert("", "end", text=car.car_code, values=(car.year, car.name, car.company, car.rate))
            else:
                messagebox.showinfo("No Results", "No matching cars found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during search: {e}")

    def search_cars(self, year, name, company):
        results = []
        for car in self.car_catalog:
            if (year is None or car.year == year) and \
               (name == "" or name in car.name.lower()) and \
               (company == "" or company in car.company.lower()):
                results.append(car)
        return results

    def on_car_select(self, event):
        item = self.car_tree.selection()[0]
        car_code = self.car_tree.item(item, "text")
        car = next((car for car in self.car_catalog if car.car_code == car_code), None)

        if car:
            self.car_code_entry.delete(0, tk.END)
            self.car_code_entry.insert(0, car.car_code)
            self.notebook.select(self.search_book_tab)

    def book_car(self):
        try:
            car_code = self.car_code_entry.get()
            legal_name = self.legal_name_entry.get()
            days = int(self.days_entry.get()) if self.days_entry.get().isdigit() else 0

            car = next((car for car in self.car_catalog if car.car_code == car_code), None)
            if car and legal_name and days > 0:
                self.generate_receipt(legal_name, car, days)
            else:
                messagebox.showinfo("Invalid Input", "Please ensure all fields are correctly filled.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while booking: {e}")

    def generate_receipt(self, user_name, car, days):
        try:
            base_cost = days * car.rate
            tax = 0.20 * base_cost
            service_charge = 0.05 * base_cost
            total_cost = base_cost + tax + service_charge
            date_str = datetime.now().strftime("%Y-%m-%d")

            receipt_message = f"\n********** Car Rental Receipt **********\n" \
                              f"Car: {car.name} ({car.year}) from {car.company}\n" \
                              f"Days rented: {days}\n" \
                              f"Rate per day: ${car.rate:.2f}\n" \
                              f"Base cost: ${base_cost:.2f}\n" \
                              f"Tax (20%): ${tax:.2f}\n" \
                              f"Service charge (5%): ${service_charge:.2f}\n" \
                              f"Total cost: ${total_cost:.2f}\n" \
                              f"Rented by: {user_name}\n" \
                              f"Date: {date_str}\n" \
                              f"***************************************\n" \
                              f"Thank you for using Car Rental Service!"

            messagebox.showinfo("Receipt", receipt_message)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating receipt: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    car_rental = CarRentalApp("car_catalog.csv")
    car_rental.run()
