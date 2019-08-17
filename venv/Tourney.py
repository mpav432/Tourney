import random
import names
import copy

'''This program simulates a tournement with four categories of games.  Players are randomly matched with eachother to play in scrums of 4 in either 2v2 or FFA games.  
If scrums of 4 cannot be formed, matchmaking will assign a bye to leftover players.  Players with the least byes have priority selection for bye assignment. Players are
otherwise assigned to play in their least played category, assuring broad distribution.

Two primary data set are created.  [players], and [scrums].  

[players] stores all information relating to a single participant in the structure [['Name'],[[Points r1],[Points r2]...],[[Lawn Games Played],[Bar Games Played]...]] 
[scrums] divides the players into the 5 possible categories of games [[Players in Lawn],[Players in Bar],[Players in Board],[Players in Video],[Players in Bye]]

The user selects an operation to carry out on the data sets.  The datasets are passed to these functions, modified, and returned.  The available operations are below:

[M]odify roster - Add or remove players from the sitting out list.  These players will be ignored by matchmaking and recieve a bye for the round. 
[P]erform matchmaking - Create scrums of 4 and assign them to a category of game.  Leftover players receive a bye
[A]ward points - Select a game to resolve and assign points to the winner.
[G]et new games - Reselect the game sets if they are not satisfactory.  Does not change teams.
[E]nd the round - Move on to the next round when all points have been awarded.
[D]isplay player stats - Display the name, scores, and game history for each player
[O]verwrite player score - Edit a players score through the current round
[R]estore game to previous round - Revert the game to a previous round.

At the end of the desired number of rounds, the game ends and a champion is chosen.
'''

def init_players(): #Initializes the player list using either randomly generated or user inputed names.
    while True:

        try:
            num_players = int(input('How Many Players? '))
            break
        except:
            print("That's not a number, enter a number of players")
    #num_players = 21
    print()
    name = [None]*num_players
    random_names = input('Randomly Generate Names? y/n: \n')
    if random_names == 'y':

        name = [names.get_first_name() for i in range(num_players)]

        for i in range(num_players):  # this loops ensures there are no duplicate names from the random generation
            if name.count(name[i])>1:
                name[i] = names.get_first_name()
                i = 0

    else:
        print("Enter everyone's name one at a time")
        for i in range(num_players):
            name[i] = input('Enter Next Player: \n')
    players = [[name[i],[],[[],[],[],[],[]]] for i in range(num_players)] #The players list has the structure [['Name'],[[Points r1],[Points r2]...],[[Lawn Games Played],[Bar Games Played]...]]
    return players
def init_scrums():  #resets the scrums list which stores information on which player is assigned to each category each round
    return [[], [], [], [], []]  # structure for scrums list is [[Lawn],[Bar],[Board],[Video],[Bye]]
def fill_scrums(players,roster,scrums,players_absent):  #Takes the active player list and assignes each player to a category
    scrums = init_scrums()
    players_absent_index = sorted([i for i in range(len(players)) if players[i][0].lower() in players_absent],
                                  reverse=True)
    [scrums[-1].append(players[i]) for i in players_absent_index]
    draw_pool = roster.copy()
    num_players = len(draw_pool)
    num_teams = int(num_players/4)
    num_byes = num_players%4  #number of players left over when teams of 4 cannot be made.  

    for i in range(num_byes):  #This loop randomly assigns byes to players that have the least byes
        least_byes_in_pool = min([draw_pool[i][2][4] for i in range(len(draw_pool))])
        players_least_byes = [i for i in range(len(draw_pool)) if draw_pool[i][2][4] == least_byes_in_pool]
        player_choice = draw_pool[random.choice(players_least_byes)]
        scrums[-1].append(player_choice)  #scrums[-1] is the bye category
        draw_pool.remove(player_choice)


    for team in range(num_teams):  #This loop finds a category in which to add teams of 4 by prioritizing the least filled category
        least_category_indexes = [i for i in range(len(scrums)-1) if len(scrums[i]) == min([len(scrums[j]) for j in range(len(scrums)-1)])]
        category_to_fill_index = random.choice(least_category_indexes)  #finds the scrums with the least number of teams assigned and randomly chooses one to fill
        current_category_size = len(scrums[category_to_fill_index])

        while len(scrums[category_to_fill_index]) < current_category_size+4:  #This loop finds the players that have played least in the chosen category and randomly assignes them to the chosen category.
            min_games_played_in_category = min([draw_pool[i][2][category_to_fill_index] for i in range(len(draw_pool))])
            players_least_in_category = [i for i in range(len(draw_pool)) if draw_pool[i][2][category_to_fill_index] == min_games_played_in_category]
            player_choice = draw_pool[random.choice(players_least_in_category)]
            scrums[category_to_fill_index].append(player_choice)  #assign player to category
            draw_pool.remove(player_choice)   #remove chosen player from draw pool


    return scrums
