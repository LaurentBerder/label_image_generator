import sys
import os
import numpy as np
from random import shuffle
from src.download_files import download_image_files, extract_texts, check_img_folders

def main():
    # Run on the first time, so you can download all the images from the data
    # and extract the captions into separate txt files
    download_image_files()
    check_img_folders()
    extract_texts()

    seed = 42
    np.random.seed(seed)

    current_dir = os.path.dirname(__file__)
    sys.path.append(os.path.join(current_dir, '..'))
    current_dir = current_dir if current_dir is not '' else '.'

    img_dir_path = current_dir + '/data/validation/img/'
    txt_dir_path = current_dir + '/data/validation/text/'
    model_dir_path = current_dir + '/models'

    img_width = 32
    img_height = 32
    img_channels = 3

    from src.gan import DCGan
    from src.img_cap_loader import load_normalized_img_and_its_text

    image_label_pairs = load_normalized_img_and_its_text(img_dir_path, txt_dir_path, img_width=img_width, img_height=img_height)

    shuffle(image_label_pairs)

    gan = DCGan()
    gan.img_width = img_width
    gan.img_height = img_height
    gan.img_channels = img_channels
    gan.random_input_dim = 200
    gan.glove_source_dir_path = './very_large_data'

    batch_size = 16
    epochs = 1000
    gan.fit(model_dir_path=model_dir_path, image_label_pairs=image_label_pairs,
            snapshot_dir_path=current_dir + '/data/snapshots',
            snapshot_interval=100,
            batch_size=batch_size,
            epochs=epochs)


if __name__ == '__main__':
    main()