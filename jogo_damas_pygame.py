import pygame
import sys

#Instalar pygame para rodar!!!!!!!!!!!!!!!!!!
BOARD_SIZE = 8
SQUARE_SIZE = 80
WIDTH = HEIGHT = BOARD_SIZE * SQUARE_SIZE

DARK_COLOR = (139, 69, 19)
LIGHT_COLOR = (245, 245, 220)
BLACK_PIECE = (0, 0, 0)
RED_PIECE = (200, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)  # indica dama

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Damas")

#INICIALIZAÇÃO DAS PEÇAS
# Cada peça: [linha, coluna, cor, é_dama]
pieces = []
for row in range(BOARD_SIZE):
    for col in range(BOARD_SIZE):
        if (row + col) % 2 == 1:
            if row <= 2:
                pieces.append([row, col, BLACK_PIECE, False])
            elif row >= 5:
                pieces.append([row, col, RED_PIECE, False])

selected_piece = None
current_turn = BLACK_PIECE  # começa o jogador preto

#FUNÇÕES
def draw_board():
    """Desenha o tabuleiro 8x8"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    """Desenha todas as peças no tabuleiro"""
    for piece in pieces:
        row, col, color, is_king = piece
        pygame.draw.circle(screen, color,
                           (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2),
                           SQUARE_SIZE//2 - 10)
        if is_king:
            pygame.draw.circle(screen, HIGHLIGHT_COLOR,
                               (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2),
                               SQUARE_SIZE//2 - 25, 3)

def get_piece_at(row, col):
    """Retorna a peça na posição (row, col), se existir"""
    for piece in pieces:
        if piece[0] == row and piece[1] == col:
            return piece
    return None

def is_valid_move(piece, row, col):
    """Verifica se o movimento é válido"""
    target = get_piece_at(row, col)
    if target or piece[2] != current_turn:
        return False
    dr, dc = row - piece[0], col - piece[1]
    if abs(dr) == 1 and abs(dc) == 1:
        # Movimento simples diagonal
        if piece[3]:  # dama pode andar para qualquer direção
            return True
        if piece[2] == BLACK_PIECE and dr > 0:
            return True
        if piece[2] == RED_PIECE and dr < 0:
            return True
    elif abs(dr) == 2 and abs(dc) == 2:
        # Movimento de captura
        mid_row, mid_col = piece[0] + dr // 2, piece[1] + dc // 2
        mid_piece = get_piece_at(mid_row, mid_col)
        if mid_piece and mid_piece[2] != piece[2]:
            return True
    return False

def capture_piece(piece, row, col):
    """Retorna a peça capturada se o movimento for de captura"""
    dr, dc = row - piece[0], col - piece[1]
    if abs(dr) == 2 and abs(dc) == 2:
        mid_row, mid_col = piece[0] + dr // 2, piece[1] + dc // 2
        mid_piece = get_piece_at(mid_row, mid_col)
        if mid_piece and mid_piece[2] != piece[2]:
            return mid_piece
    return None

def get_square_under_mouse(pos):
    """Retorna a linha e coluna da casa em que o mouse está"""
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def check_winner():
    """Verifica se há um vencedor"""
    black_exists = any(p[2] == BLACK_PIECE for p in pieces)
    red_exists = any(p[2] == RED_PIECE for p in pieces)
    if not black_exists:
        return "Vermelho venceu!"
    if not red_exists:
        return "Preto venceu!"
    return None

#LOOP PRINCIPAL
while True:
    screen.fill((0,0,0))
    draw_board()
    draw_pieces()
    pygame.display.flip()

    winner = check_winner()
    if winner:
        print(winner)
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_under_mouse(event.pos)
            piece = get_piece_at(row, col)
            if piece and piece[2] == current_turn:
                selected_piece = piece

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece:
                row, col = get_square_under_mouse(event.pos)
                captured = capture_piece(selected_piece, row, col)
                if captured:
                    pieces.remove(captured)
                    selected_piece[0], selected_piece[1] = row, col
                elif is_valid_move(selected_piece, row, col):
                    selected_piece[0], selected_piece[1] = row, col
                # Promoção a dama
                if selected_piece[2] == BLACK_PIECE and selected_piece[0] == BOARD_SIZE-1:
                    selected_piece[3] = True
                elif selected_piece[2] == RED_PIECE and selected_piece[0] == 0:
                    selected_piece[3] = True
                # Alterna turno
                current_turn = RED_PIECE if current_turn == BLACK_PIECE else BLACK_PIECE
                selected_piece = None
