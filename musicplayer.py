import os
from flask import Flask, request, render_template, redirect, url_for
from bs4 import BeautifulSoup
import requests
from urllib2 import urlopen
music_dir = 'C:/Users/LENOVO/musicplayer/static/music'

app = Flask(__name__)

def lyricseek(song_name):
        
        payload = {'search':song_name}
        r = requests.get('http://www.lyricsmode.com/search.php', params = payload)

        URL = r.url
        soup = BeautifulSoup(urlopen(URL))
        x=[]
        for link in soup.find_all('a'):
             x.append(link.get('href'))

        a=x[-1]



        r1 = requests.get('http://www.lyricsmode.com'+a)
        
        URL1 = r1.url
        soup1 = BeautifulSoup(urlopen(URL1))


        text= soup1.find_all("p", class_="ui-annotatable", id="lyrics_text")
        text=str(text)
        
        text= text.replace("</p>]","")
        text= text.replace('[<p class="ui-annotatable" id="lyrics_text">',"")
        text=text.replace("<br/>","\n")
       
        return text
        
@app.route('/')
def musicfiles():
	music_files= os.listdir(music_dir)
	number_files=0
	for f in music_files:
		if f.endswith('.mp3'):
			number_files=number_files+1
        
	return render_template("play.html", music_files=music_files, number_files=number_files)

@app.route('/<filename>')
def song(filename):
        rawname=filename.split('.')
        print rawname[0]
        text= lyricseek(rawname[0])
        
                            
        return render_template("run.html", title = filename, music_file = filename, text=text)

@app.route('/playlist', methods=['POST'])
def playlist():
        print "here I am"
        music_files= os.listdir(music_dir)
	number_files=0
	myplaylist=[]
	mylyriclist=[]
	for f in music_files:
		if f.endswith('.mp3'):
			number_files=number_files+1
        for i in range(number_files):
                check= request.form.get('checkboxname['+str(i)+']')
                if check=="on":
                        myplaylist.append(music_files[i])
                        text=lyricseek(music_files[i].split('.'))
                        mylyriclist.append(text)
        length= len(myplaylist)-1
        return render_template("playlist.html", playlist=myplaylist, lyriclist=mylyriclist, length=length)
	

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
