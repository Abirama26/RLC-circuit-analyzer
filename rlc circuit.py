import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def get_rlc_inputs():
    """Open a dialog for the user to enter R, L, C values and time range."""
    dialog = tk.Toplevel()
    dialog.title("Enter RLC Values and Time Range")
    dialog.grab_set()  # Lock focus on this window

    labels = [
        "Initial Resistor (Ω):", 
        "Initial Capacitor (F):", 
        "Initial Inductor (H):", 
        "Start Time (s):", 
        "End Time (s):", 
        "Number of Points:"
    ]

    entries = []
    defaults = ["", "", "", "0", "10", "100"]

    for i, (label_text, default_value) in enumerate(zip(labels, defaults)):
        tk.Label(dialog, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(dialog)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, default_value)
        entries.append(entry)

    data = {}

    def on_submit():
        try:
            r_init = float(entries[0].get())
            c_init = float(entries[1].get())
            l_init = float(entries[2].get())
            start_time = float(entries[3].get())
            end_time = float(entries[4].get())
            num_points = int(entries[5].get())

            if start_time >= end_time or num_points <= 0:
                messagebox.showerror("Invalid Input", "Start time must be less than end time, and points must be positive.")
                return

            data.update({
                'resistor_initial': r_init,
                'capacitor_initial': c_init,
                'inductor_initial': l_init,
                'start_time': start_time,
                'end_time': end_time,
                'num_points': num_points
            })
            dialog.destroy()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    submit_btn = tk.Button(dialog, text="Submit", command=on_submit)
    submit_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    dialog.wait_window()
    return data

def plot_rlc_variations(rlc_data, plot_frame):
    """Calculate and plot RLC variations over time."""
    if not rlc_data:
        messagebox.showinfo("No Data", "Please enter RLC values first.")
        return

    r_init = rlc_data['resistor_initial']
    c_init = rlc_data['capacitor_initial']
    l_init = rlc_data['inductor_initial']
    start_time = rlc_data['start_time']
    end_time = rlc_data['end_time']
    num_points = rlc_data['num_points']

    time = np.linspace(start_time, end_time, num_points)

    resistor = r_init * (1 + 0.1 * np.sin(2 * np.pi * 0.1 * time))
    capacitor = c_init * (1 + 0.05 * np.cos(2 * np.pi * 0.2 * time))
    inductor = l_init * (1 + 0.02 * time / end_time)

    # Clear old plot if any
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Create new figure
    fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)  # Bigger figure
    fig.suptitle('RLC Variations Over Time', fontsize=16)

    axs[0].plot(time, resistor, label=f'Resistor (Initial: {r_init:.2f} Ω)', color='blue')
    axs[0].set_ylabel('Resistance (Ω)')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(time, capacitor, label=f'Capacitor (Initial: {c_init:.2e} F)', color='orange')
    axs[1].set_ylabel('Capacitance (F)')
    axs[1].legend()
    axs[1].grid(True)

    axs[2].plot(time, inductor, label=f'Inductor (Initial: {l_init:.2e} H)', color='green')
    axs[2].set_xlabel('Time (s)')
    axs[2].set_ylabel('Inductance (H)')
    axs[2].legend()
    axs[2].grid(True)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Embed figure into tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

def main():
    """Main function to run the Tkinter app."""
    window = tk.Tk()
    window.title("RLC Variance Analyzer")

    # Maximize window
    window.state('zoomed')  # For Windows (maximize). If Linux/Mac, you can use: window.attributes('-zoomed', True)

    # Plot frame setup
    plot_frame = tk.Frame(window)
    plot_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def on_button_click():
        rlc_data = get_rlc_inputs()
        plot_rlc_variations(rlc_data, plot_frame)

    input_btn = tk.Button(window, text="Enter RLC Values and Plot", command=on_button_click, font=("Arial", 14))
    input_btn.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    main()
