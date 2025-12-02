import numpy as np
from pettingzoo.classic import connect_four_v3
from loguru import logger
from random_agent_copy2 import RandomAgent
from smart_agent_improved import SmartAgent

def test_get_valid_actions():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=42)
    agent = SmartAgent(env)
    
    mask = [1, 1, 1, 1, 1, 1, 1]  # All columns valid
    assert agent._get_valid_actions(mask) == [0, 1, 2, 3, 4, 5, 6]

    mask = [0, 1, 0, 1, 0, 1, 0]  # Only odd columns
    assert agent._get_valid_actions(mask) == [1, 3, 5]

def test_get_next_row():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=42)
    agent = SmartAgent(env)

    # Empty board - piece goes to bottom
    board = np.zeros((6, 7, 2))
    assert agent._get_next_row(board, 3) == 5

    # Column with one piece - next piece goes on top
    board[5, 3, 0] = 1
    assert agent._get_next_row(board, 3) == 4

def to_board(matrix, channel=0):
    board = np.zeros((6,7,2))
    for r in range(6):
        for c in range(7):
            if matrix[r][c] == 1:
                board[r,c,channel] = 1
    return board

def test_check_win_from_position():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=0)
    agent = SmartAgent(env)

    # horizontal
    matrix = [
        [0,1,1,1,1,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]
    board = to_board(matrix, channel=0)
    assert agent._check_win_from_position(board, row=0, col=3, channel=0) is True

    # vertical
    matrix = [
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ]
    board = to_board(matrix, channel=0)
    assert agent._check_win_from_position(board, row=0, col=3, channel=0) is True

    # diagonal / 
    matrix = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0],
        [0,0,0,0,1,0,0],
        [0,0,0,1,0,0,0],
        [0,0,1,0,0,0,0],
    ]
    board = to_board(matrix, channel=0)
    assert agent._check_win_from_position(board, row=3, col=4, channel=0) is True

    # diagonal \ 
    matrix = [
        [0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0],
    ]
    board = to_board(matrix, channel=0)
    assert agent._check_win_from_position(board, row=2, col=2, channel=0) is True

def test_find_winning_move():
    env = connect_four_v3.env(render_mode=None)
    env.reset(seed=0)
    agent = SmartAgent(env)

    matrix = [
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,1,1,0,0],
        [0,0,0,1,0,1,0],
    ]
    observation = to_board(matrix, channel=0)
    action_mask = [1, 1, 1, 1, 1, 1, 1]
    valid_actions = agent._get_valid_actions(action_mask)
    assert agent._find_winning_move(observation, valid_actions, channel=0) == 3

def test_smart_vs_random():
    smart_wins = 0
    games = 100

    for _ in range(games):
        env = connect_four_v3.env(render_mode=None)
        env.reset()

        smart_agent = SmartAgent(env, player_name="player_0")
        random_agent = RandomAgent(env, player_name="player_1")

        total_rewards = {"player_0": 0, "player_1": 0}
        move_history = []  

        for agent_name in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()

            total_rewards[agent_name] += reward

            if termination or truncation:
                env.step(None)
                continue

            obs_array = observation["observation"]
            action_mask = observation["action_mask"]

            if agent_name == "player_0":
                action = smart_agent.choose_action(
                    obs_array, reward, termination, truncation, info, action_mask
                )
            else:
                action = random_agent.choose_action(
                    obs_array, reward, termination, truncation, info, action_mask
                )

            move_history.append((agent_name, action)) 

            env.step(action)
            
        print("Total rewards this game:", total_rewards)

        if total_rewards["player_0"] == 1:
            smart_wins += 1
        else:
            print("SmartAgent LOST this game!")
            print("Move history for this losing game:")
            for i, (player, col) in enumerate(move_history, start=1):
                print(f"  Step {i}: {player} played column {col}")

        env.close()

    win_rate = smart_wins / games * 100
    print(f"SmartAgent win rate: {win_rate:.2f}%")
    assert smart_wins >= games * 0.5






if __name__ == "__main__": # 手动调用测试函数
    test_get_valid_actions()

if __name__ == "__main__":
    test_get_next_row()

if __name__ == "__main__":
    test_check_win_from_position()

if __name__ == "__main__":
    test_find_winning_move()

if __name__ == "__main__":
    test_smart_vs_random()
