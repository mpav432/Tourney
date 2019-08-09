import random
import names

## Players Sitting Out not working


#This program simulates a tournement with four categories of games.  It evenly distributes byes and maximizes the diversity of categories played for each player.
def init_players(): #Initializes the player list using either randomly generated or inputed names.
    num_players = int(input('How Many Players? '))
    # num_players = 21
    print()
    name = [None]*num_players
    random_names = input('Randomly Generate Names? y/n: ')
    #random_names = 'y'
    if random_names == 'y':

        name = [names.get_first_name() for i in range(num_players)]

        for i in range(num_players):  # this loops ensures there are no duplicate names from the random generation
            if name.count(name[i])>1:
                name[i] = names.get_first_name()
                i = 0

    else:
        print("Enter everyone's name one at a time")
        for i in range(num_players):
            name[i] = input('Enter Next Player: ')
    players = [[name[i],[],[0,0,0,0,0]] for i in range(num_players)] #The players list has the structure ['Player Name',[number of points gained in each round],[number of games played in each category]]
    return players
    #names = ['Matt','Max','Dan','Marco', 'Jeremy', 'Milli', 'Nat', 'Jake', 'Ben', 'Chai', 'Jon','Roberto', 'Pfitsch','Sam', 'Jonny', 'Lisa', 'Robert', 'Georige', 'Chad', 'Brendan','Bob','andrew','gina','mark','paul']
def init_categories():  #resets the categories list which stores information on which player is assigned to each category each round
    return [[], [], [], [], []]  # structure for categories list is [[Lawn],[Bar],[Board],[Video],[Bye]]
def fill_categories(players_this_round,categories):  #Takes the active player list and assignes each player to a category
    draw_pool = players_this_round.copy()
    num_players = len(draw_pool)
    num_teams = int(num_players/4)
    num_byes = num_players%4  #number of players left over when teams of 4 cannot be made

    for i in range(num_byes):  #This loop randomly assigns byes to players that have the least byes
        least_byes_in_pool = min([draw_pool[i][2][4] for i in range(len(draw_pool))])
        players_least_byes = [i for i in range(len(draw_pool)) if draw_pool[i][2][4] == least_byes_in_pool]
        player_choice = draw_pool[random.choice(players_least_byes)]
        categories[-1].append(player_choice)  #categories[-1] is the bye category
        draw_pool.remove(player_choice)


    for team in range(num_teams):  #This loop finds a category in which to add teams of 4 by prioritizing the least filled category
        least_category_indexes = [i for i in range(len(categories)-1) if len(categories[i]) == min([len(categories[j]) for j in range(len(categories)-1)])]
        category_to_fill_index = random.choice(least_category_indexes)
        current_category_size = len(categories[category_to_fill_index])

        while len(categories[category_to_fill_index]) < current_category_size+4:
            min_games_played_in_category = min([draw_pool[i][2][category_to_fill_index] for i in range(len(draw_pool))])
            players_least_in_category = [i for i in range(len(draw_pool)) if draw_pool[i][2][category_to_fill_index] == min_games_played_in_category]
            player_choice = draw_pool[random.choice(players_least_in_category)]
            categories[category_to_fill_index].append(player_choice)
            draw_pool.remove(player_choice)

    for i in range(len(players_this_round)):  #This loop increments the players' category count based on which category they were placed in this round.
        for j in range(5):
            if categories[j].count(players_this_round[i]) > 0:
                players_this_round[i][2][j] += 1


    return [players_this_round,categories]
def modify_roster(players,players_sitting_out):

    players_returning = []
    if len(players)> len(players_in_game):
        while True:
            print(str(players_sitting_out) + ' are away')
            try:
                players_returning_name = input('Did any players return?  Enter their name: ').lower()
                print()
                while players_returning_name != '' and players_returning_name !='no' and players_returning_name !='n' and players_returning_name !='No':
                    players_returning.append(players_returning_name)
                    players_sitting_out.remove(players_returning_name)

                    players_returning_name = input('Did any other players return? Enter their name: ' ).lower()
                    print()
                break
            except:
                print('That person is not away')

        players_returning_index = sorted([i for i in range(len(players)) if any(
            [players[i][0].lower == players_returning[j] for j in range(len(players_returning))])], reverse=True)
        [players_in_game.append(players[i]) for i in players_returning_index]


    print(str(list(zip([players_in_game[i][0] for i in range(len(players_in_game))],[sum(players[i][1]) for i in range(len(players))])))+' are in the game.')
    print()
    players_sitting_out_name = input('Did any players leave?  Enter their name: ').lower()

    while players_sitting_out_name != '' and players_sitting_out_name !='no' and players_sitting_out_name !='n' and players_sitting_out_name !='No':
        players_sitting_out.append(players_sitting_out_name)
        players_sitting_out_name = input('Did any other players leave?  Enter their name: ').lower()


    players_sitting_out_index = sorted([i for i in range(len(players_in_game)) if any([players_in_game[i][0].lower() == players_sitting_out[j] for j in range(len(players_sitting_out))])], reverse=True)
    [players_in_game.pop(i) for i in players_sitting_out_index]

    for i in players_sitting_out_index:
        players[i][2][4] += 1

    return [players,players_in_game,[players[i][0] for i in players_sitting_out_index]]
