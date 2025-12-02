"""
My Smart Agent for Connect Four

This agent uses rule-based heuristics to play strategically.
"""

import random
from loguru import logger


class SmartAgent:
    """
    A rule-based agent that plays strategically
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the smart agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.player_name = player_name or "SmartAgent"

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        if terminated or truncated:
            return None
        
        valid_actions = self._get_valid_actions(action_mask)

        # Rule 1: Win immediately
        winning_move = self._find_winning_move(observation, valid_actions, channel=0)
        if winning_move is not None:
            logger.success(f"{self.player_name}: WINNING MOVE -> column {winning_move}")
            return winning_move

        # Rule 2: Block opponent
        blocking_move = self._find_winning_move(observation, valid_actions, channel=1)
        if blocking_move is not None:
            logger.warning(f"{self.player_name}: BLOCKING -> column {blocking_move}")
            return blocking_move
        
        # Rule 3: Avoid suicidal moves
        safe_move = self._find_not_suicidal_move(observation,valid_actions,channel=0)
        if safe_move:
            logger.info(f"{self.player_name}: SUICIDAL FILTER APPLIED -> using {safe_move}") 
            valid_actions = safe_move
        else:
            logger.info(f"{self.player_name}: NO SAFE ACTIONS -> using all valid actions")

        # Rule 4: extend my chain
        best_col = None
        best_score = 0
        for col in valid_actions:
            row = self._get_next_row(observation, col)
            observation1=observation.copy()
            observation1[row,col,0] = 1
            score = self._extend_chain_move(observation1,row, col, channel=0)
            if score > best_score:
                best_score = score
                best_col = col
        if best_col is not None:
            logger.info(f"{self.player_name}: HEURISTIC BEST -> column {best_col}")
            return best_col

        # Rule 5: Create double threat (TODO - Advanced)
        # A double threat is when you create two ways to win at once
        for col in valid_actions:
            if self._creates_double_threat(observation, col, channel=0):
                logger.info(f"{self.player_name}: DOUBLE THREAT -> column {col}")
                return col

        # Rule 6: Prefer center columns
        center_preference = [3, 2, 4, 1, 5, 0, 6]
        for col in center_preference:
            if col in valid_actions:
                logger.info(f"{self.player_name}: CENTER PREFERENCE -> column {col}")
                return col

        # Rule 7: Random fallback
        action = random.choice(valid_actions)
        logger.debug(f"{self.player_name}: RANDOM -> column {action}")
        return action
        

    def _get_valid_actions(self, action_mask): # 把action_mash转化为可以下棋的列
        """
        Get list of valid column indices

        Parameters:
            action_mask: numpy array (7,) with 1 for valid, 0 for invalid

        Returns:
            list of valid column indices
        """
        # TODO: Implement this
        n = len(action_mask) # n = 7
        l = []
        for i in range(n):
            if action_mask[i] == 1:
                l.append(i)
        return l

    def _find_winning_move(self, observation, valid_actions, channel):
        """
        Find a move that creates 4 in a row for the specified player

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            column index (int) if winning move found, None otherwise
        """
        # TODO: For each valid action, check if it would create 4 in a row
        # Hint: Simulate placing the piece, then check for wins
        for col in valid_actions:
            board = observation.copy()
            row = self._get_next_row(board, col)
            board[row, col, channel] = 1          # 落棋
            if self._check_win_from_position(board, row, col, channel) == True:
                return col

    def _get_next_row(self, board, col): # 找到在某一列落下棋子时，会落在哪一行
        """
        Find which row a piece would land in if dropped in column col

        Parameters:
            board: numpy array (6, 7, 2)
            col: column index (0-6)

        Returns:
            row index (0-5) if space available, None if column full
        """
        # TODO: Implement this
        # Hint: Start from bottom row (5) and go up
        # A position is empty if board[row, col, 0] == 0 and board[row, col, 1] == 0
        for row in range(5, -1, -1):  # Start from bottom (row 5)
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row  # This position is empty
        return None  # Column is full

    def _check_win_from_position(self, board, row, col, channel):
        """
        Check if placing a piece at (row, col) would create 4 in a row

        Parameters:
            board: numpy array (6, 7, 2)
            row: row index (0-5)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if this position creates 4 in a row/col/diag, False otherwise
        """
        # TODO: Check all 4 directions: horizontal, vertical, diagonal /, diagonal \
        # Hint: Count consecutive pieces in both directions from (row, col)
        #horizontal(水平) : 左侧和右侧同色棋子大于等于3 则true
        r3, c3 = row, col
        r4, c4 = row, col
        count_gauche_1 = 0
        count_droite_1 = 0
        while c3 + 1 <= 6:
            c3 += 1
            if board[row,c3,channel] == 1:
                count_droite_1 += 1
            else:
                break
        while c4 - 1 >= 0:
            c4 -= 1
            if board[row,c4,channel] == 1:
                count_gauche_1 += 1
            else:
                break
        if count_gauche_1 + count_droite_1 >= 3:
            return True


        #vertical(垂直) : 下方有三个同色棋子 则true
        if row < 3 and board[row+1,col,channel] == board[row+2,col,channel] == board[row+3,col,channel] == 1:
            return True

        #diagonal / : 左下方和右上方同色棋子大于等于3 则true
        r1, c1 = row, col
        r2, c2 = row, col
        count_gauche_2 = 0
        count_droite_2 = 0
        while r1 + 1 <= 5 and c1 - 1 >= 0:
            r1 += 1
            c1 -= 1
            if board[r1,c1,channel] == 1:
                count_gauche_2 += 1
            else: 
                break
        while r2 - 1 >= 0 and c2 + 1 <= 6:
            r2 -= 1
            c2 += 1
            if board[r2,c2,channel] == 1:
                count_droite_2 += 1
            else: 
                break
        if count_gauche_2 + count_droite_2 >= 3:
            return True

        #diagonal \ : 左上方和右下方同色棋子大于等于3 则true
        r3, c3 = row, col
        r4, c4 = row, col
        count_gauche_3 = 0
        count_droite_3 = 0
        while r3 - 1 >= 0 and c3 - 1 >=0:
            r3 -= 1
            c3 -= 1
            if board[r3,c3,channel] == 1:
                count_gauche_3 += 1
            else: 
                break
        while r4 + 1 <= 5 and c4 + 1 <= 6:
            r4 += 1
            c4 += 1
            if board[r4,c4,channel] == 1:
                count_droite_3 += 1
            else: 
                break
        if count_gauche_3 + count_droite_3 >= 3:
            return True
        return False
    
    def _creates_double_threat(self, board, col, channel):
        """
        Check if playing column col creates two separate winning threats

        A double threat is unbeatable because opponent can only block one.

        如果我现在把子下在 col 这一列，会不会让下一回合时我有 ≥ 2 个立即获胜的落子选择？

        Returns:
            True if move creates double threat, False otherwise
        """
        # TODO: This is advanced - implement if you have time
        # Hint: After placing piece, count how many ways you can win next turn
        row=self._get_next_row(board, col)
        if row is None:
            return False
        board1 = board.copy()
        board1[row,col,channel] = 1 # board1 只下了col这一列
        count = 0
        for c in range(7):
            row2=self._get_next_row(board1, c)
            if row2 is None:
                continue
            board2 = board1.copy()
            board2[row2,c,channel] = 1 # board2 尝试下每一列
            if self._check_win_from_position(board2,row2,c,channel) == True:
                count += 1
            if count >= 2:
                return True
        return False
    
    def _find_not_suicidal_move(self,board,valid_actions,channel):
        """
        Avoid making a move that allows the opponent to win immediately on their next turn.

        Returns:
            A list of columns that are not suicidal moves
        """
        l = []
        for c in valid_actions:
            board1=board.copy()
            row = self._get_next_row(board1,c)
            board1[row,c,channel] = 1
            suicidal = False
            for c1 in valid_actions:
                board2 = board1.copy()
                row1 = self._get_next_row(board2,c1)
                if row1 is None:
                    continue
                board2[row1,c1,1-channel] = 1
                if self._check_win_from_position(board2,row1,c1,1-channel):
                    suicidal = True
                    break
            if not suicidal:
                l.append(c)
        return l

    def _extend_chain_move(self,observation,row, col, channel=0):
        """
        Assign a score to each column, according to the following rules:
            - For every new three-in-a-row created: +100 points
            - For every new two-in-a-row created: +10 points
            - If the move is in column 3: +20 points
            - If the move is in columns 2 or 4: +10 points
            - If the move is in columns 0, 1, 5, or 6: +5 points

        Returns:
            The computed score
        """
        score = 0
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]
        for dr, dc in directions:
            count = 1 
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 7 and observation[r, c, channel] == 1:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < 6 and 0 <= c < 7 and observation[r, c, channel] == 1:
                count += 1
                r -= dr
                c -= dc

            if count == 3:
                score += 100
            elif count ==2:
                score += 10

        if col == 3:
            score += 20
        elif col == 2 or col == 4:
            score += 10
        elif col == 0 or col == 1 or col == 5 or col == 6:
            score += 5 
        return score
