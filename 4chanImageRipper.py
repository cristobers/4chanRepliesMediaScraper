# ///////////////////////////////////////////
# grabs all of the images from a 4chan thread
# provide the thread you want to rip as the second argument:
# `python3 4chanImageRipper.py https://boards.4channel.org/g/thread/76759434`
# ///////////////////////////////////////////
import sys, os
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup


try:
	html = urlopen(sys.argv[1])
except Exception as e:
	print(e)
else:
	bs4 = BeautifulSoup(html.read(), 'html.parser') 
	postImage = bs4.findAll("a", {"class":"fileThumb"})
	length = len(postImage)
	imgDir = sys.argv[1].split('/')[-1]
	
	print(f"making dir: {imgDir} and grabbing {length} images...")
	os.mkdir(imgDir)

	for i, image in enumerate(postImage):
		try:
			imageName = image['href'].split('/')[-1]
			print(f"Grabbing: {imageName} \t {i+1}/{length}")
			urlretrieve(f"https://{str(image['href'].split('//')[-1])}", f"{imgDir}/{imageName}")
		except Exception as e:
			print(e)
