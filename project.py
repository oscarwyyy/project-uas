import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import locale
from tkinter import *
import ast

file_name1 = 'values1.txt'
file_name2 = 'values2.txt'
# Mengatur format angka ke IDR (Rupiah)
locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

def save_value(input_value, filename):
    with open(filename, 'w') as f:
        f.write(input_value)

def load_value(filename):
    try:
        with open(filename, 'r') as f:
            return ast.literal_eval(f.read())
    except:
        return []  # Return an empty list if the file doesn't exist or is empty

# Fungsi untuk menambahkan pengeluaran
def tambah_pengeluaran():
    try:
        kategori = clicked.get()
        jumlah = float(entry_jumlah_pengeluaran.get().replace('.', '').replace('Rp', '').strip())
        
        # Menambah data pengeluaran
        pengeluaran.append((kategori, jumlah))
        listbox_pengeluaran.insert(tk.END, f"{kategori}: {locale.currency(jumlah, grouping=True)}")
        
        # Menghitung ulang total pengeluaran
        hitung_total_pengeluaran()
    except ValueError:
        messagebox.showerror("Input Error", "Harap masukkan jumlah yang valid.")

# Fungsi untuk menambahkan pendapatan
def tambah_pendapatan():
    try:
        jumlah_pendapatan = float(entry_jumlah_pendapatan.get().replace('.', '').replace('Rp', '').strip())
        
        # Menambah pendapatan
        pendapatan.append(jumlah_pendapatan)
        listbox_pendapatan.insert(tk.END, f"{locale.currency(jumlah_pendapatan, grouping=True)}")
        
        # Menghitung ulang total pendapatan
        hitung_total_pendapatan()
        entry_jumlah_pendapatan.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Input Error", "Harap masukkan jumlah yang valid.")

# Fungsi untuk menghitung total pengeluaran
def hitung_total_pengeluaran():
    total = sum(jumlah for kategori, jumlah in pengeluaran)
    label_total_pengeluaran.config(text=f"Total Pengeluaran: {locale.currency(total, grouping=True)}")
    return total