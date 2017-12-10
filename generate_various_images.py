'''
image processing
'''
import os
import sys
from logging import getLogger, basicConfig, root
from PIL import Image


# set logger
logger = getLogger(__name__)
root.setLevel(level='INFO')
basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')


def load_files(file_path):
    '''
    load files
    '''
    files = os.listdir(file_path)
    return files


def processing_image(img, mode='gray', rotate=0):
    '''
    image processing
    '''
    fix_img = img

    # gray-scale
    if mode == 'gray':
        fix_img = img.convert('L')
    elif mode == 'noize':
        pass
    elif mode == 'rotate':
        fix_img = img.rotate(rotate)
    elif mode == 'bright':
        fix_img = img.point(lambda x: x * 1.5)
    elif mode == 'dark':
        fix_img = img.point(lambda x: x * 0.5)

    logger.info("processing '%s'.", mode)

    return fix_img


def generate_image(img, output_path=None):
    '''
    generate fixed image
    '''
    if not output_path:
        logger.error('path is not defined.')
        return 1

    img.save(output_path, 'JPEG', quality=100, optimize=True)
    logger.info('output file image.')
    return 0


def create_image(img, path, mode='gray', rotate=0):
    '''
    create_image
    '''
    output_path = path + mode + '.jpg'
    fix_img = processing_image(img, mode=mode, rotate=rotate)
    generate_image(fix_img, output_path)

    return 0


def duplicate_files(path, files, output_dir="./output"):
    '''
    duplicatites files
    '''
    # check output directories
    if not os.path.exists(output_dir):
        # if target directory is not existed, making create directories
        os.makedirs(output_dir)
        logger.info('create output directory: "%s"', output_dir)
    
    for i, file in enumerate(files):
        # load image
        fullpath = path + "/" + file
        img = Image.open(fullpath)
        resize_img = img.resize((100, 100))

        # define output path
        output_path = output_dir + '/image_{0}_'.format(i)

        # create gray-scale image
        create_image(resize_img, output_path, mode='gray')

        # create add noize image
        create_image(resize_img, output_path, mode='noize')

        # create rotate x 4 image
        create_image(resize_img, output_path, mode='rotate', rotate=0)
        create_image(resize_img, output_path, mode='rotate', rotate=90)
        create_image(resize_img, output_path, mode='rotate', rotate=180)
        create_image(resize_img, output_path, mode='rotate', rotate=270)

        # create bright image
        create_image(resize_img, output_path, mode='bright')

        # create dark image
        create_image(resize_img, output_path, mode='dark')


    return 0

def main():
    '''
    main function
    '''
    home_path = '/Users/wararaki/dataset/yahoohack'
    positive_file_path = home_path+"/positive"
    negative_file_path = home_path+"/negative"

    # load files
    positive_files = load_files(positive_file_path)
    negative_files = load_files(negative_file_path)
    logger.info("got filepath")

    # duplicate_files
    duplicate_files(positive_file_path, positive_files, output_dir=home_path+"/train/positives")
    duplicate_files(negative_file_path, negative_files, output_dir=home_path+"/train/negatives")
    logger.info("Done")

    return 0

if __name__ == "__main__":
    sys.exit(main())
