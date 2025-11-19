# README_en.md

**Language: [English](README.md), [中文](README.md).**

✨ WeixinMPTools: Your All-in-One WeChat Official Account Toolkit

📝 Introduction

WeixinMPTools is a multifunctional desktop tool designed specifically for WeChat Official Account operators. It integrates three essential functions: image splicing, cover image extraction, and image compression, aiming to streamline the content - creation and management process for WeChat Official Account operations. Whether you're a seasoned operator or just starting out, WeixinMPTools can significantly enhance your workflow efficiency.

🚀 Features

🎨 Image Stitching

- 📏 Fixed-ratio Cropping: This function enables the cropping of two images according to fixed ratios. The upper image is cropped to a 2.35:1 ratio, and the lower image is cropped to a 1:1 ratio. This ensures that the combined image has a visually appealing and harmonious layout, which is especially useful for creating consistent-style content for WeChat Official Accounts, such as article headers or promotional graphics.

- 🎨 Background Selection: Users can choose between a white or transparent background for the stitched image. A white background provides a clean and simple look, suitable for most general-purpose content. A transparent background, on the other hand, offers more flexibility in design, allowing the stitched image to blend seamlessly with different backgrounds or other elements in a layout.

🖼️ Cover Image Extraction

- 👁️ Interactive Cropping Area Drawing and Preview: An interactive cropping interface is provided. After selecting the two images, users can click the "Start Cropping" button to activate the cropping mode. In this mode, they can drag and draw a cropping frame on the preview canvas. The cropping frame is automatically locked to the preset ratios, ensuring accurate cropping. The "Preview" feature allows users to see the result of the cropping and stitching in real-time, so they can make adjustments until they are satisfied with the final look.

⚡ Image Compression

