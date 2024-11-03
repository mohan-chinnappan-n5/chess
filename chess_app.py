import streamlit as st
import chess
import chess.svg
import cairosvg
from PIL import Image
import io
import random

# Title of the app
st.title("MC Chess")

# Sidebar with rules of chess
st.sidebar.header("Chess Rules")
st.sidebar.markdown("""
### Basic Rules of Chess

1. **Objective**: The objective of chess is to checkmate your opponent's king, meaning the king is in a position to be captured and cannot escape.

2. **Board Setup**:
   - The board is an 8x8 grid.
   - Each player starts with 16 pieces: 1 king, 1 queen, 2 rooks, 2 knights, 2 bishops, and 8 pawns.

3. **Piece Movement**:
   - **King**: Moves one square in any direction.
   - **Queen**: Moves any number of squares in any direction.
   - **Rook**: Moves any number of squares horizontally or vertically.
   - **Bishop**: Moves any number of squares diagonally.
   - **Knight**: Moves in an "L" shape (two squares in one direction and then one square perpendicular).
   - **Pawn**: Moves forward one square but captures diagonally. On its first move, it can move forward two squares.

4. **Special Moves**:
   - **Castling**: A move involving the king and a rook.
   - **En Passant**: A special pawn capture.
   - **Promotion**: A pawn reaching the opposite end can be promoted to any piece (usually a queen).

5. **Check and Checkmate**:
   - **Check**: When a king is under threat of capture.
   - **Checkmate**: When a king is in check and cannot escape.

6. **Draw Conditions**:
   - Stalemate, insufficient material, threefold repetition, or the fifty-move rule can result in a draw.
""")
# Initialize the board only once, using session state
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Function to render the board and convert SVG to PNG for display in Streamlit
def render_board(board):
    svg_data = chess.svg.board(board)
    png_data = cairosvg.svg2png(bytestring=svg_data)
    return Image.open(io.BytesIO(png_data))

# Function for Black's move (randomly selects from legal moves)
def make_black_move(board):
    if not board.is_game_over():
        black_move = random.choice(list(board.legal_moves))
        board.push(black_move)
        st.write(f"Black played: {black_move}")

# Display the current state of the chess board
board_image = render_board(st.session_state.board)
st.image(board_image, caption="Chess Board")

# Input field for user moves
move = st.text_input("Enter your move (e.g., e2e4):")

# Process the user's move when entered
if move:
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in st.session_state.board.legal_moves:
            # Push the user's move to the board
            st.session_state.board.push(chess_move)
            st.success(f"Move '{move}' was successful.")
            
            # After the user move, make a move for Black
            make_black_move(st.session_state.board)
        else:
            st.error("Illegal move!")
    except ValueError:
        st.error("Invalid move format! Please use UCI format (e.g., e2e4).")

    # Re-render the same board after moves
    board_image = render_board(st.session_state.board)
    st.image(board_image, caption="Chess Board")  # This line updates the image

# Check for end of game conditions
if st.session_state.board.is_checkmate():
    st.write("Checkmate! Game over.")
elif st.session_state.board.is_stalemate():
    st.write("Stalemate! Game over.")
elif st.session_state.board.is_insufficient_material():
    st.write("Insufficient material! Game over.")
elif st.session_state.board.is_seventyfive_moves():
    st.write("Draw by seventy-five-move rule!")
elif st.session_state.board.is_fivefold_repetition():
    st.write("Draw by fivefold repetition!")
elif st.session_state.board.is_variant_draw():
    st.write("Draw!")

# Reset the game when the button is clicked
if st.button("Reset Game"):
    st.session_state.board.reset()
    st.write("Game has been reset!")
    # Re-render the board after reset
    board_image = render_board(st.session_state.board)
    st.image(board_image, caption="Chess Board After Reset")
