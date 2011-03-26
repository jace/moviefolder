MovieFolder: Get ratings and folder cover images from IMDb

Instructions:

1. sudo easy_install imdbpy beautifulsoup

2. cd ~/Movies

3. ls -1F
   Movie Name 1 (2010)/
   Movie Name 2 (1957)/
   Movie Name 3 (2011)/

4. ~/path/to/download/folder/movie-info.py

5. ls "~/Movies/By Rating"; ls "~/Movies/By Genre"

Enjoy!

Note: This code was written over two years ago for one-shot use. If you feel
it too monolithic, fork the code and modularise it. IMDb has since changed the
layout of their site, so the cover URL parser may no longer work.