def modify_roster(players,scrums,players_absent):  #Function asks the user if players have voluntarily left the game or returned from absence.  The roster: roster is modified accordingly.  Players sitting out is carried over to the next round until the user indicates they have returned.
    roster = players.copy()
    print()
    players_returning = []
    if players_absent != []:
        while True:
            if len(players_absent) ==1:  #Gramatic correction statement IS/ARE
                print(str(players_absent) + ' is away')  #states which player IS sitting out
            else:
                print(str(players_absent) + ' are away')  # states which players ARE sitting out
            try:
                print()
                players_returning_name = input('Did any players return?  Enter their name: \n').lower()
                print()
                while players_returning_name != '' and players_returning_name !='no' and players_returning_name !='n' and players_returning_name !='No':  #loop makes a list of the names of all returning players

                    players_absent.remove(players_returning_name)
                    print(str(players_returning_name)+' rejoins the fray!')
                    print()
                    players_returning_name = input('Did any other players return? Enter their name: \n' ).lower()
                    print()
                break
            except:
                print('That person is not away')
                print()

    players_absent_name = input('Are any players sitting out this round?  Enter their name: \n').lower()  #Asks user if any players are going to sit out this round.
    print()
    while players_absent_name != '' and players_absent_name !='no' and players_absent_name !='n' and players_absent_name !='No':
        if players_absent_name in [roster[i][0].lower() for i in range(len(roster))]:
            players_absent.append(players_absent_name)
            print()
            print(players_absent_name+' will sit out this round.')
            print()
        else:
            print()
            print('That person is not in the roster')
            print()
        players_absent_name = input('Are any other players sitting out this round?  Enter their name: \n').lower()
    players_absent_index = sorted([i for i in range(len(players)) if players[i][0].lower() in players_absent],
                                  reverse=True)  # finds the players index for people in the absent list, sorts in reverse.
    [roster.pop(i) for i in players_absent_index]   #removes the absent players from the active roster

    print(str(list([roster[i][0] for i in range(len(roster))])) + ' are in the game.')
    print()
    print('Absent players this round whom will receive a bye: '+str(players_absent))
    return [players,roster,scrums,players_absent]
def init_game():  #Asks the user how many players and rounds will be played, returns the data structures players and scrums which are operated on by the other functions.
    players = init_players()
    while True:
        try:
            num_rounds = int(input('How many rounds will be played?\n'))
            break
        except:
            print('Enter a number\n')
    scrums = init_scrums()
    return [players, scrums, num_rounds]
    #print(games_lookup)
