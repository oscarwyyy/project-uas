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

# Fungsi untuk menghitung total pendapatan
def hitung_total_pendapatan():
    total = sum(pendapatan)
    label_total_pendapatan.config(text=f"Total Pendapatan: {locale.currency(total, grouping=True)}")
    return total

# Fungsi untuk menghitung saldo
def hitung_saldo():
    total_pengeluaran = hitung_total_pengeluaran()
    total_pendapatan = hitung_total_pendapatan()
    saldo = total_pendapatan - total_pengeluaran
    label_saldo.config(text=f"Saldo: {locale.currency(saldo, grouping=True)}")
    return saldo

# Fungsi untuk menampilkan grafik pengeluaran vs pendapatan
def tampilkan_grafik():
    total_pengeluaran = hitung_total_pengeluaran()
    total_pendapatan = hitung_total_pendapatan()
    
    plt.bar(['Pendapatan', 'Pengeluaran'], [total_pendapatan, total_pengeluaran], color=['green', 'red'])
    plt.title('Pendapatan vs Pengeluaran')
    plt.ylabel('Jumlah (Rp)')
    plt.show()

# Fungsi untuk mereset semua data
def reset_data():
    global pengeluaran, pendapatan
    pengeluaran = []
    pendapatan = []
    listbox_pengeluaran.delete(0, tk.END)
    listbox_pendapatan.delete(0, tk.END)
    label_total_pengeluaran.config(text="Total Pengeluaran: Rp 0")
    label_total_pendapatan.config(text="Total Pendapatan: Rp 0")
    label_saldo.config(text="Saldo: Rp 0")

# Fungsi untuk menghapus pengeluaran yang dipilih
def hapus_pengeluaran():
    try:
        selected = listbox_pengeluaran.curselection()
        if selected:
            index = selected[0]
            pengeluaran.pop(index)
            listbox_pengeluaran.delete(index)
            hitung_total_pengeluaran()
    except Exception as e:
        messagebox.showerror("Hapus Error", "Terjadi kesalahan saat menghapus data pengeluaran.")

# Fungsi untuk menghapus pendapatan yang dipilih
def hapus_pendapatan():
    try:
        selected = listbox_pendapatan.curselection()
        if selected:
            index = selected[0]
            pendapatan.pop(index)
            listbox_pendapatan.delete(index)
            hitung_total_pendapatan()
    except Exception as e:
        messagebox.showerror("Hapus Error", "Terjadi kesalahan saat menghapus data pendapatan.")

def load_data():
    global pengeluaran, pendapatan
    pengeluaran = load_value(file_name1)
    pendapatan = load_value(file_name2)

    # Populate listboxes with loaded data
    for kategori, jumlah in pengeluaran:
        listbox_pengeluaran.insert(tk.END, f"{kategori}: {locale.currency(jumlah, grouping=True)}")
    for jumlah in pendapatan:
        listbox_pendapatan.insert(tk.END, f"{locale.currency(jumlah, grouping=True)}")

# Menyiapkan data awal
pengeluaran = load_value(file_name1)
pendapatan = load_value(file_name2)

# Membuat GUI
root = tk.Tk()
root.title("Aplikasi Keuangan Pribadi")
root.geometry("1200x800")
root.configure(bg="#f0f0f0")  # Setting background color

# Frame utama untuk semua widget
frame_main = tk.Frame(root, bg="#ffffff", bd=5)
frame_main.place(relx=0.5, rely=0.5, anchor="center")

# Frame untuk Pengeluaran
frame_pengeluaran = tk.LabelFrame(frame_main, text="Pengeluaran", font=("Arial", 14), bg="#ffffff", bd=2)
frame_pengeluaran.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

label_kategori_pengeluaran = tk.Label(frame_pengeluaran, text="Kategori Pengeluaran:", font=("Arial", 12), bg="#ffffff")
label_kategori_pengeluaran.grid(row=0, column=0, padx=10, pady=5, sticky="w")

options = ["Makanan", "Shopping", "Hiburan", "Elektronik", "Listrik", "Air", "Cicilan", "Bensin"]
clicked = tk.StringVar()
clicked.set("Kategori")
drop = tk.OptionMenu(frame_pengeluaran, clicked, *options)
drop.grid(row=0, column=1, padx=10, pady=5)

