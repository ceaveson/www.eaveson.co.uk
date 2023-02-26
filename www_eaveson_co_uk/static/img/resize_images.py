from PIL import Image
from os import listdir

def batch_resize(dir='.'):
    images = [i for i in listdir(dir) if i[-4:] == '.jpg' or i[-4:] == '.png']
    for image in images:
        resize_img(image)

def resize_img(image_file):
    '''
    If image is more than 500px wide. The width is reduced to 500px
    and height scaled to match.
    '''
    im = Image.open(image_file)
    if im.size[0] > 500:
        height_diff = im.size[0]-500
        percent_smaller = height_diff/(im.size[0]/100)
        new_width = int((im.size[1]/100) * (100-percent_smaller))
        size = (500, new_width)
        im.thumbnail(size)
        im.save(image_file)

if __name__=='__main__':
    batch_resize('.')