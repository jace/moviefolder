#!/usr/bin/env python

import os
import sys
import urllib2
import re
import imdb
from BeautifulSoup import BeautifulSoup

TITLE = re.compile('(.*), (The|A|An) ((?:- .* )?)\((\d{4})\)')

def main(argv):
    ia = imdb.IMDb()
    try: os.mkdir('By Genre')
    except OSError: pass
    try: os.mkdir('By Rating')
    except OSError: pass
    genredir = os.path.join(os.getcwd(), 'By Genre')
    ratingdir = os.path.join(os.getcwd(), 'By Rating')
    for root, dirs, files in os.walk('.'):
        if root in ['.', '..']:
            continue
        if os.path.basename(root) in ['By Genre', 'By Rating']:
            while dirs != []:
                dirs.pop(0)
            continue
        movietitle = TITLE.sub(r'\2 \1 \3(\4)', os.path.basename(root))
        if '.categorized' in files:
            print "Skipping: %s" % movietitle
        else:
            print "Looking Up: %s..." % movietitle
            movies = ia.search_movie(movietitle, results=5)
            if not movies:
                print "failed."
                continue
            elif len(movies) > 1:
                print "Found multiple movies, picking first:"
                for movie in movies:
                    print "   %s" % movie['long imdb title']
            movie = movies[0]
            ia.update(movie)
            if not 'folder.jpg' in files:
                print "Retrieving cover..."
                cover_url = movie.get('cover url', None)
                if not cover_url:
                    # Attempt to scrape it from page
                    page = urllib2.urlopen(ia.get_imdbURL(movie))
                    soup = BeautifulSoup(page)
                    cover_div = soup.find(attrs={"class": "photo"})
                    if cover_div is not None:
                        cover_url = (cover_div.find('img'))['src']
                    else:
                        cover_url = None
                if cover_url:
                    img = urllib2.urlopen(cover_url).read()
                    open(os.path.join(root, 'folder.jpg'), 'wb').write(img)
            if not 'genres.txt' in files:
                genres = [s.encode('utf-8') for s in movie.get('genres', [])]
                if genres:
                    open(os.path.join(root, 'genres.txt'), 'w').writelines([s + '\n' for s in genres])
                    for genre in genres:
                        try: os.mkdir(os.path.join(genredir, genre))
                        except OSError: pass
                        try: os.symlink('../../' + os.path.basename(root), os.path.join(genredir, genre, os.path.basename(root)))
                        except OSError: pass
            if not 'rating.txt' in files:
                rating = movie.get('rating', 0)
                if rating:
                    rating = '%.1f' % rating
                    open(os.path.join(root, 'rating.txt'), 'w').write(rating + '\n')
                    try: os.mkdir(os.path.join(ratingdir, rating))
                    except OSError: pass
                    try: os.symlink('../../' + os.path.basename(root), os.path.join(ratingdir, rating, os.path.basename(root)))
                    except OSError: pass
            open(os.path.join(root, '.categorized'), 'wb').write('')
        while dirs != []: # Don't visit subfolders.
            dirs.pop(0)

if __name__=='__main__':
    sys.exit(main(sys.argv))
