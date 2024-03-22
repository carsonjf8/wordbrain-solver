import pickle
import copy
from graph import Graph

def main() -> None:
    game_board = [
        ['b', 'y', 'z', 'r', 'e'],
        ['i', 't', 'h', 't', 'e'],
        ['l', 'd', 'i', 'e', 'g'],
        ['a', 'i', 'n', 'r', 'd'],
        ['r', 'z', 'm', 'a', 'a'],
        ['i', 'h', 'u', 'd', 'e']
    ]
    word_lengths = [4, 8, 8, 4, 6]
    # RAIN, HUMIDITY, BLIZZARD, HEAT, DEGREE
    # 4, 8, 8, 4, 6

    '''
    game_board = [
        ['i', 'r', 'l', 'y', 'a', 'e', 'c'],
        ['t', 'e', 's', 'n', 's', 'l', 'n'],
        ['t', 'f', 'i', 'r', 't', 'a', 'o'],
        ['r', 'p', 'v', 'l', 's', 's', 'n'],
        ['e', 'e', 'i', 'e', 'i', 'a', 'a'],
        ['c', 'n', 'a', 'r', 't', 'n', 'c'],
        ['r', 'a', 'm', 'a', 'p', 'm', 'd'],
        ['t', 'u', 'k', 'e', 'p', 's', 'a']
    ]
    word_lengths = [5, 5, 6, 6, 9, 7, 5, 8, 5]
    known_words = ['canon', '', 'trance', '', '', '', '', '', '']
    '''

    '''
    game_board = [
        ['t', 's', 'y', 'u', 'a', 'o', 's'],
        ['s', 'k', 'a', 'l', 'k', 'r', 'w'],
        ['t', 'e', 'o', 'e', 'o', 'm', 'e'],
        ['a', 'x', 'n', 's', 'h', 'l', 'e'],
        ['m', 's', 'o', 'o', 's', 'l', 'r'],
        ['e', 's', 't', 's', 'b', 'r', 'u'],
        ['e', 'b', 'a', 'l', 'c', 'l', 'y']
    ]
    # HOMEWORK, CLASSMATE, LESSONS, ESSAY, TEXTBOOK, RULER, SYLLABUS
    word_lengths = [8, 9, 6, 5, 8, 5, 8]
    known_words = []
    '''

    solve_board(game_board, word_lengths)
    
'''
main recursive function that solves the word puzzle
board: 2D list of the word puzzle
word_lengths: list of lengths of each solution word
known_words: list of known correct words
    if provided, the list should have the same length as word_lengths
    unknown words should be added as ''
word_index: index of which word the solver is correctly consider
solution: current solution word list being considered
progress: current progress percentage status
'''
def solve_board(board: list, word_lengths: list, known_words: list=[], word_index: int=0, solution: list=[], progress: list=[]) -> None:
    # print current progress
    progress_str = ''
    for percentage in progress:
        progress_str += f'{percentage[0]}/{percentage[1]} '
    print(progress_str)
    
    # check if the solver needs to look for more words
    if word_index >= len(word_lengths):
        print('solution', get_solution_words(solution), solution)
        return

    # create graph structure from current game board
    graph = create_graph_from_board(board)
    # find words in current board
    if len(known_words) > 0 and known_words[word_index] != '':
        found_words = find_words(graph, word_lengths[word_index], known_word=known_words[word_index])
    else:
        found_words = find_words(graph, word_lengths[word_index])
    # if no words found, end current solution branch
    if len(found_words) == 0:
        return
    # iterate through words found in board
    for index, word in enumerate(found_words):
        new_board = remove_word_from_board(copy.deepcopy(board), word)
        new_board = move_letters_down(new_board)
        solve_board(new_board, word_lengths, known_words, word_index + 1, solution + [word], progress + [(index + 1, len(found_words))])

# convert solution info to a more readable format
def get_solution_words(solution: list) -> str:
    solution_word_list = []
    for word in solution:
        solution_word = ''
        for letter in word:
            solution_word += letter[-1]
        solution_word_list.append(solution_word)
    return solution_word_list

# apply gravity to letters so that they fall after a word is found
def move_letters_down(board: list) -> list:
    for j in range(len(board[0])):
        for i in range(len(board) - 1, -1, -1):
            if board[i][j] != '-':
                continue
            for k in range(i - 1, -1, -1):
                if board[k][j] != '-':
                    board[i][j], board[k][j] = board[k][j], board[i][j]
                    break
    return board

# removes a word from the current board
def remove_word_from_board(board: list, word: str) -> list:
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if f'{i}_{j}_{val}' in word:
                board[i][j] = '-'
    return board

# construct a graph data structure format of the game board
# nodes are letters and edges connect neighboring letters
def create_graph_from_board(board: list) -> Graph:
    board_width = len(board[0])
    board_height = len(board)

    graph = Graph()
    # add vertices to the graph
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == '-':
                continue
            graph.add_vertex(f'{i}_{j}_{val}')
    # add edges to the graph
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == '-':
                continue
            for p in [-1, 0, 1]:
                if i + p < 0 or i + p >= board_height:
                    continue
                for q in [-1, 0, 1]:
                    if j + q < 0 or j + q >= board_width or (p == 0 and q == 0):
                        continue
                    graph.add_edge(f'{i}_{j}_{val}', f'{i + p}_{j + q}_{board[i + p][j + q]}')
    return graph

# search for words in the game board graph
def find_words(graph: Graph, word_len: int, known_word: str='') -> list:
    if known_word == '':
        with open(f'data/{word_len}.pickle', 'rb') as f:
            word_list = pickle.load(f)
    else:
        word_list = [known_word]

    found_word_list = []
    for word in word_list:
        for vertex in graph.get_vertices():
            if word[0] in vertex:
                find_word_in_graph(graph, vertex, word, 1, [vertex], found_word_list)
    return found_word_list

# helper function to find words in game board graph
def find_word_in_graph(graph: Graph, node_id: str, word: str, letter_index: int, visited_list: list, found_word_list: list) -> None:
    if letter_index >= len(word):
        found_word_list.append(visited_list)
        return
    for adj_vertex in graph.adj_list[node_id]:
        if adj_vertex in visited_list:
            continue
        if word[letter_index] in adj_vertex:
            find_word_in_graph(graph, adj_vertex, word, letter_index + 1, visited_list + [adj_vertex], found_word_list)

# print a list of words in a better format
def pretty_print_words(word_list: list) -> None:
    for word in word_list:
        pretty_print = ''
        for letter in word:
            pretty_print += letter[-1]
        print(pretty_print, word)

if __name__ == '__main__':
    main()