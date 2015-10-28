"""
Retrieves images from the Yale Public Figures Face Dataset and writes them out to a folder. 
The list of development set images is stored at http://www.cs.columbia.edu/CAVE/databases/pubfig/download/dev_urls.txt 
The list of evaluation set images is stored at http://www.cs.columbia.edu/CAVE/databases/pubfig/download/eval_urls.txt

Created by : Sayan Ghosh   Date: July 11, 2014  
"""

import csv
import sys
import os
import numpy as np
from urllib.request import urlopen,HTTPError,URLError
#from io import StringIO
from io import BytesIO

#import SimpleCV as cv2
from PIL import Image


class ImageDescription:
    """ 
    ImageDescription class represents a image from the PubFig dataset along with person name, image number, URL, bounding rectangle and md5sum
    Attribs:
        name : Person's name
        image_id : Image number
        url : URL where image is located
        bbox : Bounding rectangle dimensions containing only the face
        sha256 : SHA 256
    """
    def __init__(self,name,image_id,face_id,url,bbox,sha256):
        """ Class constructor """
        self.name=name
        self.image_id=image_id
        self.face_id=face_id
        self.url=url
        self.bbox=bbox
        self.sha256=sha256

    def print_image_description(self):
        """ Displays the attributes"""
        print("Person name:"+self.name)
        print("Image Number:"+self.image_id)
        print("URL :"+self.url)
        print("bbox :"+self.bbox)
        print("sha256 :"+self.sha256)

    def dump_file(self,path):    
        """ Retrieves the image from the URL and saves it in the specified path 
        Argument : 
             path : Path where the image is to be stored
        """
        # First retrieve the URL and obtain the file
        try:
            # Get image from URL
            print("Open Url0")
            url_res=urlopen(self.url,timeout=1)
            print("Open Url1")
            image=url_res.read()
            #img_array=imread(StringIO(image),flatten=True)
            print("Open Url2");
            pil_image=Image.open(BytesIO(image))
            print("Open Url3");
            url_res.close()
            print("Open Url4");
            #image_mat=create_opencv_image_from_url(self.url, 1);
            #
            # Parse the string containing the area to cut out
            rect_list=[int(z) for z in self.bbox.split(',')]
            print("Open Url5");
            #img_array_crop=image_mat[rect_list[1]:rect_list[3],rect_list[0]:rect_list[2]]
            #img_array_crop=image_mat
            img_folder=path+"\\"+self.name
            print("Open folder " + img_folder)
            os.makedirs(img_folder, exist_ok=True)
            jpg_img_string=img_folder+"\\"+self.image_id+".jpg"
            print("Open Url6");
            #imsave(jpg_img_string,img_array_crop)    
            #cv2.imsave(jpg_img_string,img_array_crop)
            print("Save to " + jpg_img_string)
            #Image.write(jpg_img_string, pil_image)
            pil_image.save(jpg_img_string)
            
            pil_image=pil_image.crop((rect_list[0],rect_list[1],rect_list[2],rect_list[3]))
            img_folder=path+"_crop\\"+self.name
            print("Open folder " + img_folder)
            os.makedirs(img_folder, exist_ok=True)
            jpg_img_string=img_folder+"\\"+self.image_id+".jpg"
            pil_image.save(jpg_img_string)
            print("Open Url7");
        except: # Errors could be due to different reasons like invalid format, or broken image links, catching all possible errors
            print(self.image_id+"   "+self.url + " has trouble !")

  
class ReadDataWriteImages:
    """
    ReadDataWriteImages class contains methods for reading in a PubFig data file description, and then writing it out to a folder
    """
    def __init__(self,datafile_name,path):
        self.datafile_name=datafile_name
        self.path=path
    def read_datafile(self):
        """ 
            This function reads in a data file description and stores it in a list of image_description objects 
        """
        description_list=[]
        with open(self.datafile_name,'rt') as file_handle:
            csv_reader=csv.reader(file_handle,delimiter='\t')
            # Skip the first row
            next(csv_reader)
            #next(csv_reader)
            # Start reading the rows
            for row in csv_reader:
                description_list.append(ImageDescription(row[0],row[1],row[2],row[3],row[4],row[5]))        
        return description_list    

    
    def write_out_images(self):
        """ 
        This function writes out images to a specified path 
        
        """
        read_list=self.read_datafile()
        for item in read_list:
            item.dump_file(self.path)    

# Process command line arguments
if __name__=="__main__":
    
    if len(sys.argv)<3:
        print ("Usage : python read_pub_fig.py datafile_name path")
    else:
        read_data_object=ReadDataWriteImages(sys.argv[1],sys.argv[2])
        read_data_object.write_out_images() 
