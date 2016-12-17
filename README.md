# SuperPixel
Computes superpixels of an image.

## Article
This work is based on the article : [SLIC Superpixels](http://www.kev-smith.com/papers/SLIC_Superpixels.pdf).

## Execution
```
python3.5 superpixel.py FileName.png -k int [-o resultFileName]
```
This command computes the k**2 superpixels of the given image and saves it in the result file.  

## Results
Here some results on the testing image :  

With k = 5  
![5-5](https://raw.githubusercontent.com/Jeanselme/ImageCompression/master/Images/High5-5.png)  

With k = 10  
![10-10](https://raw.githubusercontent.com/Jeanselme/ImageCompression/master/Images/High10-10.png)  

With k = 50  
![50-50](https://raw.githubusercontent.com/Jeanselme/ImageCompression/master/Images/High50-50.png)  

With k = 100  
![100-100](https://raw.githubusercontent.com/Jeanselme/ImageCompression/master/Images/High100-100.png)  

## Libraries
Needs numpy, scipy and sys. Compiled with python3.5
