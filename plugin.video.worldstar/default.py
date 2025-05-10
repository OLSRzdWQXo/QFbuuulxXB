from urllib.parse import urlencode,parse_qsl
import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui
import requests
import re
import sys
import base64
import json
import os

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
addon_icon = addon.getAddonInfo('icon')
addon_name = '[COLOR red]Worldstar[/COLOR]'
addon_handle = int(sys.argv[1])
addon_plugin = sys.argv[0]
site_url = 'https://worldstarhiphop.com/'
json_categories_path = os.path.join(addon_path,'resources','lib','json','categories.json')
videos = []

def build_url(**kwargs):
    return "{}?{}".format(addon_plugin,urlencode(kwargs))

def add_dir(name,url,icon=addon_icon,fanart=''):
    item=xbmcgui.ListItem(label=name)
    item.setArt(
        {'icon': icon,
         'fanart': fanart,
         }
        ) 
    xbmcplugin.addDirectoryItem(addon_handle,url,item,isFolder=True)

def add_video(name,url,desc='',icon="DefaultFolder.png",fanart=''):
    item = xbmcgui.ListItem(label=name)
    item.setArt(
        {'icon': icon, 
         'fanart': fanart
         }
        )
    item.setInfo('video', {'title': name, 'tagline': desc})
    xbmcplugin.addDirectoryItem(addon_handle,url,item,isFolder=False)

def set_dir(label):
    xbmcplugin.setPluginCategory(addon_handle,label)
    xbmcplugin.setContent(addon_handle,label)

def end_dir():
    xbmcplugin.endOfDirectory(addon_handle)

def play_video(params):
    item = xbmcgui.ListItem(offscreen=False,label=params['name'])
    item.setPath(params['url'])
    xbmcplugin.setResolvedUrl(addon_handle,True,listitem=item)


def get_listings(params):
    r = requests.get(params['url'])
    text = r.text
    cat = re.search(r'<script id="__NEXT_DATA__" type="application/json">\s*(.*?)\s*</script>',text)
    js = json.loads(cat.group(1))
    resp = js['props']['pageProps']['tagVideosInitialResponse']['result']
    print(resp)
    for vid in resp:
        videos.append({'name': vid['title'], 'image': vid['imageUrl'], 'desc': vid['description'], 'url': vid['utLocation']})
    return videos

def show_listings(params):
    listings = get_listings(params)
    set_dir(params['name'])
    for li in listings:
        add_video(li['name'],build_url(action='play',name=li['name'],url=li['url']),li['desc'],li['image'])
    end_dir()

def main_menu():
    set_dir(addon_name)
    file = open(json_categories_path,'r')
    entries = json.load(file)
    for entry in entries:
        add_dir(entry['name'],build_url(mode='dir',name=entry['name'],url=entry['link']))
    end_dir()

if __name__ == "__main__":
    params = dict(parse_qsl(sys.argv[2][1:]))

    if not params:
        main_menu()
    elif params.get('mode') == 'dir':
        show_listings(params)
    elif params.get('action') == 'play':
        play_video(params)
