from PIL import Image, ImageFont, ImageDraw 
import os
from json import load
from pkg_resources import parse_version
import datetime

##########################################################################################
DEBUG = False
directory = os.path.dirname(os.path.dirname(__file__))  # For more info about parent directories, visit the link below. 
                                                        # https://stackoverflow.com/questions/58778625/how-to-get-the-path-of-the-parent-directory-in-python
dataFolder = "\\data"
validExtensions = [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
config = []
font = ""
waterFont = ""
##########################################################################################

def updateConfi():
    global config, font, waterFont
    with open(directory + dataFolder + "\\confi.json", "r", encoding="utf-8") as fil:
            config = load(fil)
    font = ImageFont.truetype(directory + dataFolder + config["fontPath"], config["fontSize"]) #path, font size
    waterFont = ImageFont.truetype(directory + dataFolder + config["fontPath"], config["fontSizeWatermark"]) #path, font size

def process(path, num):
    if DEBUG:
        print(f"{num}-".rjust(3) + f" Processing: {path}")

    im = Image.open(path)  # img is the path of the image 
    im = im.convert("RGB")
    if config["pagenumIsFilename"]:
        num = path.split("/")[-1]

    if config["noCrop"]:
        config["right"], config["down"] = im.size
        config["left"] = config["up"] = 0
        im1 = im
    else:    
        im1 = im.crop((config["left"], config["up"], config["right"], config["down"]))#im.crop((left, top, right, bottom))
    dim = ImageDraw.Draw(im1) #drawn image
    textWidth, textHeight = dim.textsize(str(num), font) #will be drawn string, font size
    
    if config["numPos"] == 1:
        x = config["right"] - config["left"] - textWidth - 10
        y = config["down"] - config["up"] - textHeight - 10
    elif config["numPos"] == 2:
        x = config["right"] - config["left"] - textWidth - 10
        y = config["up"] + 10
    elif config["numPos"] == 3:
        x = config["left"] + 10
        y = config["up"] + 10
    elif config["numPos"] == 4:
        x = config["left"] + 10
        y = config["down"] - config["up"] - textHeight - 10
    if config["isBgExists"]:
        dim.rectangle((x, y, x + textWidth, y + textHeight), fill=tuple(config["bgColor"]))
    
    dim.text( (x, y), str(num), fill=tuple(config["pgnumColor"]), font=font, align ="left") #add page number

    if config["watermarkEnabled"]:
        im1 = im1.convert("RGBA")
        watWidth, watHeight = dim.textsize(str(config["watermark"]), waterFont) #will be drawn watermark string, watermark font size
        wx = (config["right"] - config["left"] - watWidth)/2 
        wy = (config["down"] - config["up"] - watHeight)/2
        
        #add watermark
        watermark = Image.new('RGBA', im1.size, (255,255,255,0))
        watermarkD = ImageDraw.Draw(watermark)
        watermarkD.text( (wx, wy), str(config["watermark"]), fill=tuple(config["watermarkColor"]), font=waterFont, align ="center")
        watermark = watermark.rotate(config["watermarkAngle"], expand = False) #degree, counter clockwise
        im1 = Image.alpha_composite(im1, watermark)
        im1 = im1.convert("RGB")

    return im1

# Useful when the only filenames are known
def save(dirPath, files):        
    ims = [process(f"{dirPath}\\{file}", (i + 1)) for i, file in enumerate(files)]
    try:
        customDT = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        ims[0].save(f"{directory}\\output\\Pdfized__{customDT}.pdf",save_all=True, append_images=ims[1:], resolution=config["dpi"], subsampling=0, quality=config["fidelity"])
        if DEBUG:
            print("Pdf has been created successfully. Press any key to exit...")

    except OSError as exo:
        if DEBUG:
            print(exo)
            print("Please close the 'output.pdf' file and run the application again. Press any key to dismiss this message...")

# Useful when processed files are in array (i.e. list in python)
def save2(ims:list):
    try:
        customDT = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
        ims[0].save(f"{config['outputFolder']}\\Pdfized__{customDT}.pdf",save_all=True, append_images=ims[1:], resolution=config["dpi"], subsampling=0, quality=config["fidelity"])
        return "Success"
    except OSError as exo:
        return str(exo)

def getFiles(dir):
    files = []
    for item in os.listdir(dir):
        if any(item.endswith(extension) for extension in validExtensions):
            files.append(dir + "/" + item)
    if DEBUG:
        print(f"{len(files)} files found, they will be converted to pdf")
    files.sort(key=parse_version)
    return validateFiles(files) 

def validateFiles(files:list):
    return [file for file in files if any(file.endswith(extension) for extension in validExtensions)]


if __name__ == '__main__':
    from msvcrt import getch
    DEBUG = True
    updateConfi()
    save(dirPath=directory + "\\input", files=getFiles(directory + "\\input"))
    DEBUG = False
    garbage = getch()
          