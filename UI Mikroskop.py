import tkinter as tk
from tkinter import messagebox
import serial

# Inisialisasi variabel serial
ser = None

# Fungsi untuk menghubungkan ke port serial
def connect_serial():
    global ser
    com_port = com_port_entry.get()
    try:
        ser = serial.Serial(com_port, 9600, timeout=1)
        messagebox.showinfo("Success", f"Connected to {com_port}")
    except serial.SerialException:
        messagebox.showerror("Error", f"Failed to connect to {com_port}")
        ser = None

# Fungsi untuk mengirimkan perintah serial
def send_serial_command(command):
    if ser and ser.is_open:
        ser.write(command.encode())
        print(f"{command} command sent")
    else:
        messagebox.showerror("Error", "Not connected to any COM port")

# Fungsi untuk setiap tombol
def up_command():
    send_serial_command('S')

def down_command():
    send_serial_command('W')

def left_command():
    send_serial_command('A')

def right_command():
    send_serial_command('D')

# Membuat GUI dengan Tkinter
root = tk.Tk()
root.title("Directional Control")

# Label dan Entry untuk COM port
com_port_label = tk.Label(root, text="Enter COM Port:")
com_port_label.grid(row=0, column=0, pady=10)

com_port_entry = tk.Entry(root)
com_port_entry.grid(row=0, column=1, pady=10)

connect_button = tk.Button(root, text="Connect", command=connect_serial, width=10)
connect_button.grid(row=0, column=2, pady=10)

# Menambahkan tombol arah
button_up = tk.Button(root, text="UP", command=up_command, width=10, height=2)
button_up.grid(row=1, column=1, pady=5)

button_left = tk.Button(root, text="LEFT", command=left_command, width=10, height=2)
button_left.grid(row=2, column=0, padx=5)

button_right = tk.Button(root, text="RIGHT", command=right_command, width=10, height=2)
button_right.grid(row=2, column=2, padx=5)

button_down = tk.Button(root, text="DOWN", command=down_command, width=10, height=2)
button_down.grid(row=3, column=1, pady=5)

# Menjalankan loop utama Tkinter
root.mainloop()

# Jangan lupa untuk menutup port serial saat program berakhir
if ser:
    ser.close()
