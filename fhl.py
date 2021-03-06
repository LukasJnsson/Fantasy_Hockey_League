#Imported modules 
from flask import Flask, render_template, redirect, url_for, request, redirect
from datetime import date
from datetime import datetime
import database
import  flask_login 
import hashlib
from database import *
import team_rank
import play_schedual
import team_score


#Application 
FHL = Flask(__name__)


@FHL.route('/')
@flask_login.login_required
def index():
    '''
        Funktionen skickar in dagens datum till database.py för att få se om dagens datum finns i tabellen fhl_team_ranking i databasen.
        Om listan är mindre än 1 så körs fuktionen delete_team_ranking i database.py och funktionen get_team_rank i team_rank.py.

        Funktionen skickar in dagens daturm till database. py för att se om dagens datum finns i tabellen fhl_game_schedual.
        Om listan är mindre än 1 så körs funktionen delete_play_schedual i database.py och funktioen get_play_schedual från play_schedual.py

        Funktionen hämtar get_game_schedual, get_team_rank, get_fhl_highscore från database.py och skickar med dessa listor till unauthorized_index.html

        return:
            returnerar unauthorized_index.html tillsammans med lagranking, spelschema och highscore.
    '''
    todaydate = date.today()
    print(todaydate)
    rank_date_list=database.get_timestamp_fhl_team_ranking(todaydate)

    schedual_date_list=database.get_date_fhl_game_schedual (todaydate)

    if len(rank_date_list) < 1:
        database.delete_team_ranking()
        team_rank.get_team_rank()

    teams_ranking=database.get_team_rank()

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()
    highscore =database.get_fhl_highscore()
    points=get_user_points()

    return render_template('index.html', teams_ranking=teams_ranking, game_schedual=game_schedual, points=points, highscore=highscore)


FHL.secret_key='hej'
login_manager=flask_login.LoginManager()
login_manager.init_app (FHL)
@FHL.route('/login', methods=['GET', 'POST'])
def login():
    '''
        Funktionen visar html filen login.html om användaren klickar på "logga in" på webbsidan.
        Funktionen hämtar datan som användaren fyllt in när denne försöker logga in. 
        Lösenordet krypteras.
        mail och lösenord skickas in i database.py för att kolla om datan finns i databasen eller inte. 
        
        return:
            Om listan med mail och lösenord är längre än o så loggas användaren in och redirectas till index.html.
            Annars returners login.html tillsammans med ett error meddelande.
    '''

    if request.method == 'GET':
        return render_template('login.html')

    mail=request.form['mail']
    password=request.form['password']
    hash_password=hashlib.md5(password.encode()).hexdigest()
    user=database.login(mail, hash_password) 


    if len(user)>0:
        user=User()
        user.id=mail
        flask_login.login_user(user)
        return redirect('/')
            
    else:
        existing="Lösenordet du angavhör inte ihop med användarnamnet, vänligen försök igen!"
        return render_template('login.html', existing=existing)
       

class User (flask_login.UserMixin):
    pass
@login_manager.user_loader
def user_loader(mail):
    '''
        Funktionen sätter user.id till användarens mail. (En del av Flask_login)
        
        return:
            returnerar användarens mail som user.
    '''
    user = User()
    user.id = mail
    return user


@FHL.route('/logout')
def logout():
    '''
        Funktionen loggar ut användaren.
        Funktionen skickar in dagens datum till database.py för att få se om dagens datum finns i tabellen fhl_team_ranking i databasen.
        Om listan är mindre än 1 så körs fuktionen delete_team_ranking i database.py och funktionen get_team_rank i team_rank.py.

        Funktionen skickar in dagens daturm till database. py för att se om dagens datum finns i tabellen fhl_game_schedual.
        Om listan är mindre än 1 så körs funktionen delete_play_schedual i database.py och funktioen get_play_schedual från play_schedual.py

        Funktionen hämtar get_game_schedual, get_team_rank, get_fhl_highscore från database.py och skickar med dessa listor till unauthorized_index.html

        return:
            returnerar unauthorized_index.html tillsammans med lagranking, spelschema och highscore.
    '''
    flask_login.logout_user()
    todaydate = date.today()
    rank_date_list=database.get_timestamp_fhl_team_ranking(todaydate)

    schedual_date_list=database.get_date_fhl_game_schedual (todaydate)

    if len(rank_date_list) < 1:
        database.delete_team_ranking()
        team_rank.get_team_rank()

    teams_ranking=database.get_team_rank()

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()
    highscore =database.get_fhl_highscore()

    return render_template('unauthorized_index.html', teams_ranking=teams_ranking, game_schedual=game_schedual, highscore=highscore)


