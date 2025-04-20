import xbmcaddon,xbmcplugin,xbmcgui
import requests,json,sys
from urllib.parse import parse_qsl

ADDON=xbmcaddon.Addon()
ADDON_ICON=ADDON.getAddonInfo('icon')
ADDON_FANART=ADDON.getAddonInfo('fanart')
ADDON_HANDLE=int(sys.argv[1])
currentjson='https://yp.cdnstream1.com/metadata/7281_64k/current.json'
url='https://ais-sa1.streamon.fm/7281_64k.aac/playlist.m3u8'

def get_current_json():
    r=requests.get(currentjson)
    if r.status_code == 200:
        try:
            js=json.loads(r.text)
            if js:
                return js[0]
        except Exception as e:
            return []
    else:
        return []
n=get_current_json()

def play_krnb():
    item=xbmcgui.ListItem(offscreen=True,label=n['TIT2'],label2=n['TPE1'])
    item.setPath(url)
    xbmcplugin.setResolvedUrl(ADDON_HANDLE,True,listitem=item)

def add_dir(label,url,icon='DefaultFolder.png'):
    item=xbmcgui.ListItem(label=label)
    item.setArt({'icon': icon,'fanart': ADDON_FANART})
    xbmcplugin.addDirectoryItem(ADDON_HANDLE,url,item)

def menu():
    xbmcplugin.setPluginCategory(ADDON_HANDLE,'KRNB')
    xbmcplugin.setContent(ADDON_HANDLE,'KRNB')
    add_dir('--- PLAY STREAM BELOW ---',' ',ADDON_ICON)
    add_dir(n['TIT2']+' - '+n['TPE1'] + ' - KRNB',url,ADDON_ICON)
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

if __name__ == "__main__":
    params=dict(parse_qsl(sys.argv[2][1:]))
    if not params:
        menu()