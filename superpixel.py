import sys
import numpy as np
import scipy.misc

def distance(p, c):
	"""
	Computes the color distance between two pixels
	"""
	s = 0
	for i in range(len(p)):
		s += (p[i] - c[i])**2
	return np.sqrt(s)

def centroid(listPixel, dim):
	"""
	Computes the centroid of the given points given as [r, g, b]
	"""
	center = np.zeros(dim)
	for pixel in listPixel:
		center = np.add(center, pixel/len(listPixel))
	return center

def superpixel(image, k, maxIter = 5):
	"""
	Computes the SLIC algorithm on an image with k**2 superpixels
	"""
	#Normalize
	image = image/255

	# Random initial centroids
	si = image.shape[0]/k
	sj = image.shape[1]/k
	randis = [int((ki+0.5)*si) for ki in range(k) for j in range(k)]
	randjs = [int((ki+0.5)*sj) for j in range(k) for ki in range(k)]
	centroidsPosition = [np.array([i,j]) for i, j in zip(randis, randjs)]
	centroids = [image[i][j] for i,j in zip(randis, randjs)]

	sk = k*k
	norm = np.sqrt(image.shape[0]**2 + image.shape[1]**2)
	# Result image
	res = np.zeros(image.shape)
	centroidMatrix = np.full((image.shape[0], image.shape[1]), -1, dtype=int)

	for iteration in range(maxIter):
		print("Computing iteration : {} / {}".format(iteration+1,maxIter))
		# Iteration assignement
		assignements = {key: [] for key in range(sk)}
		assignementsPositions = {key: [] for key in range(sk)}
		# Initialize distance to closest centroid
		distanceMatrix = np.full((image.shape[0], image.shape[1], 1), np.inf)

		# Iter on centroid and search only in a window of 2si x 2sj around centroid
		for c, ci in zip(centroids, range(sk)):
			for i in range(max(0, int(centroidsPosition[ci][0] - si)), min(image.shape[0], int(centroidsPosition[ci][0] + si))):
				for j in range(max(0, int(centroidsPosition[ci][1] - sj)), min(image.shape[1], int(centroidsPosition[ci][1] + sj))):
					pixel = image[i][j]
					ccdist = distanceMatrix[i][j]
					# Distance which takes into account distance to centroid
					cdist = distance(pixel, c) + 15*distance([i,j], centroidsPosition[ci])/norm
					if cdist < ccdist :
						distanceMatrix[i][j] = cdist
						centroidMatrix[i][j] = ci

		# Assign pixels
		for i in range(image.shape[0]):
			for j in range(image.shape[1]):
				pixel = image[i][j]
				closestCentroid = centroidMatrix[i][j]
				# Assignement
				assignements[closestCentroid].append(pixel)
				assignementsPositions[closestCentroid].append(np.array([i,j]))
				res[i][j] = centroids[closestCentroid]*255

		# Updates centroids
		for i in range(sk):
			centroids[i] = centroid(assignements[i],image.shape[2])
			centroidsPosition[i] = centroid(assignementsPositions[i],2)

		#TODO : Ensure connectivity
	return res

def help():
    print("python3.5 superpixel.py FileName.png -k int [-o resultFileName]")
    quit()

def main():
    arg = sys.argv
    if len(arg) < 4:
        help()
    elif ".png" in arg[1] or ".jpg" in arg[1] :
        fileName = arg[1]
        output = ""
        i = 2
        # Parse the command line
        while i+1 < len(arg):
            if arg[i] == "-k":
                k = int(arg[i+1])
                i+=2
            elif arg[i] == "-o":
                output = arg[i+1]
                i+=2
            else :
                help()

        if (k <= 0):
            help()
        else:
            image = scipy.misc.imread(fileName)
            res = superpixel(image, k)
            scipy.misc.imshow(res)
            if (output != ""):
            	scipy.misc.imsave(output, res)
    else:
        help()

if __name__ == '__main__':
    main()
