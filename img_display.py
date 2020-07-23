import tensorflow as tf
import tensorflow_hub as hub 
import matplotlib.pyplot as plt 
import tempfile
from six.moves.urllib.request import urlopen 
from six import BytesIO
import numpy as np 
from PIL import Image 
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
import time 

## based on https://www.tensorflow.org/hub/tutorials/object_detection

# visualization code adapted from tf object detection api
def display_img(img):
    plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(img)
    plt.show()

def download_and_resize_img(url, new_width=256, new_height=256,
                            display=False):
    """
    TODO: description
    """                            
    _, filename = tempfile.mkstemp(suffix=".jpg")

    # make a request to the url
    response = urlopen(url)

    # read the response as an image
    image_data = response.read()
    image_data = BytesIO(image_data)
    pil_image = Image.open(image_data)

    # fit the image to new_width x new_height
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)

    # convert to rgb
    pil_image_rgb = pil_image.convert("RGB")

    # save the image
    pil_image_rgb.save(filename, format="JPEG", quality=90)
    print(f"Image downloaded to {filename}")

    if display:
        display_img(pil_image_rgb)

    return filename


def draw_bounding_box_on_img(image,
                             ymin,
                             xmin,
                             ymax,
                             xmax,
                             color,
                             font,
                             thickness=4,
                             display_str_list=()):
    """
    Adds a bounding box to an image.
    """

    # initiate the drawing object
    draw = ImageDraw.Draw(image)

    # define boundaries
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin*im_width, xmax*im_width, ymin*im_height, ymax*im_height)

    # draw the line 
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=thickness, fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]

    # each display_str has a top and bottom margin of 0.05px
    total_display_str_height = (1 + 2*0.5)*sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top 
    else:
        text_bottom = top + total_display_str_height
    
    # reverse list and print from bottom to top
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05*text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin), (left + text_width, text_bottom)], fill=color)
        draw.text((left + margin, text_bottom - text_height - margin), display_str, fill="black", font=font)
        text_bottom -= text_height - 2 * margin

def draw_boxes(image, boxes, class_names, scores, max_boxes = 10, min_score = 0.1):
    ""
    "Overlay labeled boxes on an image with formatted scores and label names."
    ""
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf", 25)
    except IOError:
        print("Font not found, using default font.")
    font = ImageFont.load_default()

    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(class_names[i].decode("ascii"), int(100 * scores[i]))
            color = colors[hash(class_names[i]) % len(colors)]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_img(image_pil,
                                       ymin,
                                       xmin,
                                       ymax,
                                       xmax,
                                       color,
                                       font,
                                       display_str_list = [display_str])
            np.copyto(image, np.array(image_pil))
    
    return image

def load_img(path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3) # 3 channels for color images
    return img

#### pick a sample image and display
image_url = "https://upload.wikimedia.org/wikipedia/commons/6/60/Naxos_Taverna.jpg" 
downloaded_image_path = download_and_resize_img(image_url, 1280, 856, True)

#### pick a module and you can re-train the classifier using this guide:
#### https://www.tensorflow.org/hub/tutorials/tf2_image_retraining
module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1" 
detector = hub.load(module_handle).signatures['default']

def run_detector(detector, path):
    img = load_img(path)

    converted_img = tf.image.convert_image_dtype(img, tf.float32)
