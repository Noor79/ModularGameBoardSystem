import pygame
from typing import Dict, Tuple, List, Any, Optional
from config import BoardConfig, PieceInfo

class BoardGUI:
    """Graphical User Interface for the game board"""
    
    def __init__(self, board_config: BoardConfig, title: str = "Modular Game Board"):
        pygame.init()
        self.board_config = board_config
        self.screen_width = self.board_config.size[1] * self.board_config.square_size
        self.screen_height = self.board_config.size[0] * self.board_config.square_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(title)
        
        self.font = pygame.font.Font(None, 36)
        self.board_state: Dict[str, Optional[PieceInfo]] = {}
        self.highlights: Dict[str, List[str]] = {}
        self.message: str = ""
        
    def update_board_state(self, new_state: Dict[str, Optional[PieceInfo]]):
        self.board_state = new_state
        
    def update_highlights(self, new_highlights: Dict[str, List[str]]):
        if 'clear' in new_highlights and new_highlights['clear']:
            self.highlights = {}
        else:
            self.highlights.update(new_highlights)
            
    def set_message(self, message: str):
        self.message = message

    def draw_board(self):
        for row in range(self.board_config.size[0]):
            for col in range(self.board_config.size[1]):
                x = col * self.board_config.square_size
                y = row * self.board_config.square_size
                
                color = (200, 200, 200) if (row + col) % 2 == 0 else (100, 100, 100)
                pygame.draw.rect(self.screen, color, (x, y, self.board_config.square_size, self.board_config.square_size))
                
                # Draw position label
                pos_name = next(key for key, val in self.board_config.position_mapping.items() if val == (row, col))
                text_surface = self.font.render(pos_name, True, (255, 255, 255))
                self.screen.blit(text_surface, (x + 5, y + 5))
                
                # Draw highlights
                if 'selected' in self.highlights and pos_name in self.highlights['selected']:
                    pygame.draw.rect(self.screen, (0, 255, 0), (x, y, self.board_config.square_size, self.board_config.square_size), 5)
                elif 'possible_moves' in self.highlights and pos_name in self.highlights['possible_moves']:
                    pygame.draw.rect(self.screen, (0, 0, 255), (x, y, self.board_config.square_size, self.board_config.square_size), 5)
                elif 'invalid' in self.highlights and pos_name in self.highlights['invalid']:
                    pygame.draw.rect(self.screen, (255, 0, 0), (x, y, self.board_config.square_size, self.board_config.square_size), 5)

    def draw_pieces(self):
        for position, piece in self.board_state.items():
            if piece and piece.position:
                row, col = self.board_config.position_mapping[piece.position]
                x = col * self.board_config.square_size + self.board_config.square_size // 2
                y = row * self.board_config.square_size + self.board_config.square_size // 2
                
                color = (255, 255, 255) if piece.color == "White" else (0, 0, 0)
                pygame.draw.circle(self.screen, color, (x, y), self.board_config.square_size // 3)
                
                text_surface = self.font.render(piece.piece_type[0].upper(), True, (0, 255, 0) if piece.color == "White" else (255, 255, 255))
                text_rect = text_surface.get_rect(center=(x, y))
                self.screen.blit(text_surface, text_rect)

    def draw_message(self):
        text_surface = self.font.render(self.message, True, (255, 255, 0))
        self.screen.blit(text_surface, (10, self.screen_height - 40))

    def render(self):
        self.screen.fill((0, 0, 0)) # Clear screen
        self.draw_board()
        self.draw_pieces()
        self.draw_message()
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def quit(self):
        pygame.quit()