@login_manager.unauthorized_handler
def unauthorized_handler():
    '''
        Funktionen hanterar om användaren inte är inloggad.
        Funktionen skickar in dagens datum till database.py för att få se om dagens datum finns i tabellen fhl_team_ranking i databasen.
        Om listan är mindre än 1 så körs fuktionen delete_team_ranking i database.py och funktionen get_team_rank i team_rank.py.

        Funktionen skickar in dagens daturm till database. py för att se om dagens datum finns i tabellen fhl_game_schedual.
        Om listan är mindre än 1 så körs funktionen delete_play_schedual i database.py och funktioen get_play_schedual från play_schedual.py

        Funktionen hämtar get_game_schedual, get_team_rank, get_fhl_highscore från database.py och skickar med dessa listor till unauthorized_index.html

        return:
            returnerar unauthorized_index.html tillsammans med lagranking, spelschema och highscore.
    '''
    todaydate = date.today()
    rank_date_list=database.get_timestamp_fhl_team_ranking(todaydate)

    schedual_date_list=database.get_date_fhl_game_schedual (todaydate)

    if len(rank_date_list) < 1:
        database.delete_team_ranking()
        team_rank.get_team_rank()

    teams_ranking=database.get_team_rank()

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()
    highscore =database.get_fhl_highscore()
    return render_template('unauthorized_index.html', teams_ranking=teams_ranking, game_schedual=game_schedual, highscore=highscore)


@FHL.route('/registration', methods=['GET','POST'])
def registration():
    '''
        Funktionen ger användaren registration.html när denne klickar på "Registrera".
        Funktionen tar emot värdena som användaren fyllt i i formuläret på registration.html och skickar dessa till databasen för att som om dessa finns lagrade eller inte.
       
        Return:
            Om mailen eller användarnamnet redan finns registrerad så returneras registration.html tillbaka med felmeddelande om att mailen elelr användarnamnet redan finns registreras. 
            Annars kommer kommer användarnen in i systemet.

    '''
    if request.method == 'GET':
        return render_template('registration.html')
    
    f_name=request.form['fname']
    l_name=request.form['lname']
    mail=request.form['mail']
    username=request.form['username']
    password=request.form['password']
    hash_password=hashlib.md5(password.encode()).hexdigest()

    user=database.registrations(username, mail, f_name, l_name, hash_password)
    print(user)
    
    if len(user)>0:
        existing="Mailadressen eller användarnamnet du försökte använda finns redan, vänligen försök igen."
        return render_template('registration.html', existing=existing)
            
    else:
        user=User()
        user.id=mail
        flask_login.login_user(user)
        return redirect(('/'))
         

@FHL.route('/guide/')
def guide():
    '''
        Funktionen hämtar användarens poäng från databasen genom funktionen get_user_points.
        
        Return
            Funktionen returnerar html filen guide.htm tillsammans med den inloggade användarens poäng.
    '''
    points=get_user_points()
    return render_template('guide.html', points=points)


