import os
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np


# class ImageViewer
#
# This project is to implment a simple Content-Based Image Retrieval system based on two
# different color histogram comparison methods
#
# This test image database includes 100 true-color images in .jpg format
# 
# Contains 2 ways for color histogram comparison: Color code method, intensity method
#
# Implemented distance metrics for histogram comparison utilizing Manhattan distance
#
# Followed basic GUI requirements to enable users to browse all images. The interface supports 
# a 'next' operation, allowing users to view images page by page, with each page displaying at 
# least 20 retrieved images
#
# AI Usage: Approximately 30 lines of code in this file were generated by ChatGPT 
# to assist in the initial creation of the frame, the binding of click events to each image, the calculations 
# for retrieving color code and intensity histograms, and the indexing for the sorted image list.
class ImageViewer:

    # init
    # The constructor
    #The constructor, sets up the main window title, dimensions, and variables
    #Defines the image folder, number of images per page, total images, and the current page
    #Initializes the selected image name as none
    # 
    def __init__(self, root):
        self.root = root
        self.root.title("Image Browser")
        self.root.geometry("1000x600")
        self.imageFolder = "images"
        self.imagesPerPage = 20
        self.totalImages = 100
        self.currentPage = 0
        self.selectedImageName = None

        # Initialized a list to store all the images from the image files, with each image named based on its order number
        self.imageList = []
        for i in range(self.totalImages):
            imagePath = os.path.join(self.imageFolder, f"{i + 1}.jpg")
            img = Image.open(imagePath)
            self.imageList.append(img)

        self.allHistograms = self.calculateHistograms()
        self.sortedImages = list(range(self.totalImages))

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame for the display of the selected image and its label
        self.selectedImageBox = tk.Frame(
            self.root, width=200, height=200, highlightbackground="white", highlightcolor="white", highlightthickness=2)
        self.selectedImageBox.pack(
            side=tk.TOP, anchor=tk.NE, padx=20, pady=20)

        self.selectedImageLabel = tk.Label(self.selectedImageBox)
        self.selectedImageLabel.pack()

        # Layout Controls
        self.navFrame = tk.Frame(self.root)
        self.navFrame.pack(side=tk.BOTTOM, fill=tk.X)

        # Up and down buttons
        # Includes label to show the current page number at the top for simplicity
        self.navButton = tk.Frame(self.navFrame)
        self.navButton.pack(side=tk.LEFT, padx=20)

        self.pageNumber = tk.Label(
            self.navButton, text=f"Page {self.currentPage + 1} / 5", font=("Arial", 12))
        self.pageNumber.pack(pady=5)

        self.prevButton = tk.Button(
            self.navButton, text="Up", command=self.upper, width=15, height=2)
        self.prevButton.pack(pady=5)

        self.nextButton = tk.Button(
            self.navButton, text="Down", command=self.under, width=15, height=2)
        self.nextButton.pack(pady=5)

        # Retrieval buttons for color code method and intensity method
        # Includes close button for closing the application and reset for returning the image grid to its defaul setting at the bottom for simplicity
        self.retrieveButton = tk.Frame(self.navFrame)
        self.retrieveButton.pack(side=tk.LEFT, padx=20)
        
        #this is for the intensity and colour code button
        self.retrieveBothButton = tk.Button(
            self.retrieveButton, text="Intensity and Color Code Method", command=self.retrieveByBothMethods, width=28, height=2)
        self.retrieveBothButton.pack(pady=5)  

        self.retrieveColorCodeButton = tk.Button(
            self.retrieveButton, text="Retrieve by Color-Code Method", command=self.retrieveByColorCode, width=28, height=2)
        self.retrieveColorCodeButton.pack(pady=5)

        self.retrieveIntensityButton = tk.Button(
            self.retrieveButton, text="Retrieve by Intensity Method", command=self.retrieveByIntensity, width=28, height=2)
        self.retrieveIntensityButton.pack(pady=5)

        self.closeButton = tk.Button(
            self.retrieveButton, text="Close", command=self.root.quit, width=28, height=2)
        self.closeButton.pack(pady=5)

        self.resetButton = tk.Button(
            self.retrieveButton, text="Reset", command=self.resetOrder, width=28, height=2)
        self.resetButton.pack(pady=5)


       # Add a Checkbutton for relevance toggle below the Up and Down buttons
        self.relevanceChecked = tk.BooleanVar()  # Variable to hold the state of the Checkbutton

        self.relevanceToggle = tk.Checkbutton(
            self.navButton, text="Relevance", variable=self.relevanceChecked, onvalue=True, offvalue=False,
            command=self.onRelevanceToggle)
        self.relevanceToggle.pack(pady=5)

        #relevant checkbox for each image
        self.relevanceState = {i: tk.BooleanVar() for i in range(self.totalImages)}


        # Displaying all images in a grid
        self.displayImages()

    # displayImages
    #
    # Displays a grid of images
    # Clears the previous grid, retrieves the images from a sorted list based on the current order
    # and arranges them in a grid
    # Binds click to each image, allowing the user to select individual images
    # Updates the page number based on the current order
    def displayImages(self):
        # Clear the existing grid before creating a new one
        for widget in self.canvas.winfo_children():
            widget.destroy()

        # Create a new grid whenever display is called
        self.grid = tk.Frame(self.canvas)
        self.canvas.create_window(
            (0, 0), window=self.grid, anchor="nw")

        # Prepare a new list of images to be displayed
        imagesToDisplay = []
        for i in self.sortedImages:
            imagesToDisplay.append(self.imageList[i])

        startIndex = self.currentPage * self.imagesPerPage
        endIndex = min(startIndex + self.imagesPerPage, len(imagesToDisplay))
        columns = 4

        # Go through all the images to display on the current page
        for i, imgIndex in enumerate(range(startIndex, endIndex)):
            img = imagesToDisplay[imgIndex]
            imgResized = img.resize((197, 143))  # Fixed size for consistency
            imgTk = ImageTk.PhotoImage(imgResized)

            # Create the grid for the current image with fixed size to avoid resizing
            imgFrame = tk.Frame(self.grid, width=200, height=200)
            imgFrame.grid_propagate(False)  # Prevent frame resizing based on contents
            imgFrame.grid(row=i // columns, column=i % columns, padx=5, pady=5)

            # Label for displaying the image
            label = tk.Label(imgFrame, image=imgTk)
            label.image = imgTk
            label.pack()

            # Name label for the image
            imageName = f"{self.sortedImages[imgIndex] + 1}.jpg"
            nameLabel = tk.Label(imgFrame, text=imageName, wraplength=200)
            nameLabel.pack()

            # Add relevance checkbox if relevance toggle is enabled
            if self.relevanceChecked.get():
                relevanceCheck = tk.Checkbutton(
                    imgFrame, text="Relevant", variable=self.relevanceState[self.sortedImages[imgIndex]])
                relevanceCheck.pack()

            # Bind click to each image
            label.bind("<Button-1>", lambda e,
                    index=self.sortedImages[imgIndex]: self.displaySelectedImage(index))

        # Update the page number label
        numPages = (self.totalImages + self.imagesPerPage - 1) // self.imagesPerPage
        self.pageNumber.config(
            text=f"Page {self.currentPage + 1} / {numPages}")



    # displaySelectedImage
    #
    # Displays the selected image
    # Resizes the selected image to fit the display area
    # Updates the name of current selected image to reflect the new one
    def displaySelectedImage(self, imgIndex):
        img = self.imageList[imgIndex]
        imgResized = img.resize((500, 470))
        imgTk = ImageTk.PhotoImage(imgResized)

        # Label selected image
        self.selectedImageLabel.configure(image=imgTk)
        self.selectedImageLabel.image = imgTk

        # Set the name of the currently selected image
        self.selectedImageName = os.path.basename(
            os.path.join(self.imageFolder, f"{imgIndex + 1}.jpg"))

    # Upper
    #
    # Navigates to the upper page of images
    # Calls displayImages() to display theupper grid
    def upper(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.displayImages()

    # Under
    #
    # Navigates to the page of images below
    # Calls displayImages() to display the grid below
    def under(self):
        if (self.currentPage + 1) * self.imagesPerPage < len(self.sortedImages):
            self.currentPage += 1
            self.displayImages()

    # calculateHistograms
    #
    # Computes and stores histograms for all images in a dictionary
    # The dictionary contains two lists for colorCode and intensity histograms
    # Accesses the dictionary by image labels
    def calculateHistograms(self):
        histograms = {}

        # Go through the list of images
        for i in range(self.totalImages):
            img = self.imageList[i]

            # Called upon colorCodeHistorgram
            histograms[f"{i + 1}.jpg"] = {
                'colorCode': self.colorCodeHistogram(img),
                'intensity': self.intensityHistogram(img)
            }
        return histograms

    # intensityHistogram
    #
    # Converts the input image to grayscale and creates a histogram with 25 bins,
    # each representing a range of pixel intensities from 0 to 255
    # Go through each pixel, sorts them into each of the 25 bins
    # Count the occurrences in each bin
    def intensityHistogram(self, img):
    # Initializes a histogram with 25 bins
        histogram = np.zeros(25, dtype=int)

        # Convert the image to RGB (if it's not already in RGB format)
        img = img.convert("RGB")

        # Create an array to hold pixels
        pixels = np.array(img)

        # Go through each pixel's RGB values and calculate the intensity
        for r, g, b in pixels.reshape(-1, 3):
            value = 0.299 * r + 0.587 * g + 0.114 * b  # Calculate the intensity using the weighted formula
            binIndex = min(int(value) // 10, 24)  # Group the value into a bin of ranges (0-9, 10-19, ..., 240-249)
            histogram[binIndex] += 1  # Increment the corresponding bin in the histogram

        return histogram

    # colorCodeHistogram
    #
    # Converts the input image to RGB and creates a histogram with 64 bins,
    # Go through each pixel RBG values, sorts them into each of the 64 bins
    # Red contributes to 16 possible bins, green contributes 4 bins,
    # and blue contributing 1 bin.
    def colorCodeHistogram(self, img):
        # Initializes a histogram with 64 bins
        histogram = np.zeros(64, dtype=int)

        # Convert the image to RGB
        img = img.convert("RGB")

        # Create an array to hold pixels
        pixels = np.array(img)

        # Go thorugh each pixel's RGB values and divide them by 64 to group them into one of 64 bins
        # Multiplies by 16 because R contributes to 16 different bins
        # Multiplies by 4 because G contributes to 4 different bins.
        for r, g, b in pixels.reshape(-1, 3):
            binIndex = (r // 64) * 16 + (g // 64) * 4 + (b // 64)
            histogram[binIndex] += 1

        return histogram

    # retrieveByIntensity
    #
    # Retrieves images sorted by their intensity histogram based on the selected image
    # calculates the Manhattan distance between the selected image's histogram and
    # those of other images.
    # Sorts by the computed distances, and the display is updated to show the sorted images
    def retrieveByIntensity(self):
        # Check if an image has been selected
        if not self.selectedImageName:
            return

        # Retrieve the histogram of the selected image and count its pixels
        selectedHistogram = self.allHistograms[self.selectedImageName]['intensity']
        numPixelsSelected = np.sum(selectedHistogram)

        distances = []

        # Go through the list of image and its histograms
        for imageName, data in self.allHistograms.items():
            if imageName == self.selectedImageName:
                continue

            histogram = data['intensity']

            # Counts up all the intensity histograms
            numPixels = np.sum(histogram)

            # Perform manhattan distance
            distance = self.manhattanDistance(
                selectedHistogram, histogram, numPixelsSelected, numPixels)

            # Get the current image index and put it into a list with its manhattan distance result
            imageIndex = int(imageName.split('.')[0]) - 1
            distances.append((imageIndex, distance))

        # Sort distances in ascending order
        distances.sort(key=lambda x: x[1])

        # Get all the newly sorted images index and intert them into the sorted list
        self.sortedImages = [index for index, _ in distances]
        selectedImageIndex = int(self.selectedImageName.split('.')[0]) - 1
        self.sortedImages.insert(0, selectedImageIndex)

        # Reset current page to 0 and refresh grid based on current order
        self.currentPage = 0
        self.displayImages()

    # retrieveByColorCode
    #
    # Retrieves images sorted by their color code histogram based on the selected image
    # calculates the Manhattan distance between the selected image's histogram and
    # those of other images.
    # Sorts by the computed distances, and the display is updated to show the sorted images
    def retrieveByColorCode(self):
        # Check if an image has been selected
        if not self.selectedImageName:
            return

        # Retrieve the histogram of the selected image and count its pixels
        selectedHistogram = self.allHistograms[self.selectedImageName]['colorCode']
        numPixelsSelected = np.sum(selectedHistogram)

        distances = []

        # Go through the list of image and its histograms
        for imageName, data in self.allHistograms.items():
            if imageName == self.selectedImageName:
                continue

            histogram = data['colorCode']

            # Counts up all the colorcode histograms
            numPixels = np.sum(histogram)

            # Perform manhattan distance
            distance = self.manhattanDistance(
                selectedHistogram, histogram, numPixelsSelected, numPixels)

            # Get the current image index and put it into a list with its manhattan distance result
            imageIndex = int(imageName.split('.')[0]) - 1
            distances.append((imageIndex, distance))

        # Sort distances in ascending order
        distances.sort(key=lambda x: x[1])

        # Get all the newly sorted images index and intert them into the sorted list
        self.sortedImages = [index for index, _ in distances]
        selectedImageIndex = int(self.selectedImageName.split('.')[0]) - 1
        self.sortedImages.insert(0, selectedImageIndex)

        # Reset current page to 0 and refresh grid based on current order
        self.currentPage = 0
        self.displayImages()

    # manhattanDistance
    #
    # Calculates the Manhattan distance between two histograms
    # takes two histograms and the total number of pixels in each histogram
    # Returns infinity to indicate 0 pixels
    # Computes the manhattan distance by summing the absolute differences of the
    # normalized histogram values.
    def manhattanDistance(self, hisA, hisB, pixelsA, pixelsB):
        if pixelsA == 0 or pixelsB == 0:
            return float('inf')

        return np.sum(np.abs(hisA / pixelsA - hisB / pixelsB))

    # resetOrder
    #
    # Resets the order of images to their original sequence from 1 to 100
    # Resets current page
    def resetOrder(self):
        self.sortedImages = list(range(self.totalImages))
        self.currentPage = 0
        self.displayImages()

    def onRelevanceToggle(self):
        """Handle relevance toggle state change."""
        if self.relevanceChecked.get():
            print("Relevance enabled")
        else:
            print("Relevance disabled")

        # Refresh the displayed images to add or remove relevance checkboxes
        self.displayImages()
        
    def intensityAndColorCodeHistogram(self, img):
        intensity = self.intensityHistogram(img).astype(float)  # Convert to float
        colorCode = self.colorCodeHistogram(img).astype(float)  # Convert to float

        # Normalize histograms by the number of pixels in the image
        imageSize = img.size[0] * img.size[1]  # Total number of pixels
        if imageSize > 0:
            intensity /= imageSize
            colorCode /= imageSize
            
        combinedHistogram = np.concatenate((intensity, colorCode))

        return combinedHistogram

    def calculateAverageHistogram(self):
        # Create an array to hold histograms for all images
        histograms = np.array([self.intensityAndColorCodeHistogram(img) for img in self.imageList])
        # Calculate and return the average histogram
        return np.average(histograms, axis=0)

    def calculateStandardDeviation(self):
        # Create an array to hold histograms for all images
        histograms = np.array([self.intensityAndColorCodeHistogram(img) for img in self.imageList])
        # Calculate and return the standard deviation
        return np.std(histograms, axis=0, ddof=1)  # Using ddof=1 for sample standard deviation

    def gaussianNormalization(self):
        averageHistogram = self.calculateAverageHistogram()
        stdDevHistogram = self.calculateStandardDeviation()
        
        # Find non-zero standard deviations
        nonZeroStdDevs = stdDevHistogram[stdDevHistogram > 0]
        
        # Calculate sti as 0.5 times the minimum of non-zero standard deviations, if any exist
        sti = 0.5 * np.min(nonZeroStdDevs) if nonZeroStdDevs.size > 0 else 0.5

        # Replace zero or negative standard deviations with sti
        adjustedStdDevHistogram = np.where(stdDevHistogram <= 0, sti, stdDevHistogram)

        normalizedHistograms = []
        
        for imgIndex, img in enumerate(self.imageList):
            combinedHistogram = self.intensityAndColorCodeHistogram(img)
            normalizedHistogram = np.zeros(89)

            # Normalize using Gaussian normalization
            for i in range(89):
                normalizedHistogram[i] = (combinedHistogram[i] - averageHistogram[i]) / adjustedStdDevHistogram[i]

            normalizedHistograms.append(normalizedHistogram)

        return normalizedHistograms

    def retrieveByBothMethods(self):
        # Check if an image has been selected
        if not self.selectedImageName:
            return

        # Get the list of Gaussian-normalized histograms for all images
        normalizedHistograms = self.gaussianNormalization()

        # Find the index of the selected image
        selectedImageIndex = int(self.selectedImageName.split('.')[0]) - 1
        selectedHistogram = normalizedHistograms[selectedImageIndex]

        # List to hold distances
        distances = []

        # Calculate distances from the selected image to all other images
        for imageIndex, normalizedHistogram in enumerate(normalizedHistograms):
            if imageIndex == selectedImageIndex:
                continue
            # Calculate Manhattan distance
            distance = np.sum(np.abs(selectedHistogram - normalizedHistogram) / 98)
            distances.append((imageIndex, distance))  # Store as (index, distance) tuple

        # Sort by distance (ascending order)
        distances.sort(key=lambda x: x[1])
            
        # Update sorted image list and display images
        self.sortedImages = [selectedImageIndex] + [index for index, _ in distances]
        self.currentPage = 0
        self.displayImages()