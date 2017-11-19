import cv2
from cv2 import cv
from concurrent.futures import ThreadPoolExecutor


def compare(small_image, large_image):
	method = cv.CV_TM_SQDIFF_NORMED	
	result = cv2.matchTemplate(small_image, large_image, method)
	mn,_,mnLoc,_ = cv2.minMaxLoc(result)
	if mn < 0.25 :
		return mnLoc
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
			if res1 != -1:
				return res1
			else:
				return res2
	except Exception,e:
		return str(e)
			
print subimage('abcd.jpg','template_ccorr_3.jpg')

print subimage('messi_face.jpg','template_ccorr_3.jpg') 
			
print subimage('img216.jpg','template_ccorr_3.jpg')



 