@FHL.route('/köp-spelare/', methods = ['GET', 'POST'])
@flask_login.login_required
def buy_players():
    '''
        När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
        Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.

        Funktion som först hämtar hur mycket poäng användaren har genon get_user_points() som finns i
        database.py och sedan hämtar alla spelare som användaren inte redan köpt och finns genom get_..._players(user_id) som också finns i 
        database.py

        När användaren sedan klickar på köp i html filen buy_players skickas ett formulär tillbaka
        med id för den spelare som ska köpas. Sedan i funktionen add_purchased_player_to_team()
        skickas spelaren och användarens id med och läggs sedan till i databasen.

        return:
            GET:
            returnerar buy_players.html med alla spelare som användaren kan köpa och dennes poäng.

            POST:
            Om användaren försöker köpa en spelare som är för dyr returneras filen fel_poäng.html tillsammans med användarens poäng.
            Om användaren köper en spelare så returneras my_players.html med alla sina köpta spelare och aktuella poäng.
            Om användaren köper en spelare som denne redan har returneras error_köp.html med användarens poäng (borde ej kunna ske.)
    '''
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)

    if len(date_list) < 1:
        print("Funktionen kommer att ta lång tid att köra, vänta ca 3 min.")
        team_score.insert_score_to_database()

    points=get_user_points()

    user_id=flask_login.current_user.id

    right_forwards = get_right_forward_players(user_id)
    centers = get_center_players(user_id)
    left_forwards = get_left_forward_players(user_id)
    defense = get_defense_players(user_id)
    goalies = get_goalie_players(user_id)
    

    if request.method == 'POST':
        try:
            user_id=flask_login.current_user.id
            player_id = request.form["id"]
            player_price = request.form["price"]
            update_points_after_bought_player(player_price, user_id)
            points_validate = get_user_points()

            if points_validate <=0:
                revert_points_after_error(player_price, user_id)
                return render_template('fel_poäng.html', points=get_user_points())

            else:
                add_purchased_player_to_team(user_id, player_id)

                return render_template('my_players.html', user_id = user_id, goalie = get_users_goalie(user_id), defenseman = get_users_defenseman(user_id),
                forward = get_users_forward(user_id), center = get_users_center(user_id), points=get_user_points())

        except:
            revert_points_after_error(player_price, user_id)
            return render_template('error_köp.html', points = get_user_points())
   
    return render_template('buy_players.html', points=get_user_points(), right_forwards = right_forwards, centers = centers,
    left_forwards = left_forwards, defense = defense, goalies = goalies)


@FHL.route('/sell', methods = ['GET', 'POST'])
@flask_login.login_required
def sell_players():
    '''
        Funktionen tillåter användaren att sälja en spelare från sitt lag. Dessutom adderas spelarens pris till användares poäng för att köpa nya spelare

        return:
            returnerar my_players.html
    '''
    if request.method == 'POST':
        user_id=flask_login.current_user.id
        player_id = request.form["id"]
        player_price = request.form["price"]
        update_points_after_sell_player(player_id, player_price, user_id)
        return redirect(url_for('my_players'))
    
    else: 
        return redirect(url_for('my_players'))


@FHL.route('/fel-köp/')
def error_purchase():
    '''
        Felhantering för när det blir något fel vid köp av spelare, användaren skickas vidare till en route som förklarar problemet
        
        return:
            Returnerar error_köp.html tillsammans med användarens poäng.
    '''
    points=get_user_points()
    return render_template('error_köp.html', points=points)


@FHL.route('/fel-poäng/')
def error_points():
    '''
    Felhantering för när det blir något fel vid köp av spelare pga för lite poäng, användaren skickas vidare till en route som förklarar problemet

    return:
        returnerar error_köp.html tillsammans med användarens poäng.

    '''
    points=get_user_points()
    return render_template('error_köp.html', points=points)


@FHL.route('/search', methods=['GET', 'POST'])
def search():
    '''
        Funktionen tar emot en sträng med ordet som användaren sökt efter i buy_player.html. 
        Sökningen skickas till database.py för att hitta i databasen.

        return
            Om listan längd som kommer från databasen är större än 0 returneras listan med sökresultat till puy_players.html tillsammans med användarens poäng.
            Annars rederectas användaren tillbaka till utgångssidan.

    '''
    user_id=flask_login.current_user.id

    if request.method =='POST':
        user_search=request.form['search']
        search_result=database.search(user_search, user_id)
    
        if len(search_result) > 0:
            
            points=get_user_points()
            return render_template('buy_players.html', points=points, search_result=search_result)
        
        else:
            print("då")
            return redirect('/köp-spelare/') 


@FHL.route('/buy', methods=['GET','POST'])
def buy():
    '''
        Om användaren vill köpa en spelare som den sökt efter kör denna funktionen. 
        Funktionen tar emot spelaren som ska köpas id samt användarens id och för in i databasen.
        
        Return
            Användaren rederectas till my_players.html
    '''
    if request.method =='POST':
        player_id = request.form['id']
        user_id=flask_login.current_user.id

        add_purchased_player_to_team(user_id, player_id)

    return redirect('/mina-spelare/')
        

