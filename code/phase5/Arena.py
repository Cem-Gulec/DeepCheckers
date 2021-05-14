import logging

from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def changeValues(self, action, valids):
        # Bu fonksiyonda player2 için üretilen action ve valids
        # değerlerinin düzeltilmesi için var
        
        # action : int değer
        # valids : array
        bin_action = format(action, 'b').zfill(10)
        bin_flip = ''.join('1' if x=='0' else '0' for x in bin_action[3:])
        bin_index = bin_action[:3] + bin_flip
        new_action = int(bin_index, 2)

        non_zero_indexes = [i for i,e in enumerate(valids) if e!=0]
        for old_index in non_zero_indexes:
            bin_old_index = format(old_index, 'b').zfill(10)
            bin_new_index = ''.join('1' if x=='0' else '0' for x in bin_old_index[3:])
            bin_index = bin_old_index[:3] + bin_new_index
            new_act = int(bin_index, 2)
            valids[old_index], valids[new_act] = valids[new_act], valids[old_index]
        
        return new_action

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        while self.game.getGameEnded(board, curPlayer) == 0:
            it += 1
            if verbose:
                assert self.display
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.display(board)
            action = players[curPlayer +
                             1](self.game.getCanonicalForm(board, curPlayer))

            valids = self.game.getValidMoves(
                self.game.getCanonicalForm(board, curPlayer), 1)
            
            if curPlayer == -1: action = self.changeValues(action, valids)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
        if verbose:
            assert self.display
            print("Game over: Turn ", str(it), "Result ",
                  str(self.game.getGameEnded(board, 1)))
            self.display(board)
        return curPlayer * self.game.getGameEnded(board, curPlayer)

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """

        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult = self.playGame(verbose=verbose)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1

        return oneWon, twoWon, draws
