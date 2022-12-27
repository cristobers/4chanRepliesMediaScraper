#  ///////////////////////////////////////////
#  grabs all of the images from a 4chan thread
#  provide the thread you want to rip as the second argument:
#  python3 4chanImageRipper.py https://boards.4channel.org/g/thread/76759434
#  ///////////////////////////////////////////
import sys, os
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

updateFromThread = False

try:
	html = urlopen(sys.argv[1])
except Exception as e:
	print(e)

else:
	bs4 = BeautifulSoup(html.read(), 'html.parser') 
	postImage = bs4.findAll("a", {"class":"fileThumb"})
	length = len(postImage)
	imgDir = sys.argv[1].split('/')[-1]
	print(f"making dir {imgDir}/ and grabbing {length} replies...")

	try:
		os.mkdir(imgDir)
	except FileExistsError:
		print(f"A folder with the same name as the thread already exists, grabbing media that haven't been downloaded yet.")
		updateFromThread = True

	for i, image in enumerate(postImage):
		try:
			threadMedia = image['href'].split('/')[-1]
			if updateFromThread:
				if threadMedia in os.listdir(imgDir):
					print(f"Already downloaded {threadMedia}, skipping...")
					continue
			print(f"Grabbing: {threadMedia} \t {i+1}/{length}")
			urlretrieve(f"https://{str(image['href'].split('//')[-1])}", f"{imgDir}/{threadMedia}")
		except Exception as e:
			print(e)
