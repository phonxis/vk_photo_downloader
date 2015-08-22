import vk
import webbrowser
import urllib.request
from urllib.parse import urlparse, parse_qs
from os.path import isfile
import os


OWNER_ID = '17530607'
APP_ID = '4805368'
SCOPE = 'photos'

class AuthVK():
    def __init__(self,app_id,scope):
        self.app_id = app_id
        self.scope = scope

        self.auth_in_browser()
        self.parse_redirect_url()

    def auth_in_browser(self):
        url = 'https://oauth.vk.com/authorize?' \
              'client_id={app_id}&' \
              'scope={scopes}&' \
              'redirect_uri=https://oauth.vk.com/blank.html&' \
              'display=page&v=5.0&' \
              'response_type=token'.format(app_id=self.app_id,scopes=self.scope)
        webbrowser.open(url)
        print('Give access to your audio files and')
        self.redirect_url = input('Copy and paste url from address bar(click the right mouse button -> Paste) - ')

    def parse_redirect_url(self):
        parsed_URL = urlparse(self.redirect_url)
        parsed_fragment = parse_qs(parsed_URL.fragment)
        self.access_token = parsed_fragment.get('access_token')[0]

class Get_photos():
    def __init__(self,access_token):
        self.access_token = access_token
        self.owner_id = ''
        self.parse_owner()
        self.download_photos()

    def parse_owner(self):
        owner_url = input('Input owner albums URL \t(e.g.- https://vk.com/albums36080782) -- ')
        parsed_URL = urlparse(owner_url)
        if 'albums' in parsed_URL.path:
            n = parsed_URL.path.find('s')
            self.owner_id = parsed_URL.path[n+1:]
        else:
            print('You input invalid URL. Please restart program')

    def download_photos(self):
        vkapi = vk.API(access_token=self.access_token)
        buffer = {}
        select_album = ''
        photoalbums = vkapi.photos.getAlbums(owner_id=self.owner_id)
        while select_album != '0':
            print('List of albums: \n')
            for jj,i in enumerate(photoalbums['items'],start=1):
                print("{} -- Title: '{}'\t ID: {}".format(jj,i['title'],i['id']))
                buffer[str(jj)] = i['id']
            select_album = input('Select album please!(0 to exit) --- ')
            if select_album == '0':
                return
            downl_photos = vkapi.photos.get(owner_id=self.owner_id,album_id=str(buffer[select_album]))
            try:
                os.mkdir(photoalbums['items'][int(select_album)-1]['title'])
            except OSError:
                print('Directory is already exists')
            else:
                for i in range(downl_photos['count']):
                    if 'photo_2560' in downl_photos['items'][i]:
                        url = downl_photos['items'][i]['photo_2560']
                    elif 'photo_1280' in downl_photos['items'][i]:
                        url = downl_photos['items'][i]['photo_1280']
                    elif 'photo_807' in downl_photos['items'][i]:
                        url = downl_photos['items'][i]['photo_807']
                    else:
                        url = downl_photos['items'][i]['photo_604']
                    photofile = urllib.request.urlopen(url).read()
                    filename = '{}{}{}{}'.format(photoalbums['items'][int(select_album)-1]['title'],os.sep,str(i),'.jpg')
                    f = open(filename,'wb')
                    f.write(photofile)
                    f.close()
                    print('{} photos was downloaded'.format(i+1))

if __name__== '__main__':
    auth = AuthVK(APP_ID,SCOPE)
    music = Get_photos(auth.access_token)
