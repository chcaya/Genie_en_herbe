import customtkinter as ctk
import serial
import serial.tools.list_ports
import pygame

def set_player_id(team_index, player_id):
    team_player_id[team_index] = player_id
    update_player_id_display()

def reset():
    global team_player_id
    team_player_id = ["", ""]
    # Send a reset command to the Arduino
    ser.write(b"R\n")  # b"RESET\n" converts the string to bytes
    #print("Reset")
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

def detect_mcu_com_port():
    mcu_com_port = None

    # Get a list of available serial ports
    available_ports = list(serial.tools.list_ports.comports())

    for port in available_ports:
        if "CP210x" in port.description:
            mcu_com_port = port.device
            break
        
        if "Maple" in port.description:
            mcu_com_port = port.device
            break

        if "Serial" in port.description:
            mcu_com_port = port.device
            break

    return mcu_com_port

def read_serial_data():
    try:
        serial_data = ser.readline().decode()

        if len(serial_data) > 0:
            print(str(serial_data))
            input_data = int(serial_data)
            print(str(input_data))
            pressed_players = []

            for i in range(8):  # Assuming 8 bits
                if input_data & (1 << i):
                    pressed_players.append(i)

            str_team0 = ""
            str_team1 = ""

            if len(pressed_players) > 1:
                str_team0 += "D "
                str_team1 += "D "

            for i in pressed_players:
                if 0 <= i <= 3:
                    player_id = i+1
                    str_team0 += str(player_id) + " "
                
                elif 4 <= i <= 7:
                    player_id = i-3
                    str_team1 += str(player_id) + " "
            
            pygame.mixer.music.play()
            set_player_id(0, str_team0)
            set_player_id(1, str_team1)

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

pygame.mixer.init()
pygame.mixer.music.load("buzz_sound.wav")

container_frame = ctk.CTkFrame(root)
container_frame.grid(row=0, column=0, padx=10, pady=10)

# Create the columns inside the container frame and pass the reset_button
create_column(container_frame, 0)
create_column(container_frame, 1)
reset_button = ctk.CTkButton(root, text="Reset", command=reset)
reset_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

root.bind("<Return>", bind_reset_to_enter)

mcu_com_port = detect_mcu_com_port()

if mcu_com_port is None:
    print("MCU not found.")
else:
    print("MCU detected on:", mcu_com_port)

# Open the serial port for communication with the MCU
ser = serial.Serial(mcu_com_port, 115200, timeout=1)

reset()

# Schedule the read_serial_data() function to be called initially and then every 100ms
root.after(0, read_serial_data)

root.mainloop()
