from pysolman import pysolman
from trello import TrelloApi

TRELLO_API_KEY = "75f65b49a408582246f40a6116f5d23b"
TRELLO_TOKEN = "3a6204a237a6c94386b8b67627140d86c3190596b0efd66daa07b23699bd6568"
TRELLO_BOT = 'indraargentina'
TRELLO_BOARD = 'Indra'
GMAIL_USER = 'indra.company.ar'
GMAIL_PASS = 'dmctlp86'

trello = TrelloApi( TRELLO_API_KEY, TRELLO_TOKEN )

def get_idBoard( bot_name, board_name ):
    idBoard = None
    user = trello.members.get( bot_name ) 
    for ids in user['idBoards']:
        board = trello.boards.get( ids )
        if board['name'] == board_name:
            idBoard = board['id']
    return idBoard

idBoard = get_idBoard( TRELLO_BOT, TRELLO_BOARD )

solman = pysolman( GMAIL_USER, GMAIL_PASS )
solman.check_updates()

status = solman.get_status()
sgp = solman.get_pi()

indra_board = trello.boards.get_list( idBoard )

list_id = {}
for list in indra_board:
    list_id[ list['name'] ] = list['id']

for list in indra_board:
    # Actualizo las nuevas tarjetas que entran
    if list['name'] == "Estimacion":
        cards_estimacion = trello.lists.get_card( list['id'] )
        for card in cards_estimacion:
            name = card['name']
            id = card['id']
            if name[0:3] == 'RV:':
                name = "PI%s - %s"%( name[13:19], name[34:-2] )
                trello.cards.update_name( id, name )
                trello.cards.update_desc( id, '' )
                trello.cards.new_label( id, 'blue' )
                if name.lower().find('urgencia') > 0:
                    trello.cards.new_label( id, 'red' )
                if name.lower().find('emergenciA') > 0:
                    trello.cards.new_label( id, 'yellow' )
            if name[0:2] == 'PI':
                pi = name[2:8]
                if pi.isdigit():
                    if pi in sgp:
                        trello.cards.update_name( id, sgp[ pi ] )
                        trello.cards.update_idList( id, list_id['Desarrollo'] )
    if list['name'] == 'Desarrollo' or list['name'] == 'Pruebas':
        # aca estan las tarjetas trackeables
        cards = trello.lists.get_card( list['id'] )
        for card in cards:
            name = card['name']
            id = card['id']
            solman = name[0:10]
            if solman.isdigit():
                if solman in status:
                    trello.cards.update_idList( id, list_id[ status[solman] ] )
            if name[0:2] == 'PI':
                pi = name[2:8]
                if pi.isdigit():
                    if pi in sgp:
                        trello.cards.update_name( id, sgp[ pi ] )