- 🔗 Link Input and Parsing: Simply input the full URL of any WeChat Official Account article (the format should be like https://mp.weixin.qq.com/s?xxxx). The tool will automatically parse the link, extracting the relevant information from the HTML code of the article page to locate the cover image.

- 

  - 📄 Single-file Compression: For single-file compression, users can select a single image and then adjust the compression quality slider, which ranges from 10 to 100. The tool will intelligently analyze the selected image and determine whether compression is necessary. This allows users to fine-tune the compression level according to their specific requirements, such as maintaining a certain level of image quality while reducing file size.

  - 📁 Batch Compression: When it comes to batch compression, the tool supports processing all the images in an entire folder (including sub-directories). This is very useful for users who have a large number of images to compress, such as a collection of product images or a series of article illustrations. By simply selecting the folder and clicking the "Batch Compression" button, they can compress all the relevant images at once.

- 

  - 🔄 Automatic Conversion to JPEG: In scenarios where transparency is not required, this option can be selected to automatically convert PNG images to JPEG format. JPEG images generally have a higher compression rate, which can significantly reduce the file size of the image, making it more suitable for web-based use, such as on WeChat Official Account articles.

  - 🔒 Maintaining PNG Format: When the transparent channel of a PNG image is crucial, users can choose to keep the PNG format during compression. This ensures that the transparency of the image is preserved, although the compression ratio may be relatively lower compared to converting to JPEG.

- 📋 Automatic Link Copying: Once the cover image is successfully identified, the tool will automatically copy the image link to the clipboard. This is extremely convenient for users who may want to use the cover image in other applications or platforms without having to manually copy the link, saving time and reducing the risk of errors.

🛠️ Usage Instructions

- 📥 Automatic Image Downloading: The cover image is automatically downloaded to the directory where the program is located. The file name follows the format cover_YYYYMMDD_HHMMSS.jpg, making it easy to organize and identify the downloaded cover images. This feature streamlines the process of obtaining cover images for WeChat Official Account operators, who can quickly access and use the images for their content creation needs.

💻 Operating Environment

- 

  - 🖱️ tkinter: A standard Python interface to the Tcl/Tk GUI toolkit. It provides the graphical user interface elements for users to interact with the tool, such as buttons, sliders, and windows.

  - 🖼️ Pillow: A fork of the Python Imaging Library (PIL), Pillow is used for opening, manipulating, and saving many different image file formats. It enables all the image-related operations in WeixinMPTools, like cropping, resizing, and format conversion.

  - 🌐 requests: This library simplifies the process of sending HTTP requests in Python. It is used to fetch the content of the WeChat Official Account article pages for cover image extraction.

  - 📋 pyperclip: It provides a cross-platform clipboard access in Python. WeixinMPTools uses it to automatically copy the cover image links to the clipboard for easy sharing and further use.

- 📦 Single-file and Batch Compression:

🔧 Installation of Dependencies

If the tool has not been packaged into an executable file, you need to install the core dependency libraries. The following steps can be used:

- 🎨 PNG Strategies:

- ⏭️ Automatic Skipping of Small Files: The tool is designed to automatically skip images that are already smaller than the set size (the default is 10MB). This prevents unnecessary compression operations on files that are already small enough, saving processing time and system resources.

1. Run the following command to install the necessary libraries:

pip install pillow requests pyperclip

Since tkinter is usually part of the Python standard library, it doesn't need to be installed separately in most cases. However, on some systems, additional system - level packages may be required to ensure its proper functionality. For example, on Ubuntu, you may need to install the python3 - tk package.

- 🐍 Python Version: Python 3.7+ is required. Python is a high-level, interpreted programming language known for its simplicity and readability, which forms the core runtime environment for WeixinMPTools.

▶️ Startup Methods

There are two ways to start the WeixinMPTools:

- 📚 Dependency Libraries:

python WeixinMPTools.py

2. Open your command-line interface (such as the Windows Command Prompt or the Terminal on Linux/macOS).

📝 Operation Guidelines

- 

  1. 🖼️ Image Selection: Click the "Select Upper Image" and "Select Lower Image" buttons to choose the two images you want to stitch.

  2. : Click the "Start Cropping" button. This will activate the interactive cropping mode on the preview canvas.

  3. Cropping Operation: Drag and draw a cropping frame on the preview canvas. The cropping frame is automatically locked to the preset ratios (2.35:1 for the upper image and 1:1 for the lower image). You can adjust the position and size of the cropping frame within the image area to get the desired cropping result.

  4. ✂️ Cropping Activation: Click the "Start Cropping" button to activate the cropping mode, which allows you to draw a cropping frame on the preview canvas.

  5. Cropping Confirmation: After you are satisfied with the cropping, click the "Apply Cropping" button to confirm the cropping.

  6. Background Setting: Select either a white or transparent background from the background - selection dropdown menu.

  7. Stitching Execution: Click the "Execute Stitching" button to perform the image - stitching operation.

  8. Saving the Result: Click the "Save Image" button. A file - saving dialog will appear, allowing you to choose the save location and name for the stitched image. The default file name format is combined_image_YYYYMMDD.jpg.

Output Examples

- Compressed Image: Compressed image files have a file name appended with _compressed_q{quality value}. For instance, if the original file is named banner.jpg and the compression quality is set to 75, the compressed file will be named banner_compressed_q75.jpg.

FAQs

- Q2: The cover image extraction fails. Why?

  - A: First, make sure the link is a WeChat official article page (starting with https://mp.weixin.qq.com/s?). Some articles with anti - hotlinking enabled may not be able to be extracted. Also, check if there are any network issues that could prevent the tool from accessing the article page.

Contact the Author

- bilibili: https://space.bilibili.com/366462635

- GitHub: https://github.com/SorakageMeiou

If you encounter any bugs during the use of WeixinMPTools or have suggestions for new features, please feel free to submit an Issue on GitHub. Your feedback is highly valued as it helps to improve the tool and make it more user - friendly and feature - rich for all WeChat Official Account operators.

- Q4: The transparent background of the PNG image is lost after compression. What can I do?

  - A: You need to select the "Maintain PNG Format" option during compression. If you choose "Automatic Conversion to JPEG", the transparent background will be converted to white because JPEG does not support transparency.

- Q3: The image size doesn't decrease after compression. Why?

  - A: By default, the tool will automatically skip images that are already smaller than 10MB. If you want to further compress these images, you can manually adjust the size threshold in the settings or reduce the compression quality value.

- Q1: I can't draw a rectangle during cropping. What should I do?

  - A: Please click the "Start Cropping" button first to activate the drawing mode. The cropping frame will be automatically locked to the preset ratio, and then you can start drawing the cropping area on the preview canvas.

- Stitched Image: The stitched image file follows the format combined_image_YYYYMMDD.jpg. For example, if the stitching operation is carried out on November 19, 2025, the output file will be named combined_image_20251119.jpg.

- Cover Image: The cover image file is named in the format cover_YYYYMMDD_HHMMSS.jpg. For example, if the extraction is done on November 19, 2025, at 12:30:45 PM, the file name would be cover_20251119_123045.jpg.

- 📝 Running from Source Code: If you have the source code of the tool, navigate to the directory where the WeixinMPTools.py file is located in the command-line interface. Then run the following command:

- Cover Image Extraction:

  1. Link Input: Paste the full URL of the WeChat Official Account article (in the format https://mp.weixin.qq.com/s?xxxx) into the designated input box.

  2. Extraction Initiation: Click the "Extract Cover Image" button. The tool will start parsing the article link and searching for the cover image.

  3. Result Feedback: Once the cover image is successfully extracted, the image link will be automatically copied to the clipboard. Meanwhile, the cover image will be downloaded to the directory where the program is located, with the file name following the format cover_YYYYMMDD_HHMMSS.jpg.
Note: Only standard WeChat Official Account article pages (not mini - program pages or third - party - redirected links) are supported.

- Image Compression:

  - Single - file Compression:

    1. Image Selection: Click the "Select Image" button to choose the single image you want to compress.

    2. Quality Adjustment: Drag the compression quality slider, which ranges from 10 to 100. A lower value means higher compression but potentially lower image quality, while a higher value preserves more image details but results in a larger file size.

    3. Compression Start: Click the "Start Compression" button to start the compression process. The compressed image will be saved in the same directory as the original image, with a file name appended with _compressed_q{quality value}. For example, if the original file is named example.jpg and the compression quality is set to 80, the compressed file will be named example_compressed_q80.jpg.

  - Batch Compression:

    1. Folder Selection: Click the "Select Folder" button to choose the folder that contains the images you want to compress.

    2. Sub - directory Option: If you want to include all the sub - directories within the selected folder, check the "Include Sub - directories" checkbox.

    3. Batch Compression Execution: Click the "Batch Compression" button. The tool will start compressing all the eligible images in the selected folder (and sub - directories if selected). Each compressed image will have a file name with the _compressed_q{quality value} suffix, and the original files will remain intact.

- 🖱️ Running the Packaged Program: If the tool has been packaged into an executable file (.exe for Windows, or a binary file for other operating systems), simply double-click the executable file. The graphical user interface of the tool will then be launched.