@FHL.route('/spela-match/', methods= ['GET', 'POST'])
@flask_login.login_required
def play_game():
    '''
        Route för att spela match, användaren skickar via ett formulär in sitt lag och utmanar ett annat lag
        Poäng hämtas via formuläret för både användarens lag och motståndarens lag och sedan beroende på det lag som har flest
        poäng så avgörs vinnaren

        Användarens ranking och poäng avgörs genom att först kolla vem som har bäst lag och sedan genom funktionerna 
        update_points_after_win och update_ranking_after_win så får den vinnande användaren sin nya statistik

        return:
            returnerar vinnare.html med användarens nya poäng, lagets poäng och motståndarens poäng
    '''
    points=get_user_points()
    user_id=flask_login.current_user.id
    teams = get_other_users_lineup(user_id)
    my_teams = get_users_lineup(user_id)

    if request.method == 'POST':

        try:

            opponent_team_form = request.form['opponent_team'].split(", ")
            opponent_score = int(opponent_team_form[0])
            opponent_user = opponent_team_form[1]
            opponent_team_id = int(opponent_team_form[2])

            my_team_form= request.form['my_team'].split(", ")
            my_team_score = int(my_team_form[0])
            my_team_user = user_id
            my_team_id = int(my_team_form[1])

            if my_team_score > opponent_score:
                print("Du vinner!")
                winner = my_team_user
                looser = opponent_user

                print("Mitt lag")
                print(my_team_score)
                print(my_team_user)
                print(my_team_id)

                print("Motståndare")
                print(opponent_score)
                print(opponent_user)
                print(opponent_team_id)

                add_game_to_match_history(my_team_id, opponent_team_id, winner, looser)
                
                update_points_after_win(user_id)
                update_ranking_after_win(user_id)

                new_points = get_user_points()

                return render_template('vinnare.html', new_points = new_points, my_score = my_team_score, opponent_score = opponent_score)

                #Användaren får poäng

            elif my_team_score < opponent_score:
                print("Du förlorar!")
                winner = opponent_user
                looser = my_team_user

                add_game_to_match_history(my_team_id, opponent_team_id, winner, looser)

                update_points_after_win(winner)
                update_ranking_after_win(winner)

                points_loss = get_user_points()

                return render_template('förlorare.html', points = points_loss, my_score = my_team_score, opponent_score = opponent_score)
                #Andra spelaren får poäng

            else:
                
                return render_template('lika.html', points=get_user_points(), opponent_score = opponent_score, my_score = my_team_score)

        except:
            return render_template('error_game.html', points = get_user_points())

    return render_template('play_game.html', points=points, teams = teams, my_teams = my_teams)


@FHL.route('/mina-spelare/')
@flask_login.login_required
def my_players():

    """
        Den inloggade användarens mail sparas i denna: current_user.id. denna används för att ta ut saker ur databasen.
        Hämtar poäng och sedan vilka spelare som användaren har genom get_users_players() med användarens mail som 
        parameter.

        När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
        Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.

        return:
            returnerar my_players.html med användarens poäng och dennes köpta spelare

    """
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)

    if len(date_list) < 1:
        print("Funktionen kommer att ta lång tid att köra, va 3 min.")
        team_score.insert_score_to_database()

    points=get_user_points()
    user_id=flask_login.current_user.id
    goalie = get_users_goalie(user_id)
    defenseman = get_users_defenseman(user_id)
    forward = get_users_forward(user_id)
    center = get_users_center(user_id)
    return render_template('my_players.html', points=points, goalie=goalie, defenseman=defenseman, center=center, forward=forward)


