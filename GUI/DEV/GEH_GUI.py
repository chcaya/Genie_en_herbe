import customtkinter as ctk
import serial
import serial.tools.list_ports

def set_player_id(team_index, player_id):
    team_player_id[team_index] = player_id
    update_player_id_display()

def reset():
    global team_player_id
    team_player_id = ["", ""]
    # Send a reset command to the Arduino
    ser.write(b"R\n")  # b"RESET\n" converts the string to bytes
    print("Reset")
    update_player_id_display()

def bind_reset_to_enter(event):
    reset()

def update_player_id_display():
    for i in range(2):
        display_square = display_squares[i]
        display_square.delete("all")
        size = 30
        padding = 5
        score = team_player_id[i]

        # Add the score as text inside the canvas
        text_x = display_square.winfo_reqwidth() / 2
        text_y = display_square.winfo_reqheight() / 2
        display_square.create_text(text_x, text_y, text=str(score), font=("Roboto", 24))

def create_column(container, team_index):
    column_frame = ctk.CTkFrame(container)
    column_frame.grid(row=0, column=team_index)

    Combobox = ctk.CTkComboBox(master=column_frame,
                                values=team_labels,
                                command=combobox_cb,
                                font=("Roboto", 12))
    Combobox.set("Select team")
    Combobox.grid(row=0, column=0)

    square_frame = ctk.CTkFrame(column_frame)
    square_frame.grid(row=1, column=0, padx=5, pady=5)

    square = ctk.CTkCanvas(square_frame, width=200, height=30, bg="grey")
    square.pack(ipadx=5, ipady=5)
    display_squares.append(square)

def combobox_cb(choice):
    print(choice)

def detect_esp32_com_port():
    esp32_com_port = None

    # Get a list of available serial ports
    available_ports = list(serial.tools.list_ports.comports())

    for port in available_ports:
        if "CP210x" in port.description:
            esp32_com_port = port.device
            break

    return esp32_com_port

def read_serial_data():
    try:
        serial_data = ser.readline().decode().strip()

        if serial_data.startswith("W"):
            # A winner message is received, extract the winner index
            winner_index = int(serial_data[1:])
            # Update the score for the winning team (assuming 0 and 1 are the teams in your GUI)
            if 0 <= winner_index <= 3:
                player_id = winner_index+1
                set_player_id(0, player_id)
            elif 4 <= winner_index <= 7:
                player_id = winner_index-3
                set_player_id(1, player_id)
            
        elif serial_data == "D":
            # Draw message is received, handle the draw scenario in your GUI
            # For example, display a message indicating the draw
            draw = "D"
            set_player_id(0, draw)
            set_player_id(1, draw)

    except ValueError:
        pass  # Handle invalid data (non-integer values)

    # Schedule the read_serial_data() function to be called again after 100ms
    root.after(100, read_serial_data)



team_player_id = [0, 0]
display_squares = []
team_labels =   ["ULaval",
                "Poly",
                "MgCil",
                "Conco",
                "Sherby",
                "UQTR",
                "ETS",
                "UQAT",
                "UQOttawa",
                "UQAC",
                "RiMoncton",
                "Drummond"]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("GEH")

container_frame = ctk.CTkFrame(root)
container_frame.grid(row=0, column=0, padx=10, pady=10)

# Create the columns inside the container frame and pass the reset_button
create_column(container_frame, 0)
create_column(container_frame, 1)
reset_button = ctk.CTkButton(root, text="Reset", command=reset)
reset_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.bind("<Return>", bind_reset_to_enter)

esp32_com_port = detect_esp32_com_port()

if esp32_com_port is None:
    print("ESP32 not found.")
else:
    print("ESP32 detected on:", esp32_com_port)

# Open the serial port for communication with the MCU
ser = serial.Serial(esp32_com_port, 9600, timeout=1)

reset()

# Schedule the read_serial_data() function to be called initially and then every 100ms
root.after(0, read_serial_data)

root.mainloop()