def award_points(players,scrums,games,games_resolved):  # Asks the user which game is to be resolved and which particiapants are awarded points

    announce_round(scrums,Teams,games)
    games_unresovled = [i for i in range(len(games)) if i not in games_resolved]  #finds which games are unresolved
    print('Unresovled games: '+str([games_unresovled[i]+1 for i in range(len(games_unresovled))]))

    try:
        game_to_resolve = int(input('Which game would you like to resolve? (1-n)\n'))-1
        games_unresovled.remove(game_to_resolve)
        games_resolved.append(game_to_resolve)  #Moving game from unresolved to resovled list
        i = (game_to_resolve)*2

    except:
        print('Not a valid input, returning to menu\n')
        return players, games_resolved



    if games[int(i / 2)][1] == '2v2':     #If the game to resolve is 2v2, then 4 points are awarded to the two winners, team A or B.
        while True:
            print('Team A: ' + str(Teams[i][0]) + ' and ' + str(Teams[i][1]) + ' vs. Team B: ' + str(
                Teams[i + 1][0]) + ' and ' + str(Teams[i + 1][1]) + ' in ' + str(games[int(i / 2)]) + ' ? ')
            winner = input('Enter "A" or "B" for winner\n').lower()
            #winner = random.choice(['A', 'B'])
            if winner == 'a':
                winners_index = [j for j in range(len(players)) if
                                 players[j][0] in Teams[i]]
                losers_index = [j for j in range(len(players)) if
                                players[j][0] in Teams[i + 1]]
                [players[k][1].append(4) for k in winners_index]
                [players[k][1].append(0) for k in losers_index]

                break
            elif winner == 'b':
                winners_index = [j for j in range(len(players)) if
                                 (players[j][0] == Teams[i + 1][0] or players[j][0] == Teams[i + 1][1])]
                losers_index = [j for j in range(len(players)) if
                                (players[j][0] == Teams[i][0] or players[j][0] == Teams[i][1])]
                [players[k][1].append(4) for k in winners_index]
                [players[k][1].append(0) for k in losers_index]

                break
            else:
                print()
                print("Don't try to break me.")
                print()
        [players[k][2][Teams[i][2]].append(games[int(i / 2)]) for k in winners_index + losers_index]

    else:    #If the game to resolve is FFA, then 4 points are awarded to 1st place, 2 points to 2nd and 3rd, and 0 points to 4th.
        print('List players in decending order starting with first place: ' + str(Teams[i][0]) + ', ' + str(
            Teams[i][1]) + ', ' + str(Teams[i + 1][0]) + ', and ' + str(
            Teams[i + 1][1]) + ' in the game of ' + str(games[int(i / 2)]) + '?')
        players_in_game = [Teams[i][0].lower(), Teams[i][1].lower(), Teams[i + 1][0].lower(), Teams[i + 1][1].lower()]
        [players[k][2][Teams[i][2]].append(games[int(i / 2)]) for k in range(len(players)) if players[k][0].lower() in players_in_game]
        for k in [4, 2, 2]:
            while True:
                try:

                    place = input(str(k) + ' points are awarded to: \n').lower()
                                        #place = random.choice(players_in_game)
                    players_in_game.remove(place)
                    [players[j][1].append(k) for j in range(len(players)) if players[j][0].lower() == place]
                    break

                except:
                    print("That's not one of the available players, try again")
        [players[j][1].append(0) for j in range(len(players)) if players[j][0].lower() == players_in_game[0]] #The remaining plays recieves 0 points.


    print()


    [print(players[i][0:2]) for i in range(len(players))]  #Prints the scores
    print("Here are the scores")
    return players, games_resolved
def get_teams(scrums):  # groups the scrums into teams, which is easer to hanle for some operations.
    Teams = [[scrums[i][j][0], scrums[i][j + 1][0], i] for i in range(4) for j in
             range(0, len(scrums[i]), 2)]
    return Teams
def announce_round(scrums,Teams,games): #prints the current matchmaking and game selections.
    byes_this_round = []
    print()
    print('Round: ' + str(round))
    print()
    for i in range(0, len(Teams), 2):
        if games[int(i / 2)][1] == '2v2':
            print('Game: '+str(int(i/2)+1))
            print(str(Teams[i][0]) + ' and ' + str(Teams[i][1]) + ' will be playing ' + str(
                Teams[i + 1][0]) + ' and ' + str(Teams[i + 1][1]) + '\n' + str(games[int(i / 2)]) + ' in the ' + str(
                category_lookup[Teams[i][2]]) + ' category.\n')
        else:
            print('Game: ' + str(int(i / 2)+1))
            print(str(Teams[i][0]) + ', ' + str(Teams[i][1]) + ', ' + str(Teams[i + 1][0]) + ', and ' + str(
                Teams[i + 1][1]) + ' are in a FFA playing: \n' + str(games[int(i / 2)]) + 'in the ' + str(
                category_lookup[Teams[i][2]]) + ' category.\n')

    byes_this_round = [scrums[4][i][0] for i in range(len(scrums[-1]))]

    print()
    print("Players taking bye this round: " + str(byes_this_round))
    print()
