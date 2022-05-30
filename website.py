# streamlit run website.py

# Installed Libraries
from numpy import full
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
   page_title="Manipulate Image",
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

# Method to incorporate multiple operations
def fullMethod(FileNameWithoutExtension, ImageCaption, Operation, TextToShow, SuccessMessage, FinalFileName):
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
            
        # Load image as an array for OpenCV operations
        LI = loadImg(__FILE_WITH_EXTENSION)
        IMG = LI.getImg()

        if Operation == 1:
            BR = bgRemove(IMG, __FILE_WITH_EXTENSION)    
            Value = BR.removeBG()
        if Operation == 2:
            GS = grayScale(IMG, __FILE_WITH_EXTENSION)
            Value = GS.grayImg()
        if Operation == 3:
            CDI = changeDimensionsImg(50, 50, IMG, __FILE_WITH_EXTENSION)
            Value = CDI.translateImg()
        if Operation == 4:
            RTS = rotations(IMG, 45, __FILE_WITH_EXTENSION)
            Value = RTS.rotateImg()
        if Operation == 5:
            BLR = imgS(IMG, __FILE_WITH_EXTENSION)
            Value = BLR.imgAverageSmoothing((3, 3))
        if Operation == 6:
            DTE = imgT(IMG, __FILE_WITH_EXTENSION)
            Value = DTE.imgCan("")

        # Saving processed image
        LI.imgSave(Value, FileNameWithoutExtension + __EXTENSION, "Images/")

        # st.image("Images/<FileNameWithoutExtension>" + __EXTENSION, width = 300)
        image_file = FileNameWithoutExtension + __EXTENSION
            
        # Saving Background removed image name with extension to a text file
        LI.imgSave(Value, image_file, "Images/")

        colx, coly = st.columns(2)
        # if Slider button is clicked
        with colx:
            x = st.button('Slider Image Comparision')
        # if Parallel button is clicked
        with coly:
            y = st.button('Parallel Image Comparision?')
                
        with st.container():
            if x:
                st.text("Images Comparision using Slider")
                # render image-comparison
                image_comparison(
                    img1 = "Images/upload" + __EXTENSION,
                    img2 = "Images/" + FileNameWithoutExtension + __EXTENSION,
                    width = 400
                )
                st.success(SuccessMessage + "!!!")
            if y:
                # Putting Columns based Viweing Experience if clicked on "Parallel Image Comparision?"
                col1, col2 = st.columns(2)
                with col1:
                    st.text("Original Image - ")
                    st.image("Images/upload" + __EXTENSION, caption = 'Original Image', width = 400)
                with col2:
                    st.text(TextToShow + "Image - ")
                    st.image("Images/" + FileNameWithoutExtension + __EXTENSION, caption = ImageCaption, width = 400)
                st.success(SuccessMessage + "!!!")
                
            # if Download button is clicked
            # - open text file in read mode
            text_file = open("texts/file_name.txt", "r")
            __FILE_NAME = text_file.read() # read whole file to a string
            text_file.close() # close file

            # Loading file name from a text file
            __PATH, __EXTENSION = "Images/", extensionFileName(__FILE_NAME)
            __FILE_WITH_EXTENSION = __PATH + "FileNameWithoutExtension" + __EXTENSION
                
            # Button to click and download image
            __UPLOAD = __PATH + FileNameWithoutExtension + __EXTENSION
            with open(__UPLOAD, "rb") as file:
                btn = st.download_button(
                    label = "Download image",
                    data = file,
                    file_name = FinalFileName + " " + __FILE_NAME,
                    mime = "image/" + __EXTENSION
                )
    except:
        st.error('Please upload an image in Upload Section')
        st.image("Images/help.png")

# Creates a sidebar navigation panel
with st.sidebar:
    selected = option_menu("Manipulation Menu", ["Help", "Home Page", "Upload", 'Remove Background', 'GrayScale', 'Edit Image', 'Remove Images'], 
        icons = ['info-square', 'house-door', 'file-earmark-arrow-up', 'wrench', '', '', 'trash2'], menu_icon = "cast", default_index = 1)
    selected

# When "Help" button is clicked on Side bar navigation panel
if selected == "Help":
    st.title("Help Site")
    st.markdown("---")
    st.subheader("Step - 1 -> Click on Upload to upload an image")
    st.image("Images/help.png", width = 300)
    st.markdown("---")
    st.subheader("Step - 2 -> Click on Browse files and upload a desired file")
    st.image("Images/help1.png", width = 900)
    st.markdown("---")
    st.subheader("Step - 3 -> Click on an option such as \"Remove Background\" from Side panel to start selected processing style on an uploaded image")
    st.image("Images/help2.png", width = 300)
    st.markdown("---")
    st.subheader("Step - 4 -> Click on Either button to view images accordingly")
    st.image("Images/help3.png", width = 700)
    st.markdown("---")
    st.subheader("Step - 5 -> Click on download button to download desired image")
    st.image("Images/help4.png", width = 200)
    st.markdown("---")
    st.caption("Note -> Before downloading you can view image to be downloaded")

if selected == "Home Page":
    st.title("Welcome to Vivek's Image Manipulation Web Site")

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

# Opeartions for fullMethod(operations = *)
# * is replaced by a number, 
# 1 - Remove Background
# 2 - Grayscale
# 3 - Translate/Displacement
# 4 - Rotate
# 5 - Blurr
# 6 - Edge Detection

# When "Remove Background" button is clicked on Side bar navigation panel
if selected == "Remove Background":
    st.title("Removing Background!")
    fullMethod(
        "bgremove", "Background Removed Image", 1, 
        "Backgorund Removed ", "Background Removed", "Background Removed"
    )

# When "GrayScale" button is clicked on Side bar navigation panel
if selected == "GrayScale":
    st.title("GrayScale!")
    fullMethod(
        "grayscale", "Grayscale Image", 2, 
        "Grayscale ", "Grayscale Image generated", "Grayscale"
    )

# When "Edit Image" button is clicked on Side bar navigation panel
if selected == "Edit Image":
    st.title("Edit Uploaded Image!")
    
    option = st.selectbox(
        'Which Opeartion to Perform?',
        ('None', 'Translate', 'Rotate', 'Blurr', 'Detect Edges')
    )

    # When "Translate" option is selected from Drop Down menu
    if option == 'Translate':
        fullMethod(
            "translate", "Move/Displace Image", 3, 
            "Moved/Displaced ", "Image Moved/Displaced", "Moved_Displaced"
        )

    # When "Rotate" option is selected from Drop Down menu
    elif option == 'Rotate':
        fullMethod(
            "rotate", "Rotated Image", 4,
            "Rotated ", "Image Rotated", "Rotated"
        )

    # When "Blurr" option is selected from Drop Down menu
    elif option == 'Blurr':
        fullMethod(
            "median", "Blurred Image", 5,
            "Blurred ", "Image Blurred", "Blurred"
        )

    # When "Detect Edges" option is selected from Drop Down menu
    elif option == 'Detect Edges':
        fullMethod(
            "detect", "Edge Detected Image", 6,
            "Edge Detected ", "Image Edge Detected", "Edge Detected"
        )
        
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