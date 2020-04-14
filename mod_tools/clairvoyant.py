### YOU CAN RUN IT REPL.IT
### https://repl.it/repls/SelfishDopeyBinarytree


#------- CONFIG --------#

# 0 = unknown (u)
# 1 = good or SK (g)
# 2 = evil (e)
u = 0
g = 1
e = 2

original_board = [
  [g, g, g, g, u],
  [g, g, u, u, u],
  [g, u, g, g, u],
  [g, u, u, g, g]];

name_board = [
  ["DJ", "Kathy", "Kai", "Krystal", "Goku"],
  ["Tony", "Tobin", "Lala", "Anish", "Deba"],
  ["Tim", "Vincent", "Arjun", "Abir", "Tina"],
  ["Ajay", "Victoria", "Nikhil", "Aditi", "Aarti"]];

# people who can't be all evil together
people_who_cant_be_together = [
  # ["DJ", "Krystal"],
  # ["Tony", "Abir"],
];

# groups of people where if one is good, the other is evil (and vice versa)
people_who_are_mutually_exclusive = [
  # ["Tony", "Abir"],
]

board_width = 5;
board_height = 4;
max_num_evil = 4;



#------- FUNCTIONS --------#
def print_board(title, board):
  print(title)
  for y in range(len(board)):
    row = board[y]
    print(row);
  print("\n")

def get_all_points_of_value(value, board):
  result = []
  for y in range(len(board)):
    for x in range(len(board[0])):
      elt = board[y][x]
      if elt == value:
        result.append((x, y))
  return result

def get_first_point_of_value(value, board):
  for y in range(len(board)):
    for x in range(len(board[0])):
      elt = board[y][x]
      if elt == value:
        return((x, y))
  return None

def names_to_points(group):
  points = []
  for name in group:
    points.append(get_first_point_of_value(name, name_board))
  return points

# def getAllPairs(board):
#   for point in get_all_points_of_value(u, board):
#     get_adj_points(point)

def get_adj_points(point):
  x = point[0]
  y= point[1]
  adjs = []
  if (x > 0):
    adjs.append((x - 1, y))
  if (x < board_width - 1):
    adjs.append((x + 1, y))
  if (y > 0):
    adjs.append((x, y - 1))
  if (y < board_height - 1):
    adjs.append((x, y + 1))
  return adjs

def get_value_at_point(point, board):
  return board[point[1]][point[0]]

def get_values_at_points(points):
  result = []
  for point in points:
    result.append(get_value_at_point(point))
  return result

def get_num_evil(board):
  return len(get_all_points_of_value(e, board))

def print_all_possible_boards(board):
  board_stack = []
  board_copy = copy_of(board)
  rectify_board(board_copy)
  rectify_mutually_exclusives(board_copy)
  board_stack.append(board_copy)
  num_runs = 0
  num_board_possibilities = 0
  likelihoods = {}
  while len(board_stack) > 0:
    num_runs += 1
    cur_board = board_stack.pop()
    good_version = copy_of(cur_board)
    evil_version = copy_of(cur_board)
    goodify_first_unknown(good_version)
    evilize_first_unknown(evil_version)
    rectify_mutually_exclusives(good_version)
    rectify_mutually_exclusives(evil_version)
    if not board_is_known(good_version):
      board_stack.append(good_version)
    if not board_is_known(evil_version) and not found_all_evil(evil_version):
      board_stack.append(evil_version)
    if found_all_evil(evil_version):
      goodify_all_unknowns(evil_version)
      #print_board("POSSIBLE BOARD", evil_version)
      if board_has_people_who_cant_be_together(evil_version):
        continue
      num_board_possibilities += 1
      evil_points = get_all_points_of_value(e, evil_version)
      for point in evil_points:
        if point in likelihoods:
          likelihoods[point] += 1
        else:
          likelihoods[point] = 1
  print("TOTAL POSSIBILITIES: " + str(num_board_possibilities))
  pretty_print_likelihoods(likelihoods, num_board_possibilities)
  # pretty_print_likelihoods_rigged("Goku", likelihoods, num_board_possibilities)

def board_has_people_who_cant_be_together(board):
  for group in people_who_cant_be_together:
    group_points = names_to_points(group)
    if board_has_specific_evil_people(group_points, board):
      return True
  return False

def board_has_specific_evil_people(points, board):
  all_evil = get_all_points_of_value(e, board)
  for point in points:
    if point not in all_evil:
      return False
  return True

def pretty_print_likelihoods(likelihoods, num_board_possibilities):
  sorted_likelihoods = {k: v for k, v in sorted(likelihoods.items(), reverse=True, key=lambda item: item[1])}
  for point in sorted_likelihoods:
    percent = sorted_likelihoods[point] / num_board_possibilities
    print (get_value_at_point(point, name_board) + " : " + str(sorted_likelihoods[point]) + " or " + "{:.2%}".format(percent))

def pretty_print_likelihoods_rigged(evil_name, likelihoods, num_board_possibilities):
  sorted_likelihoods = {k: v for k, v in sorted(likelihoods.items(), reverse=True, key=lambda item: item[1])}
  print (evil_name + " : " + str(num_board_possibilities) + " or " + "{:.2%}".format(1))
  for point in sorted_likelihoods:
    percent = sorted_likelihoods[point] / num_board_possibilities
    name = get_value_at_point(point, name_board)
    if name == evil_name:
      continue
    print (get_value_at_point(point, name_board) + " : " + str(sorted_likelihoods[point]) + " or " + "{:.2%}".format(percent))

def found_all_evil(board):
  evilizedCount = get_num_evil(board)
  if evilizedCount >= max_num_evil:
    return True
  else:
    return False

def evilize_board_greedy(board):
  evilizedCount = get_num_evil(board)
  while not board_is_known(board) and evilizedCount < max_num_evil:
    evilize_first_unknown(board)
    evilizedCount += 1
  if evilizedCount == max_num_evil:
    goodify_all_unknowns(board)
    return True
  else:
    return False

# takes all the evils and makes their surroundings good
def rectify_board(board):
  evils = get_all_points_of_value(e, board)
  for evil in evils:
    evilize(evil, board)

def rectify_mutually_exclusives(board):
  for group in people_who_are_mutually_exclusive:
    group_points = names_to_points(group)
    if (get_value_at_point(group_points[0], board) == e):
      goodify(group_points[1], board)
    if (get_value_at_point(group_points[1], board) == e):
      goodify(group_points[0], board)
    if (get_value_at_point(group_points[0], board) == g):
      evilize(group_points[1], board)
    if (get_value_at_point(group_points[1], board) == g):
      evilize(group_points[0], board)

def evilize_first_unknown(board):
  point = get_first_point_of_value(u, board)
  evilize(point, board)

def evilize(point, board):
  board[point[1]][point[0]] = 2;
  adjs = get_adj_points(point)
  for adj in adjs:
    goodify(adj, board)

def goodify_first_unknown(board):
  point = get_first_point_of_value(u, board)
  goodify(point, board)

def goodify_all_unknowns(board):
  points = get_all_points_of_value(u, board)
  for point in points:
    goodify(point, board)

def goodify(point, board):
  board[point[1]][point[0]] = 1;

def board_is_known(board):
  for row in board:
    for elt in row:
      if elt == 0:
        return False
  return True

def copy_of(board):
  return [x[:] for x in board]



#------- MAIN PROGRAM --------#
print_board("ORIGINAL BOARD", original_board)
print_all_possible_boards(original_board)