def choose_games(scrums): #Randomly chooses games to play
    Teams = get_teams(scrums)
    games = []
    games = [games_lookup[Teams[i][2]][random.randint(0, len(games_lookup[Teams[i][2]])-1)] for i in range(0, len(Teams), 2)]
    return games
def assign_scores(players): #Asks the user which player's score needs to be updated, then allows re-writing of the score list
    num_rounds_played = len(players[0][1])
    while True:
        try:
            player_to_edit = input("Which player would you like to edit?\n").lower()
            if player_to_edit == '':
                break
            player_to_edit_index = [i for i in range(len(players)) if player_to_edit == players[i][0].lower()]
            player_to_edit_index = int(player_to_edit_index[0])
            if num_rounds_played!=0:
                for i in range(num_rounds_played):
                    new_score = int(input("What was " + str(player_to_edit) + "'s score in round " + str(i + 1) + '?\n'))
                    players[player_to_edit_index][1][i] = new_score
                break
            else:
                print('There is no score to edit')
                break


        except:
            print('That is not a player in the tournament')
    return(players)
def restore_round(players,which_round): #Asks the user which round should be restore, then looks up the players dataset for that round which is stored in players_history.  Resets all variables and restores this saved data.
    while True:
        try:
            if which_round <= len(players[0][1]) and which_round!= '':
                players = copy.deepcopy(players_history[which_round])
                round = which_round + 1
                print()
                print('Round ' + str(which_round) + ' will be restored.\n')
                print()


                return players

        except:
            print()
            print('Thats not a valid round. Back to main menu.')
            print()
            break

#initialize some lists to be used later
[players, scrums, num_rounds] = init_game()
players_absent = []
byes_list = []
game_history = [None]*(num_rounds+1)
players_history = [None]*(num_rounds+1)
players_history[0] = copy.deepcopy(players)
round = 1
#these loopup tabes define the game and rule sets to be used in the tournement, and their corresponding category.
category_lookup = {0:['Lawn'],
                   1:['Bar'],
                   2:['Board'],
                   3:['Video']}
games_lookup = {0:[['Spike Ball','2v2'],['Can Jam','2v2'],['Beer Die','2v2'],['Cornhole','2v2'],['Bocce Ball','2v2'],['Aquatic Spike Ball','2v2'],['Lawn Darts','FFA'],['Wall Ball','2v2']],
                   1:[['Darts','2v2'],['Pool','2v2'],['Quarters','2v2'],['Shuffleboard','2v2'],['Beruit','2v2'],['Air Hockey','FFA'],['Asshole','FFA'],['Pool','FFA' ]],
                   2:[['Skull','FFA'],['Startups','FFA'],['Love Letter','2v2'],['Coup','2v2'],['Dominion','FFA'],['Smallworld','2v2'],['Hearts','FFA'],['Kemps','2v2'],['Asshole','2v2']],
                   3:[['Overcooked','FFA'],['Kart 64','FFA'],['Goldeneye','FFA'],['Nidhog','FFA'],['Halo 1: Combat Evolved','2v2'],['Halo 1: Combat Evolved','FFA'],['Smash Ultimate','FFA'],['Smash Ultimate','2v2']]}