def init_game():
    players = init_players()
    num_rounds = 8
    categories = init_categories()
    return [players, categories, num_rounds]
    #print(games_lookup)






category_lookup = {0:['Lawn'],
                   1:['Bar'],
                   2:['Board'],
                   3:['Video']}
games_lookup = {0:[['Spike Ball','2v2'],['Can Jam','2v2'],['Beer Die','2v2'],['Cornhole','2v2'],['Bocce Ball','2v2']],
                   1:[['Darts','2v2'],['Pool','2v2'],['Quarters','2v2'],['Shuffleboard','2v2'],['Beruit','2v2']],
                   2:[['Skull','FFA'],['Startups','FFA'],['Love Letter','2v2'],['Coup','2v2']],
                   3:[['Overcooked','FFA'],['Kart 64','FFA'],['Goldeneye','FFA'],['Nidhog','FFA']]}


[players, categories, num_rounds] = init_game()
players_sitting_out = []
players_in_game = players.copy()
players_with_byes = []
game_history = [None]*num_rounds
players_history = [None]*num_rounds
for round in range(num_rounds):

    [players, players_in_game,players_sitting_out] = modify_roster(players,players_sitting_out)
    [players_history[round],categories] = fill_categories(players_in_game,categories)

    Teams = [[categories[i][j][0],categories[i][j+1][0],i] for i in range(4) for j in range(0,len(categories[i]),2)]

    games = [games_lookup[Teams[i][2]][random.randint(0, len(games_lookup[Teams[i][2]])-1)] for i in range(0,len(Teams),2)]

    print()
    print('Round: ' + str(round+1))
    print()

    for i in range(0,len(Teams),2):
        if games[int(i/2)][1]=='2v2':
            print(str(Teams[i][0])+' and '+str(Teams[i][1]) + ' will be playing '+ str(Teams[i+1][0])+' and '+str(Teams[i+1][1])+ ' in '+ str(games[int(i/2)])+ ' in the ' + str(category_lookup[Teams[i][2]])+ ' category.')
        else:
            print(str(Teams[i][0])+', '+str(Teams[i][1]) + ', '+ str(Teams[i+1][0])+', and '+str(Teams[i+1][1])+ ' are in a FFA playing: '+ str(games[int(i/2)])+ 'in the ' + str(category_lookup[Teams[i][2]])+ ' category.')

    byes_this_round = [categories[4][i][0] for i in range(len(categories[4]))]+[players_sitting_out[i] for i in range(len(players_sitting_out))]
    players_with_byes += byes_this_round
    print()
    print("Players taking bye this round: " + str(byes_this_round))
    print()

    #players_in_game = players_in_game[:-1]
    print()
    print("All players with byes: " + str(players_with_byes))
#print(players_in_game)
    game_history[round] = categories
    categories = init_categories()
    print()
    for i in range(0, len(Teams), 2):
        if games[int(i / 2)][1] == '2v2':

            while True:
                print('Team A: '+str(Teams[i][0]) + ' and ' + str(Teams[i][1]) + ' vs. Team B: ' + str(Teams[i + 1][0]) + ' and ' + str(Teams[i + 1][1]) + ' in ' + str(games[int(i / 2)]) + ' ? ')
                #winner = input('Enter "A" or "B" for winner')
                winner = random.choice(['A','B'])
                if winner.upper() == 'A':
                    winners_index = [j for j in range(len(players)) if (players[j][0] == Teams[i][0] or players[j][0] == Teams[i][1])]
                    [players[k][1].append(4) for k in winners_index]
                    break
                elif winner.upper() == 'B':
                    winners_index = [j for j in range(len(players)) if (players[j][0] == Teams[i+1][0] or players[j][0] == Teams[i+1][1])]
                    [players[k][1].append(4) for k in winners_index]
                    break
                else:
                    print()
                    print("Don't try to break me.")
                    print()


        else:
            print('List players in decending order starting with first place: ' + str(Teams[i][0]) + ', ' + str(
                Teams[i][1]) + ', ' + str(Teams[i + 1][0]) + ', and ' + str(
                Teams[i + 1][1]) + ' in the game of ' + str(games[int(i / 2)]) + '?')
            for k in [4, 2, 2]:
                while True:
                    #place = input(str(k) + ' points are awarded to: ')
                    place = random.choice([Teams[i][0],Teams[i][1],Teams[i+1][0],Teams[i+1][1]])
                    if any([place.lower() == Teams[i][j].lower() for j in range(2)]) or any([place.lower() == Teams[i+1][j].lower() for j in range(2)]):
                        [players[j][1].append(k) for j in range(len(players)) if players[j][0].lower() == place.lower()]
                        break
                    else:
                        print()
                        print("Don't try to break me.")
                        print()


               




        print()
    [print(players[i]) for i in range(len(players))]
    print(sum([(sum(players[i][1])) for i in range(len(players))]))


    