@FHL.route('/match/', methods = ['GET', 'POST'])
@flask_login.login_required
def match():
    '''
        Route för att lägga ett lag, väljaren väljer via sina köpta spelare som placeras ut på positioner som sedan beräknar hur bra ens lag är
        När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
        Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.

        return:
            Om användaren sedan tidigare under dagen skapat ett lag så returneras today_match.html med användarens poäng och de spelare som användaren tidigare valt att ha med i laget.'
            Annars returneras match.html med listor med användarens köpta spelare som kan användas för att skapa ett lag.

    '''
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)
    points=get_user_points()
    user_id=flask_login.current_user.id

    if len(date_list) < 1:
        print("Hämtar nyare data från API, tar ett tag, var god vänta")
        team_score.insert_score_to_database()

    team_list=database.get_todays_team_list(todaydate, user_id)

    if len(team_list) > 0:
        left_forward=database.get_todays_left_forward(todaydate, user_id)
        right_forward=database.get_todays_right_forward(todaydate, user_id)
        list_center=database.get_todays_center(todaydate, user_id)
        left_back=database.get_todays_left_back(todaydate, user_id)
        right_back=database.get_todays_right_back(todaydate, user_id)
        goalkeeper=database.get_todays_goalie(todaydate, user_id)
        return render_template('today_match.html',points=points, left_forward=left_forward, right_forward=right_forward, list_center=list_center, left_back=left_back, right_back=right_back, goalkeeper=goalkeeper, todaydate=todaydate)
    else:
        
        goalie = get_users_goalie(user_id)
        defenseman = get_users_defenseman(user_id)
        left_wing = get_users_left_wing(user_id)
        center = get_users_center(user_id)
        right_wing = get_users_right_wing(user_id)

        if request.method == 'POST':
            left_forward_form = request.form['left_forward'].split(", ")
            left_forward_id = left_forward_form[0]

            center_form = request.form['center'].split(", ")
            center_id = center_form[0]
            
            right_forward_form = request.form['right_forward'].split(", ")
            right_forward_id = right_forward_form[0]
            
            left_defense_form = request.form['left_defense'].split(", ")
            left_defense_id = left_defense_form[0]
            
            right_defense_form = request.form['right_defense'].split(", ")
            right_defense_id = right_defense_form[0]
            
            goalie_form = request.form['goalie'].split(", ")
            goalie_id = goalie_form[0]
            
            team_name = request.form['team_name']

            user_id=flask_login.current_user.id

            add_chosen_players_to_game(left_forward_id, center_id, right_forward_id, left_defense_id, 
            right_defense_id, goalie_id, user_id, team_name)

        return render_template('match.html', points=points, goalie=goalie, defenseman=defenseman, left_wing=left_wing, center=center, right_wing=right_wing)


@FHL.route('/match-historik/')
@flask_login.login_required
def match_history():
    '''
        Route för ens matchhistorik, den hämtar samtliga vunna och förlade matcher och visar upp detta för användaren

        return:
            returnerar matchhistory tillsammans med päng och listor på vunna matcher, förlorade matcher och antal vunna och förlorade matcher, om användaren har spelat matcher.
            Annars returneras historik_fel.html med användarens poäng om inga matcher spelats eller om dessa matcher enbart vunnits eller förlorats.
    '''

    try:
        points=get_user_points()
        user_id=flask_login.current_user.id

        wins_get = get_wins(user_id)
        losses_get = get_losses(user_id)

        wins = wins_get[1]
        losses = losses_get[1]

        won_games = get_history_won_games(user_id)
        lost_games = get_history_lost_games(user_id)

        return render_template('matchhistory.html', points=points, won_games = won_games, lost_games = lost_games, wins=wins, losses=losses)

    except:
        points=get_user_points()
        return render_template('historik_fel.html', points = points)


@FHL.route('/historik-fel/')
@flask_login.login_required
def history_error():
    '''
        Felhanteringssida för om man inte skulle ha några spelade matcher i matchhistoriken

        return:
            returnerar historik_fel.html tillsammans med användarens poäng.
    '''
    points=get_user_points()
    return render_template('historik_fel.html', points = points)


@FHL.route('/top-spelare')
def top_scorer():
    points=get_user_points()
    '''
        Funktion skickar med sig en lista av lexikon players som hämtad från funktionen get_all_players som finns i 
        database.py. Denna lista sorteras sedan utifrån vad spelarkorten ska sorteras på, exempelvis mål, assist mm.

        När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
        Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.

        return:
            returnerar topscorer.html med listor på hockeyspelare som varit bäst inom de olika kategorierna.
    '''
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)

    if len(date_list) < 1:
        ("Funktionen kommer att ta lång tid att köra, ca 3 min.")
        team_score.insert_score_to_database()

    players = get_all_players()
    top_players = sorted(players, key = lambda k: k['price'], reverse=True)
    top_players =top_players[:10]
    most_goals = sorted(players, key = lambda k: k['goal'], reverse=True)
    most_goals = most_goals[:10]
    most_assists = sorted(players, key = lambda k: k['assists'], reverse=True)
    most_assists = most_assists [:10]
    most_saves= sorted(players, key = lambda k: k['saves'], reverse=True)
    most_saves=most_saves [:10]
    return render_template('topscorer.html', players = players, top_players = top_players, most_goals = most_goals, most_assists = most_assists, most_saves=most_saves, points=points)