print("Welcome to the tournament.")
[print(players[i][0]) for i in range(len(players))]
print('Are ready to play')
roster = copy.deepcopy(players)
while round <= num_rounds:  #This is the primary game loop, each iteration represents one round.  Only a user action an initate the next round after all conditions are met.
    print()
    print('Round '+str(round)+' has begun!')
    print()
    scrums = init_scrums()
    games_resolved = []
    points_assigned = False
    while True:  #This loop allows the user to input un-ending commands to modify the datasets as needed for the round.  This is only broken by moving to the next round.
        print()
        print('Round '+str(round))

        user_action = input('Choose an action to perform: \n[M]odify roster\n[P]erform matchmaking\n[A]ward points\n[G]et new games\n[E]nd the round\n[D]isplay player stats\n[O]verwrite player score\n[R]estore game to previous round\n').lower()
        if user_action == 'm': #[M]odify roster - Add or remove players from the sitting out list.  These players will be ignored by matchmaking and recieve a bye for the round.
            [players, roster, scrums, players_absent] = modify_roster(players, scrums, players_absent)

        elif user_action == 'p':#[P]erform matchmaking - Create scrums of 4 and assign them to a category of game.  Leftover players receive a bye
            if points_assigned ==False:
                scrums = fill_scrums(players, roster, scrums, players_absent)
                games = choose_games(scrums)
                Teams = get_teams(scrums)
                announce_round(scrums,Teams, games)
            else:
                sure = input('Points have alrady been assigned, are you sure you want to repeat matchmaking? Scores will be deleted.\n').lower()
                if sure == 'yes':
                    games_resolved = []
                    points_assigned = False
                    players = restore_round(players,round-1)
                    scrums = fill_scrums(players, roster, scrums, players_absent)
                    games = choose_games(scrums)
                    Teams = get_teams(scrums)
                    announce_round(scrums, Teams, games)

        elif user_action == 'r':#[R]estore game to previous round
            while True:
                try:
                    which_round = int(input('Which round would you like to go back to? Enter a letter to cancel.\n'))
                    players = restore_round(players, which_round)
                    [print(players[i]) for i in range(len(players))]
                    round_looks_good = input('This is the round you want?\n').lower()
                    if round_looks_good == 'yes' or round_looks_good == 'y':
                        scrums = init_scrums()
                        points_assigned = False
                        games_resolved = []
                        round = which_round+1
                        break

                except:
                    print()
                    break
                    print()

        elif user_action == 'a': #[A]ward points - Select a game to resolve and assign points to the winner.

            if scrums==[[],[],[],[],[]]:
                print()
                print('Cannot assign points until matchmaking is complete.  Enter "p"\n')
            elif games_resolved == list(range(int(len(players)/4))):
                print()
                print('All games have been resolved. Type "E" to end the round.\n')
            else:
                [players, games_resolved] = award_points(players, scrums, games,games_resolved)
                points_assigned = True

        elif user_action == 'o': #[O]verwrite player score
            players = assign_scores(players)

        elif user_action == 'e':#[E]nd the round - Move on to the next round when all points have been awarded.

            if games_resolved == list(range(int(len(players)/4))):
                [players[k][2][4].append(['Bye', ['']]) for k in range(len(players)) if players[k] in scrums[-1]]
                [players[k][1].append(0) for k in range(len(players)) if players[k][0] in [scrums[-1][l][0] for l in range(len(scrums[-1]))]]
                break
            else:
                print()
                print('Some teams have not been assigned points, cannot continue to next round.')

        elif user_action == 'g': #[G]et new games - Reselect the game sets if they are not satisfactory.  Does not change teams.
            if scrums[0]==[]:
                print()
                print('Cannot assign games until matchmaking is complete.  Enter "p"')
            else:
                games = choose_games(scrums)
                Teams = get_teams(scrums)
                announce_round(scrums,Teams, games)

        elif user_action == 'd':#[D]isplay player stats - Display the name, scores, and game history for each player
            [print(players[i]) for i in range(len(players))]

        else:
            print("That's not a valid input.\n")

    game_history[round] = copy.deepcopy(scrums)  #saves the game history
    players_history[round] = copy.deepcopy(players) #saves the players history

    [byes_list.append(scrums[-1][i][0]) for i in range(len(scrums[-1]))]  #Add players who received a bye to the bye list.
    # These players can resolve their byes at the end of the tournemeny by either receiving one point or playing eachother
    # in a post-game scrum
    round += 1

print()
print("All players with byes: " + str(byes_list))
#print(roster)
scores = [sum(players[i][1]) for i in range(len(players))]
print(scores)
winner = [players[i][0] for i in range(len(players)) if sum(players[i][1]) >= max(scores)]

print(str(winner)+ ' is the winner!\n\n\n')
[print(players[i]) for i in range(len(players))]