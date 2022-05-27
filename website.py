# streamlit run website.py

# Installed Libraries
from streamlit_option_menu import option_menu

# Locally created libraries
from Python.loadimg import loadImg
from Python.backgroundremoval import bgRemove
from Python.grayscale import grayScale
from Python.translate import changeDimensionsImg
from Python.rotate import rotations
from Python.blur import imgS
from Python.edgedetection import imgT
from streamlit_image_comparison import image_comparison

# Utils
import time
import os
import streamlit as st
timestr = time.strftime("%Y%m%d-%H%M%S")

# Remove .streamlit from page title tag
st.set_page_config(
   page_title="Transform Image",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

# Custom Method to find extension of a file name
def extensionFileName(file_name):
    __EXTENSION = ""
    if file_name[len(file_name) - 3:] == "png" or file_name[len(file_name) - 3:] == "jpg" or file_name[len(file_name) - 3:] == "bmp":
        __EXTENSION += file_name[len(file_name) - 3:]
    elif file_name[len(file_name) - 4:] == "jpeg":
        __EXTENSION += file_name[len(file_name) - 4:]
    return "." + __EXTENSION

# delete image after use
def remove_img(path, img_name):
    os.remove(path + '/' + img_name)
    # check if file exists or not
    if os.path.exists(path + '/' + img_name) is False:
        # file did not exists
        return True
    else: 
        return False

# Creates a sidebar navigation panel
with st.sidebar:
    selected = option_menu("Main Menu", ["Help", "Upload", 'Remove Background', 'GrayScale', 'Edit Image', 'Download', 'Remove Images'], 
        icons=['info-square', 'file-earmark-arrow-up', 'wrench', '', '', 'download', 'trash2'], menu_icon="cast", default_index=1)
    selected

# When "Help" button is clicked on Side bar navigation panel
if selected == "Help":
    st.title("Welcome to Background Removal site help page")
    st.markdown("---")
    st.subheader("Step - 1 -> Click on Upload to upload an image whose background is to be removed")
    st.image("Images/help.png", width = 300)
    st.markdown("---")
    st.subheader("Step - 2 -> Click on Browse files and upload a desired file")
    st.image("Images/help1.png", width = 700)
    st.markdown("---")
    st.subheader("Step - 3 -> Click on an option such as \"Remove Background\" from Side panel to start selected processing style upon an uploaded image")
    st.image("Images/help2.png", width = 300)
    st.markdown("---")
    st.subheader("Step - 4 -> Click on download button to download desired image")
    st.image("Images/help3.png", width = 300)
    st.markdown("---")
    st.caption("Note -> Before downloading you can view image to be downloaded")

# When "Upload" button is clicked on Side bar navigation panel
if selected == "Upload":
    st.title("Upload an Image")
    image_file = st.file_uploader("Upload Images", type = ["png", "jpg", "jpeg", "bmp"])
    if image_file is not None:
        # To See details
        # file_details = {"filename":image_file.name, "filetype":image_file.type, "filesize":image_file.size}
        # st.write(file_details)
        
        # To View Uploaded Image
        # st.image(image_file, width = 250)
        st.image(image_file, width = 300)
        
        #Saving upload
        __EXTENSION = extensionFileName(image_file.name)
        with open(os.path.join("Images/", "upload" + __EXTENSION), "wb") as f:
        
        # with open(os.path.join("Images/Uploaded_Image", image_file.name), "wb") as f:
            f.write((image_file).getbuffer())
            st.success("File Saved")
            
            # Writing file name into a text file
            text_file = open("texts/file_name.txt", "w") # open text file
            text_file.write(image_file.name) # write string to file
            text_file.close() # close file

# When "Remove Background" button is clicked on Side bar navigation panel
if selected == "Remove Background":
    st.title("Removing Background!")
    
    # Check for Wether image is uploaded or not!
    try:
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file

        # open text file in read mode
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file
        
        # Loading file name from a text file
        __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
        __FILE_WITH_EXTENSION = __PATH + "upload" + __EXTENSION
        
        # Convert to Background removed image
        LI = loadImg(__FILE_WITH_EXTENSION)
        IMG = LI.getImg()
        BR = bgRemove(IMG, __FILE_WITH_EXTENSION)    
        __BG_REMOVE_IMG = BR.removeBG()
        LI.imgSave(__BG_REMOVE_IMG, "bgremove" + __EXTENSION, "Images/")
        # st.image("Images/bgremove" + __EXTENSION, width = 300)
        image_file = "bgremove" + __EXTENSION
        
        # Saving Background removed image name with extension to a text file
        LI.imgSave(__BG_REMOVE_IMG, image_file, "Images/")
        st.success("File Saved")

        # render image-comparison
        image_comparison(
            img1 = "Images/upload" + __EXTENSION,
            img2 = "Images/bgremove" + __EXTENSION,
            width = 500
        )
    except:
        st.error('Please upload an image in Upload Section')
        st.image("Images/help.png")

# When "GrayScale" button is clicked on Side bar navigation panel
if selected == "GrayScale":
    st.title("GrayScale!")
    
    # Check for Wether image is uploaded or not!
    try:
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file

        # open text file in read mode
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file
        
        # Loading file name from a text file
        __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
        __FILE_WITH_EXTENSION = __PATH + "upload" + __EXTENSION
        
        # Convert to grayscale image
        LI = loadImg(__FILE_WITH_EXTENSION)
        IMG = LI.getImg()
        GS = grayScale(IMG, __FILE_WITH_EXTENSION)
        __GRAYSCALE_IMG = GS.grayImg()
        LI.imgSave(__GRAYSCALE_IMG, "grayscale" + __EXTENSION, "Images/")
        # st.image("Images/grayscale" + __EXTENSION, width = 300)
        image_file = "grayscale" + __EXTENSION
        
        # Saving Background removed image name with extension to a text file
        LI.imgSave(__GRAYSCALE_IMG, image_file, "Images/")
        st.success("File Saved")

        # render image-comparison
        image_comparison(
            img1 = "Images/upload" + __EXTENSION,
            img2 = "Images/grayscale" + __EXTENSION,
            width = 500
        )
    except:
        st.error('Please upload an image in Upload Section')
        st.image("Images/help.png")

# When "Edit Image" button is clicked on Side bar navigation panel
if selected == "Edit Image":
    st.title("Edit Uploaded Image!")
    
    option = st.selectbox(
        'Which Opeartion to Perform?',
        ('None', 'Translate', 'Rotate', 'Blurr', 'Detect Edges')
    )
    st.info('Select and option from drop down')

    # When "Translate" option is selected from Drop Down menu
    if option == 'Translate':
        # Check for Wether image is uploaded or not!
        try:
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file
            
            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "upload" + __EXTENSION
            
            # Convert to grayscale image
            LI = loadImg(__FILE_WITH_EXTENSION)
            IMG = LI.getImg()
            CDI = changeDimensionsImg(50, 50, IMG, __FILE_WITH_EXTENSION)
            __TRANSLATED_IMG = CDI.translateImg()
            LI.imgSave(__TRANSLATED_IMG, "translate" + __EXTENSION, "Images/")
            # st.image("Images/translate" + __EXTENSION, width = 300)
            image_file = "translate" + __EXTENSION
            
            # Saving Background removed image name with extension to a text file
            LI.imgSave(__TRANSLATED_IMG, image_file, "Images/")
            st.success("File Saved")

            # render image-comparison
            image_comparison(
                img1 = "Images/upload" + __EXTENSION,
                img2 = "Images/translate" + __EXTENSION,
                width = 500
            )
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")
    
    # When "Rotate" option is selected from Drop Down menu
    elif option == 'Rotate':
        # Check for Wether image is uploaded or not!
        try:
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file
            
            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "upload" + __EXTENSION
            
            # Convert to Rotated image
            LI = loadImg(__FILE_WITH_EXTENSION)
            IMG = LI.getImg()
            RTS = rotations(IMG, 45, __FILE_WITH_EXTENSION)
            __ROTATIONS_IMG = RTS.rotateImg()
            LI.imgSave(__ROTATIONS_IMG, "rotate" + __EXTENSION, "Images/")
            # st.image("Images/rotate" + __EXTENSION, width = 300)
            image_file = "rotate" + __EXTENSION
            
            # Saving Rotated image name with extension to a text file
            LI.imgSave(__ROTATIONS_IMG, image_file, "Images/")
            st.success("File Saved")

            # render image-comparison
            image_comparison(
                img1 = "Images/upload" + __EXTENSION,
                img2 = "Images/rotate" + __EXTENSION,
                width = 500
            )
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

    # When "Blurr" option is selected from Drop Down menu
    elif option == 'Blurr':
        # Check for Wether image is uploaded or not!
        try:
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file
            
            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "upload" + __EXTENSION
            
            # Convert to Blurred image
            LI = loadImg(__FILE_WITH_EXTENSION)
            IMG = LI.getImg()
            BLR = imgS(IMG, __FILE_WITH_EXTENSION)
            __BLURR_IMG = BLR.imgAverageSmoothing((3, 3))
            LI.imgSave(__BLURR_IMG, "median" + __EXTENSION, "Images/")
            # st.image("Images/median" + __EXTENSION, width = 300)
            image_file = "median" + __EXTENSION
            
            # Saving Rotated image name with extension to a text file
            LI.imgSave(__BLURR_IMG, image_file, "Images/Blurr")
            st.success("File Saved")

            # render image-comparison
            image_comparison(
                img1 = "Images/upload" + __EXTENSION,
                img2 = "Images/median" + __EXTENSION,
                width = 500
            )
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

    # When "Detect Edges" option is selected from Drop Down menu
    elif option == 'Detect Edges':
        # Check for Wether image is uploaded or not!
        try:
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file
            
            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "upload" + __EXTENSION
            
            # Convert to Edge Detected image
            LI = loadImg(__FILE_WITH_EXTENSION)
            IMG = LI.getImg()
            DTE = imgT(IMG, __FILE_WITH_EXTENSION)
            __GRAYSCALE_IMG = grayScale(IMG, __FILE_WITH_EXTENSION).grayImg()
            __DETECT_IMG = DTE.imgCan("")
            LI.imgSave(__DETECT_IMG, "detect" + __EXTENSION, "Images/")
            # st.image("Images/detect" + __EXTENSION, width = 300)
            image_file = "detect" + __EXTENSION
            
            # Saving Rotated image name with extension to a text file
            LI.imgSave(__DETECT_IMG, image_file, "Images/")
            st.success("File Saved")

            # render image-comparison
            image_comparison(
                img1 = "Images/upload" + __EXTENSION,
                img2 = "Images/detect" + __EXTENSION,
                width = 500
            )
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

# When "Download" button is clicked on Side bar navigation panel
if selected == "Download":
    st.title("Download the uploaded and processed image")
    
    option = st.selectbox(
        'Which Image to Download?',
        ('None', 'Background Removed', 'GrayScale', 'Translate', 'Rotate', 'Blurr', 'Detect Edges')
    )

    # When "Background Removed" option is selected from Drop Down menu
    if option == 'Background Removed':
    # Check for Wether image is uploaded or not!
        try:
            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "bgremove" + __EXTENSION
            st.image(__FILE_WITH_EXTENSION, width = 300)
        
            # Button to click and download image
            __UPLOAD = __PATH + "bgremove" + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = "Background Removed " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                ) 
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

    # When "GrayScale" option is selected from Drop Down menu
    elif option == 'GrayScale':
    # Check for Wether image is uploaded or not!
        try:
            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "grayscale" + __EXTENSION
            st.image(__FILE_WITH_EXTENSION, width = 300)
        
            # Button to click and download image
            __UPLOAD = __PATH + "grayscale" + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = "GrayScale " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                ) 
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

    # When "Translate" option is selected from Drop Down menu
    if option == 'Translate':
    # Check for Wether image is uploaded or not!
        try:
            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "translate" + __EXTENSION
            st.image(__FILE_WITH_EXTENSION, width = 300)
        
            # Button to click and download image
            __UPLOAD = __PATH + "translate" + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = "translate " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                ) 
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

    # When "Rotate" option is selected from Drop Down menu
    if option == 'Rotate':
    # Check for Wether image is uploaded or not!
        try:
            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "rotate" + __EXTENSION
            st.image(__FILE_WITH_EXTENSION, width = 300)
        
            # Button to click and download image
            __UPLOAD = __PATH + "rotate" + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = "rotate " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                ) 
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

    # When "Blurr" option is selected from Drop Down menu
    if option == 'Blurr':
    # Check for Wether image is uploaded or not!
        try:
            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "median" + __EXTENSION
            st.image(__FILE_WITH_EXTENSION, width = 300)
        
            # Button to click and download image
            __UPLOAD = __PATH + "median" + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = "Blurred " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                ) 
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

    # Detect Edges
    # When "Detect Edges" option is selected from Drop Down menu
    if option == 'Detect Edges':
    # Check for Wether image is uploaded or not!
        try:
            # open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "detect" + __EXTENSION
            st.image(__FILE_WITH_EXTENSION, width = 300)
        
            # Button to click and download image
            __UPLOAD = __PATH + "detect" + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = "Edge Detected " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                ) 
        except:
            st.error('Please upload an image in Upload Section')
            st.image("Images/help.png")

