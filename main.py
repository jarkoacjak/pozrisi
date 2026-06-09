import sys
import urllib.parse
import xbmcgui
import xbmcplugin

# Získanie základných parametrov od Kodi
BASE_URL = sys.argv[0]
ADDON_HANDLE = int(sys.argv[1])
ARGS = urllib.parse.parse_qs(sys.argv[2][1:])

def get_url(**kwargs):
    """Pomocná funkcia na generovanie URL odkazov v menu"""
    return f"{BASE_URL}?{urllib.parse.urlencode(kwargs)}"

def build_main_menu():
    """Hlavné menu: Seriály a Filmy"""
    # Položka Seriály
    url_serials = get_url(action='show_serials')
    li_serials = xbmcgui.ListItem(label="Seriály")
    xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url_serials, listitem=li_serials, isFolder=True)

    # Položka Filmy
    url_movies = get_url(action='show_movies')
    li_movies = xbmcgui.ListItem(label="Filmy")
    xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url_movies, listitem=li_movies, isFolder=True)

    xbmcplugin.endOfDirectory(ADDON_HANDLE)

def show_serials():
    """Menu seriálov: Zobrazí Vikingov"""
    url = get_url(action='show_seasons', show_name='Vikingovia')
    li = xbmcgui.ListItem(label="Vikingovia")
    xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

def show_seasons(show_name):
    """Menu sérií: Zobrazí 1. Séria"""
    if show_name == 'Vikingovia':
        url = get_url(action='show_episodes', show_name='Vikingovia', season='1')
        li = xbmcgui.ListItem(label="1. Séria")
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

def show_episodes(show_name, season):
    """Menu epizód: Zobrazí 1. epizódu s priamym odkazom"""
    if show_name == 'Vikingovia' and season == '1':
        # Priamy odkaz na video (Kodi potrebuje priamy stream, ak files.fm nefunguje priamo, bude treba vyriešiť resolver)
        video_url = "https://files.fm/f/hg5f5cj8ra" 
        
        li = xbmcgui.ListItem(label="1. Epizoda")
        li.setProperty('IsPlayable', 'true') # Hovorí Kodi, že ide o spustiteľné video
        
        xbmcplugin.addDirectoryItem(handle=ADDON_HANDLE, url=video_url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

def show_movies():
    """Sekcia Filmy: Ukáže oznam 'pripravujeme'"""
    # Otvorí vyskakovacie okno (dialog) s informáciou
    dialog = xbmcgui.Dialog()
    dialog.ok("Informácia", "Pripravujeme")
    # Vráti používateľa späť do hlavného menu
    build_main_menu()

# Hlavný rozcestník (Router) doplnku
action = ARGS.get('action', [None])[0]

if action is None:
    build_main_menu()
elif action == 'show_serials':
    show_serials()
elif action == 'show_movies':
    show_movies()
elif action == 'show_seasons':
    show_name = ARGS.get('show_name')[0]
    show_seasons(show_name)
elif action == 'show_episodes':
    show_name = ARGS.get('show_name')[0]
    season = ARGS.get('season')[0]
    show_episodes(show_name, season)


