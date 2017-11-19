import cv2
from cv2 import cv
from concurrent.futures import ThreadPoolExecutor
import sys


def compare(small_image, large_image):
	method = cv.CV_TM_SQDIFF_NORMED	
	result = cv2.matchTemplate(small_image, large_image, method)
	mn,_,mnLoc,_ = cv2.minMaxLoc(result)
	threshold = 0.25 # This should be decided using data mining
	if mn < threshold :
		return mn, mnLoc
	else:
		return -1
		
def subimage(image_path1, image_path2):
	try:
		image1 = cv2.imread(image_path1) #,0)
		image2 = cv2.imread(image_path2) #,0)
		pool = ThreadPoolExecutor(max_workers=2)
		thread1 = pool.submit(compare, image1, image2)
		thread2 = pool.submit(compare, image2, image1)
		res1 = thread1.result()
		res2 = thread2.result()
		if res1 == -1 and res2 == -1:
			return "sub image not found"
		else:
			if res1 == -1:
				return res2[1]
			else:
				if res2 == -1:
					return res1[1]
				else:
					mn1, mnloc1 = res1
					mn2, mnloc2 = res2
					if mn1 < mn2 :
						return mnloc1
					else:
						return mnloc2
	except Exception,e:
	    return "There is an exception and dtail is :\n" + str(e)
			
#print subimage('abcd.jpg','template_ccorr_3.jpg')

#print subimage('messi_face.jpg','template_ccorr_3.jpg') 
			
#print subimage('img216.jpg','template_ccorr_3.jpg')

if len(sys.argv) < 3:
	print "usage is:"
	print "python " + sys.argv[0] + " <image file 1>   <image file 2>"
print subimage(sys.argv[1], sys.argv[2])
	



 