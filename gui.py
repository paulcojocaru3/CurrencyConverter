import tkinter as tk
from tkinter import ttk, messagebox
import load_data
import converter
import threading
from datetime import datetime, timedelta


""" GUI pentru converiterea valutelor cu refresh automat la ora 12 """

class CurrencyConverterGUI:
    """
    root -> fereastra main
    loader(instance) -> incarca date din BNR
    converter(instance) -> converteste intre valute
    currencies -> dict exchange values
    last_update -> last rate update time
    """
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

        self.no_cacheandfetch = None

        self.create_widgets()
        self.schedule_refresh()

    def create_widgets(self):
        """Crearea layerelor din GUI"""
        if self.loader.fetched:
            bg_color = "green"
            text = "Using latest BNR rates"
        elif self.loader.cached:
            bg_color = "orange"
            text = "Using cached rates - No network connection"
        else:
            bg_color = "red"
            text = "No cache/fetch - Please connect to the internet"
            self.no_cacheandfetch = True

        #banner
        self.banner = tk.Frame(self.root, bg=bg_color, height=35)
        self.banner.pack(fill="x")
        self.banner_label = tk.Label(self.banner, text=text, bg=bg_color, fg="white")
        self.banner_label.pack(pady=8)

        # Amount
        tk.Label(self.root, text="Amount:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root, width=20)
        self.amount_entry.pack()

        # currency 1
        tk.Label(self.root, text="From:").pack(pady=5)
        currency_list = sorted(list(self.currencies.keys()))
        self.from_combo = ttk.Combobox(self.root, values=currency_list, state="readonly", width=18)
        if self.currencies:
            self.from_combo.set("USD")
        self.from_combo.pack()

        # currency 2
        tk.Label(self.root, text="To:").pack(pady=5)
        self.to_combo = ttk.Combobox(self.root, values=currency_list, state="readonly", width=18)
        if self.currencies:
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
        if not (self.loader.fetched or self.loader.cached):
            messagebox.showwarning("Warning", "No exchange rates available. Refresh with your internet connection on!")
            return
        try:

            amount = float(self.amount_entry.get())
            from_curr = self.from_combo.get()
            to_curr = self.to_combo.get()

            result = self.converter.convert(amount, from_curr, to_curr)

            if isinstance(result, str):
                messagebox.showerror("Error", result)
            else:
                self.result_label.config(text=f"Result: {result:.4f} {to_curr}")
        except ValueError:
            messagebox.showwarning("Error", "Please enter a valid numeric amount.")
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def refresh_pushbtn(self):
        """Face handle la refresh button pentru a nu se bloca UI"""
        threading.Thread(target=self.refresh_rates).start()

    def refresh_rates(self):
            self.loader.load()
            self.currencies = self.loader.parse()
            self.converter.currencies = self.currencies
            self.last_update = self.loader.timestamp
            if not self.loader.cached and not self.loader.fetched:
                messagebox.showerror("Error", "You need have a internet connection to refresh!")
            elif not self.loader.fetched and self.loader.cached:
                messagebox.showerror("Warning", "Using cache, try to have a internet connection to have the latest BNR rates")
            self.root.after(0, self.update_ui)

    def update_ui(self):
        currency_list = sorted(list(self.currencies.keys()))
        self.from_combo['values'] = currency_list
        self.to_combo['values'] = currency_list
        if self.loader.fetched:
            self.result_label.config(text="Result: ")
        #update
        self.update_label.config(text=f"Last update: {self.last_update}")
        if self.loader.fetched:
            #banner
            self.banner.config(bg="green")
            self.banner_label.config(text="Using latest BNR rates", bg="green")
            if self.no_cacheandfetch:
                self.from_combo.set("USD")
                self.to_combo.set("RON")
            self.no_cacheandfetch = False
        elif self.loader.cached:
            #banner
            self.banner.config(bg="orange")
            self.banner_label.config(text="Using cached rates - No network connection", bg="orange")
        else:
            self.banner.config(bg="red")
            self.banner_label.config(text="No cache/fetch - Please connect to the internet", bg="red")

    def schedule_refresh(self):
        now = datetime.now()
        today_noon = now.replace(hour=13, minute=1, second=0, microsecond=0)
        if now >= today_noon:
            next_noon = today_noon + timedelta(days=1)
        else:
            next_noon = today_noon
        delay = (next_noon - now).total_seconds()
        delay = int(delay*1000)
        self.root.after(delay, self.time_refresh)

    def time_refresh(self):
        threading.Thread(target=self.refresh_rates, daemon=True).start()
        self.schedule_refresh()


def main():
    root = tk.Tk()
    CurrencyConverterGUI(root)
    root.mainloop()
