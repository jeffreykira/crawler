# crawler
Simple web crawler that downloads images from google and flickr.

## Python environment dependency
1. python3
2. pip install -r requirements.txt

## Get Started
1. Image keywords in classification.csv
    1. The first column is the download folder. All folders will be create in ```{project_folder}/classification_image```.
    2. The second column is the image keyword.
    3. In the same directory, the file name will be sorted by the serial number.
2. Need to put flickr key in the userdata.conf. If not, only download images from google.
3. Download up to 1000 images from google and flickr.
4. ```python crawler.py```