label_jumlah_pengeluaran = tk.Label(frame_pengeluaran, text="Jumlah Pengeluaran (Rp):", font=("Arial", 12), bg="#ffffff")
label_jumlah_pengeluaran.grid(row=1, column=0, padx=10, pady=5, sticky="w")

entry_jumlah_pengeluaran = tk.Entry(frame_pengeluaran, font=("Arial", 12))
entry_jumlah_pengeluaran.grid(row=1, column=1, padx=10, pady=5)

button_tambah_pengeluaran = tk.Button(frame_pengeluaran, text="Tambah Pengeluaran", command=tambah_pengeluaran, bg="#4CAF50", fg="white", font=("Arial", 12))
button_tambah_pengeluaran.grid(row=2, column=0, columnspan=2, pady=10)

button_hapus_pengeluaran = tk.Button(frame_pengeluaran, text="Hapus Pengeluaran Terpilih", command=hapus_pengeluaran, bg="#F44336", fg="white", font=("Arial", 12))
button_hapus_pengeluaran.grid(row=3, column=0, columnspan=2, pady=5)

listbox_pengeluaran = tk.Listbox(frame_pengeluaran, height=6, font=("Arial", 12))
listbox_pengeluaran.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

label_total_pengeluaran = tk.Label(frame_pengeluaran, text="Total Pengeluaran: Rp 0", font=("Arial", 12, "bold"), bg="#ffffff")
label_total_pengeluaran.grid(row=5, column=0, columnspan=2, pady=5)

# Frame untuk Pendapatan
frame_pendapatan = tk.LabelFrame(frame_main, text="Pendapatan", font=("Arial", 14), bg="#ffffff", bd=2)
frame_pendapatan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

label_jumlah_pendapatan = tk.Label(frame_pendapatan, text="Jumlah Pendapatan (Rp):", font=("Arial", 12), bg="#ffffff")
label_jumlah_pendapatan.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_jumlah_pendapatan = tk.Entry(frame_pendapatan, font=("Arial", 12))
entry_jumlah_pendapatan.grid(row=0, column=1, padx=10, pady=5)

button_tambah_pendapatan = tk.Button(frame_pendapatan, text="Tambah Pendapatan", command=tambah_pendapatan, bg="#4CAF50", fg="white", font=("Arial", 12))
button_tambah_pendapatan.grid(row=1, column=0, columnspan=2, pady=10)

button_hapus_pendapatan = tk.Button(frame_pendapatan, text="Hapus Pendapatan Terpilih", command=hapus_pendapatan, bg="#F44336", fg="white", font=("Arial", 12))
button_hapus_pendapatan.grid(row=2, column=0, columnspan=2, pady=5)

listbox_pendapatan = tk.Listbox(frame_pendapatan, height=6, font=("Arial", 12))
listbox_pendapatan.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

label_total_pendapatan = tk.Label(frame_pendapatan, text="Total Pendapatan: Rp 0", font=("Arial", 12, "bold"), bg="#ffffff")
label_total_pendapatan.grid(row=4, column=0, columnspan=2, pady=5)

# Frame untuk Saldo
frame_saldo = tk.Frame(frame_main, bg="#ffffff", bd=2)
frame_saldo.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

label_saldo = tk.Label(frame_saldo, text="Saldo: Rp 0", font=("Arial", 14, "bold"), bg="#ffffff")
label_saldo.grid(row=0, column=0, padx=10, pady=10)

button_hitung_saldo = tk.Button(frame_saldo, text="Hitung Saldo", command=hitung_saldo, bg="#2196F3", fg="white", font=("Arial", 12))
button_hitung_saldo.grid(row=1, column=0, pady=10)

button_grafik = tk.Button(frame_saldo, text="Tampilkan Grafik", command=tampilkan_grafik, bg="#2196F3", fg="white", font=("Arial", 12))
button_grafik.grid(row=2, column=0, pady=10)

# Tombol Reset
button_reset = tk.Button(root, text="Reset Data", command=reset_data, bg="#FF9800", fg="white", font=("Arial", 12))
button_reset.pack(pady=20)

# Menjalankan GUI
load_data()

root.mainloop()

# Save values when the program ends
save_value(str(pengeluaran), file_name1)
save_value(str(pendapatan), file_name2)