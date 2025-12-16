import tkinter as tk
from tkinter import ttk
import load_data
import converter
import threading


class CurrencyConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        self.loader = load_data.load_data()
        self.converter = converter.converter()

        # Load initial data
        self.loader.load()
        self.currencies = self.loader.parse()
        self.converter.currencies = self.currencies
        self.last_update = self.loader.timestamp

        self.create_widgets()

    def create_widgets(self):
        # Amount
        tk.Label(self.root, text="Amount:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root, width=20)
        self.amount_entry.pack()

        # currency 1
        tk.Label(self.root, text="From:").pack(pady=5)
        currency_list = sorted(list(self.currencies.keys()))
        self.from_combo = ttk.Combobox(self.root, values=currency_list, state="readonly", width=18)
        self.from_combo.set("USD")
        self.from_combo.pack()

        # currency 2
        tk.Label(self.root, text="To:").pack(pady=5)
        self.to_combo = ttk.Combobox(self.root, values=currency_list, state="readonly", width=18)
        self.to_combo.set("RON")
        self.to_combo.pack()

        # convert
        tk.Button(self.root, text="Convert", command=self.convert, bg="green", fg="white").pack(
            pady=5)

        # result
        self.result_label = tk.Label(self.root, text="Result: ")
        self.result_label.pack(pady=5)

        # Rrefresh
        tk.Button(self.root, text="Refresh Rates", command=self.refresh_pushbtn).pack(pady=5)

        # last_update
        self.update_label = tk.Label(self.root, text=f"Last update: {self.last_update}")
        self.update_label.pack()

    def convert(self):
        amount = float(self.amount_entry.get())
        from_curr = self.from_combo.get()
        to_curr = self.to_combo.get()

        result = self.converter.convert(amount, from_curr, to_curr)
        self.result_label.config(text=f"Result: {result:.4f} {to_curr}")


    def refresh_pushbtn(self):
        threading.Thread(target=self.refresh_rates).start()

    def refresh_rates(self):
            self.loader.load()
            self.currencies = self.loader.parse()
            self.converter.currencies = self.currencies
            self.last_update = self.loader.timestamp
            self.root.after(0, self.update_ui)

    def update_ui(self):
        currency_list = sorted(list(self.currencies.keys()))
        self.from_combo['values'] = currency_list
        self.to_combo['values'] = currency_list
        self.update_label.config(text=f"Last update: {self.last_update}")


def main():
    root = tk.Tk()
    CurrencyConverterGUI(root)
    root.mainloop()
