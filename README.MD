# We are building a player vs player chess game 
The first version will be a chess game in the terminal between two players

# Things to do
- King in check after oponent moves --> (Done)
- A player must respond if their king is in check (and after reponse king is no more in check) and can't rock. --> (Done)
- The squares near the king are not attacked to allow rock --> (Done)
- The player still has legal moves (Have to consider if piece is pinned set can move to false) --> (Done)
    - Look if piece is pinned set pinned to true
    - Move any piece
    - Block check moves 
- Checkmate implementation --> (Done)
- Stalemate if no move available --> (Done)
- Stalemate if 3 repetition --> (Done)
- refactor the code --> (In progress)
- Pawn promotion
- We will see if we'll add the 50 moves rule
- Build UI using tkinter
