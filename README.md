# Modular Game Board System

An interactive and modular game board prototype with sensor-based piece recognition and visual feedback. This repository contains the Python server for game logic and GUI, and the Arduino firmware for RFID reader management, all structured for modularity and extensibility. Ideal for research and development of adaptable board game systems.

## Project Structure

```
modular_board_game_system/
├── python_server/
│   ├── config.py
│   ├── game_logic/
│   │   ├── base.py
│   │   ├── chess.py
│   │   └── checkers.py
│   ├── gui.py
│   ├── serial_communication.py
│   └── main.py
├── arduino_firmware/
│   ├── config.h
│   ├── structures.h
│   ├── utility.ino
│   ├── configuration.ino
│   ├── hardware_init.ino
│   └── modular_gameBoard.ino
├── docs/
│   └── design_plan.md
├── examples/
└── LICENSE
└── README.md
```

## Python Server Setup

1.  **Prerequisites:** Ensure you have Python 3.x installed. You will also need `pygame` and `pyserial`.
    ```bash
    pip install pygame pyserial
    ```
2.  **Running the Server:**
    Navigate to the `python_server` directory and run `main.py`.
    ```bash
    cd modular_board_game_system/python_server
    python main.py <serial_port> <board_size> [game_type]
    ```
    -   `<serial_port>`: The serial port where your Arduino is connected (e.g., `COM3` on Windows, `/dev/ttyACM0` on Linux/macOS).
    -   `<board_size>`: `4x4` or `8x8`.
    -   `[game_type]`: Optional. `chess` (default) or `checkers`.

    Example:
    ```bash
    python main.py /dev/ttyACM0 4x4 chess
    ```

## Arduino Firmware Setup

1.  **Prerequisites:** Arduino IDE installed.
2.  **Libraries:** Install the `Adafruit PN532` library and `Wire` library (usually pre-installed).
3.  **Upload:** Open `modular_gameBoard.ino` in the Arduino IDE, ensure all `.ino` and `.h` files are in the same directory, select your Arduino Mega ADK board and port, then upload the sketch.

## Usage

Once both the Python server and Arduino firmware are running, place RFID-tagged game pieces on the board. The system will detect piece movements, validate them according to the selected game logic, and provide visual feedback on the GUI and potentially on the physical board (if LEDs are implemented and controlled by the Arduino).

## Contributing

Contributions are welcome! Please refer to the `docs/design_plan.md` for an overview of the modular architecture.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