# When "Remove Images" button is clicked on Side bar navigation panel
if selected == "Remove Images":
    # Check for Wether image is uploaded or not!
    try:
        # open text file in read mode
        text_file = open("texts/file_name.txt", "r")
        __FILE_NAME = text_file.read() # read whole file to a string
        text_file.close() # close file
            
        # Loading file name from a text file
        __EXTENSION = extensionFileName(__FILE_NAME)

        # Remove Original Image
        if remove_img("Images/", "upload" + __EXTENSION):
            # Print successfull deletion text
            st.title("Suceessfully removed Uploaded image, please upload images again!")
            st.balloons()

        # Remove "Background removed" image
        remove_img("Images/", "bgremove" + __EXTENSION)
        
        # Remove "Grayscale" image
        remove_img("Images/", "grayscale" + __EXTENSION)
        
        # Remove "Translate" image
        remove_img("Images/", "translate" + __EXTENSION)

        # Remove "Rotate" image
        remove_img("Images/", "rotate" + __EXTENSION)

        # Remove "Blurr" image
        remove_img("Images/", "median" + __EXTENSION)

        # Remove "Detected Edge" image
        remove_img("Images/", "detect" + __EXTENSION)

    except:
        st.error('Please upload an image in Upload Section')
        st.image("Images/help.png")