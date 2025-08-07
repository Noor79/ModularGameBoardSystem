import sys
import time
import json
from typing import Dict, Any

from config import BoardConfig, GameEvent, GameEventData, PieceInfo
from serial_communication import SerialCommunication
from gui import BoardGUI
from game_logic.base import GameLogic
from game_logic.chess import ChessLogic
from game_logic.checkers import CheckersLogic

class GameSystem:
    """Main class for the modular game board system"""
    
    def __init__(self, serial_port: str, board_size: str = "4x4", game_type: str = "chess"):
        self.serial_port = serial_port
        
        if board_size == "4x4":
            self.board_config = BoardConfig.create_4x4_config()
        elif board_size == "8x8":
            self.board_config = BoardConfig.create_8x8_config()
        else:
            raise ValueError("Unsupported board size. Choose '4x4' or '8x8'.")

        if game_type.lower() == "chess":
            self.game_logic: GameLogic = ChessLogic(self.board_config)
        elif game_type.lower() == "checkers":
            self.game_logic: GameLogic = CheckersLogic(self.board_config)
        else:
            raise ValueError("Unsupported game type. Choose 'chess' or 'checkers'.")

        self.serial_comm = SerialCommunication(self.serial_port)
        self.serial_comm.set_message_callback(self._handle_serial_message)
        
        self.gui = BoardGUI(self.board_config, title=f"Modular Board - {self.game_logic.get_game_name()}")
        
        self.current_board_state: Dict[str, Optional[PieceInfo]] = {}
        self.pieces = self.game_logic.initialize_pieces()
        
        print(f"Initialized {self.game_logic.get_game_name()} on a {board_size} board.")

    def _handle_serial_message(self, message: str):
        """Callback for messages received from Arduino"""
        print(f"Received from Arduino: {message}")
        
        try:
            parts = message.split(":")
            event_type_str = parts[0]
            piece_uid = parts[1]
            
            event_type = None
            if event_type_str == "PLACE":
                event_type = GameEvent.PIECE_PLACED
                position = parts[2]
                event_data = GameEventData(event_type, piece_uid, position)
            elif event_type_str == "LIFT":
                event_type = GameEvent.PIECE_LIFTED
                position = parts[2]
                event_data = GameEventData(event_type, piece_uid, position)
            elif event_type_str == "MOVE":
                event_type = GameEvent.PIECE_MOVED
                from_position = parts[2]
                to_position = parts[3]
                event_data = GameEventData(event_type, piece_uid, to_position, from_position)
            else:
                print(f"Unknown event type: {event_type_str}")
                return
            
            response = self.game_logic.handle_event(event_data)
            self.gui.set_message(response.get("message", ""))
            self.gui.update_highlights(response.get("highlights", {}))
            self.gui.update_board_state(self.game_logic.board_state)
            
            # Send feedback to Arduino if needed (e.g., invalid move indication)
            if not response.get("valid", True):
                self.serial_comm.send_command("INVALID_MOVE") # Example command
                
        except Exception as e:
            print(f"Error processing serial message: {e}")

    def run(self):
        """Main loop for the game system"""
        if not self.serial_comm.start():
            print("Failed to start serial communication. Exiting.")
            return
        
        running = True
        while running:
            running = self.gui.handle_input()
            self.gui.render()
            time.sleep(0.01) # Small delay to reduce CPU usage
            
        self.serial_comm.stop()
        self.gui.quit()
        print("Game system shut down.")

if __name__ == "__main__":
    # Example usage:
    # python main.py COM3 4x4 chess
    # python main.py /dev/ttyACM0 8x8 checkers
    
    if len(sys.argv) < 3:
        print("Usage: python main.py <serial_port> <board_size> [game_type]")
        sys.exit(1)
        
    serial_port = sys.argv[1]
    board_size = sys.argv[2]
    game_type = sys.argv[3] if len(sys.argv) > 3 else "chess"
    
    try:
        system = GameSystem(serial_port, board_size, game_type)
        system.run()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