@FHL.route('/forum/', methods = ['GET', 'POST'])
@flask_login.login_required
def forum():
    """
        Funktionen visar alla foruminlägg

        return:
            POST:
            returnerar forum.html med användarens poäng och en lista med inlägg inom en specifik kategori
            Annars returneras forum.html med användarens poäng och en lista på alla inlägg
    """
    if request.method == 'POST':
        category = request.form['category']
        points= get_user_points()
        fhldata= get_category_forum(category)
        return render_template('forum.html', points=points, fhldata=fhldata)
    else:
        points= get_user_points()
        fhldata= get_all_forum()
        return render_template('forum.html', points=points, fhldata=fhldata)


@FHL.route('/forum/mina/inlägg/', methods = ['GET', 'POST'])
@flask_login.login_required
def forum_username():
    """
        Funktionen visar enbart den inloggade användarens foruminlägg

        return:
            returnerar forum_delete.html med användarens poäng och en lista med den inloggade användarens skapade inlägg.
    """
    points=get_user_points()
    user_id=flask_login.current_user.id
    fhluserdata = get_forum_username(user_id)
    return render_template('forum_delete.html', points=points, fhluserdata=fhluserdata)


@FHL.route('/inlägg/')
@flask_login.login_required
def write_post():
    """
        Funktionen låter användaren skapa ett nytt foruminlägg

        return:
            write_post.html med användarens poäng
    """
    points=get_user_points()
    return render_template('write_post.html', points=points)


@FHL.route('/form', methods=['POST'])
def form():
    """
        Funktionen sparar ett foruminlägg till databasen
        
        return:
            rederectar användaren till forum
    """
    points=get_user_points()
    user_id=flask_login.current_user.id
    post = post_forum(user_id)
    fhldata = post_forum_redirect()
    return redirect(url_for('forum'))


@FHL.route('/forum/mina/inlägg/delete', methods = ['GET', 'POST'])
@flask_login.login_required
def delete_post():
    """
        Funktionen tar bort ett foruminlägg från databasen

        return:
            redirectar användaren till forum_username
    """
    if request.method == 'POST':
        article_id = request.form['delete']
        delete = delete_article_id(article_id)
        return redirect(url_for('forum_username'))
    else:
        return redirect(url_for('forum_username'))


@FHL.route('/forum/like', methods = ['GET', 'POST'])
@flask_login.login_required
def forum_like():
    """
        Funktionen låter användarna att gilla ett inlägg

        return:
            redirectar användaren till forum
    """
    if request.method == 'POST':
        article_id = request.form['like']
        like = like_article_id(article_id)
        points= get_user_points()
        fhldata = get_all_forum()
        return redirect(url_for('forum'))


@FHL.route('/points')
@flask_login.login_required
def get_user_points():
    ''' 
        Funktionen hämtar den inloggade användarens poäng från databasen.
        Return
            Returnerar poängen
    '''
    user_id=flask_login.current_user.id
    points=database.get_points(user_id)
    
    for i in points:
        points=i[0]
        
    
    return points


@FHL.route('/vinnare/')
def winner():
    '''
        Route som visar upp att användaren har vunnit en match

        return:
            returnerar vinnare.html med användarens poäng
    '''
    points=get_user_points()
    return render_template('vinnare.html', points=points)


@FHL.route('/förlorare/')
def looser():
    '''
        Route som visar upp att användaren har förlorat en match

        return:
            returnerar förlorare.html med användarens poäng
    '''
    points=get_user_points()
    return render_template('förlorare.html', points=points)


@FHL.route('/lika/')
def tie():
    '''
        Route som visar upp att användaren har fått lika i en match

        return:
            returnerar lika.html med användarens poäng
    '''
    points=get_user_points()
    return render_template('lika.html', points=points)


@FHL.route('/fel-match/')
def error_game():
    '''
        Route som visar upp om det blivit fel vid en match, exempelvis att ett lag inte har några poäng

        return:
            returnerar error_game.html med användarens poäng
    '''
    points=get_user_points()
    return render_template('error_game.html', points=points)


#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)   