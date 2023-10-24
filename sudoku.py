#!/usr/bin/env python
#coding:utf-8
"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys

ROW = "ABCDEFGHI"
COL = "123456789"
BOX_STARTS = ['A1', 'A4', 'A7', 'D1', 'D4', 'D7', 'G1', 'G4', 'G7']

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def domain_check(board, key, value):
    row_now, col_now = key
    unassed = set()

    for r in ROW:
        checker_row = r + col_now
        if board[checker_row] != 0 and board[checker_row] != value:
            unassed.add(board[checker_row])
    for c in COL:
        checker_col = row_now + c
        if board[checker_col] != 0 and board[checker_col] != value:
            unassed.add(board[checker_col])
    box_start = BOX_STARTS[(ROW.index(row_now) // 3) * 3 + COL.index(col_now) // 3]
    for i in range(3):
        for j in range(3):
            cell = chr(ord(box_start[0]) + i) + chr(ord(box_start[1]) + j)
            if board[cell] != 0 and board[cell] != value:
                unassed.add(board[cell])
    return (set(range(1, 10)) - unassed, 9 - len(unassed))


def constraints(board, key, value):
    row_now, col_now = key

    for r in ROW:
        if board[r + col_now] == value and board[r + col_now] != 0:
            return False
    for c in COL:
        if board[row_now + c] == value:
            return False
    box_start = BOX_STARTS[(ROW.index(row_now) // 3) * 3 + COL.index(col_now) // 3]
    for i in range(3):
        for j in range(3):
            cell = chr(ord(box_start[0]) + i) + chr(ord(box_start[1]) + j)
            if board[cell] == value:
                return False
    return True


#Choose the variable with the fewest legal values in its domain
def mrv_h(board):
    # return the variable with the fewest legal values in its domain

    mrv_key = min((k for k, v in board.items() if v == 0), key=lambda k: domain_check(board, k, board[k])[1], default=None)

    # If no key was found to be unassigned (mrv_key is still None), this will return None
    return mrv_key
            
            
def fc_algo(val, board, key):
    fc_check = {}
    row_now, col_now = key
    for i in ROW + COL:
        temp_key = row_now + i if i in COL else i + col_now
        if board[temp_key] == 0:
            domain, _ = domain_check(board, temp_key, val)
            if val in domain:
                domain.remove(val)
                fc_check[temp_key] = domain
                if not domain:
                    return None
            else:
                fc_check[temp_key] = domain
    box_start = BOX_STARTS[(ROW.index(row_now) // 3) * 3 + COL.index(col_now) // 3]
    for i in range(3):
        for j in range(3):
            temp_key = chr(ord(box_start[0]) + i) + chr(ord(box_start[1]) + j)
            if board[temp_key] == 0:
                domain, _ = domain_check(board, temp_key, val)
                if val in domain:
                    domain.remove(val)
                    fc_check[temp_key] = domain
                    if not domain:
                        return None
                else:
                    fc_check[temp_key] = domain
    return fc_check


def is_complete(board):
    """Check if the board is complete (i.e., no zeros in any cells)."""
    for v in board.values():
        if v == 0:
            return False
    return True


def backtracking(board):
    # TODO: implement this
    if is_complete(board):  # Check if the board is complete
        return board
    
    keys = mrv_h(board)
    
    if not keys:
        return board
    
    #print(f"MRV selected: {keys}")  # Debugging Point 1

    for values in range(1,10):
        if constraints(board, keys, values) == True:
            board[keys] = values
            
            inferences = fc_algo(values, board, keys)
            
            if inferences is None:
                board[keys] = 0  # undo the assignment
                continue
            
            if -1 not in board.values():  # No domain is empty due to forward checking
                result = backtracking(board)
                if result:
                    return result
            
            for cell_key in inferences:
                board[cell_key] = 0  # Restore values
            
            board[keys] = 0
            
    
    return None


if __name__ == '__main__':
     # Assume main_code() contains all the main logic
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        #########

        #########
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")