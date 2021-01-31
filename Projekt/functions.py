import math
import numpy as np


def get_random_pattern(image, pattern_width, patterns_number):
    patterns = []
    patterns_indexes = []
    
    image_width = len(image[0])
    max_reduced_index = image_width / pattern_width
    if not max_reduced_index.is_integer():
        raise ValueError(f'Incorrect pattern width ({max_reduced_index}) - required image width divider.')
    
    while len(patterns) < patterns_number:
        row_index = np.random.randint(0, max_reduced_index) * pattern_width
        col_index = np.random.randint(0, max_reduced_index) * pattern_width
        if [row_index, col_index] not in patterns_indexes:
            patterns_indexes.append([row_index, col_index])
            pattern = image[row_index : row_index + pattern_width,
                            col_index : col_index + pattern_width]
            patterns.append(pattern.ravel())
    return patterns


def get_all_patterns(image, pattern_width):
    patterns = []
    image_width = len(image[0])
    max_reduced_index = image_width / pattern_width
    if not max_reduced_index.is_integer():
        raise ValueError(f'Incorrect pattern width ({max_reduced_index}) - required image width divider.')

    row = 0
    while row < image_width:
        col = 0
        while col < image_width:
            pattern = image[row : row + pattern_width,
                            col : col + pattern_width]
            patterns.append(pattern.ravel())
            col += pattern_width
        row += pattern_width
    return patterns


def normalize_from_pixels(arraylike):
    return arraylike / 255


def normalize_to_pixels(arraylike):
    return arraylike * 255


def get_psnr(orginal_image, reduced_image):
    orginal_image = np.array(orginal_image).ravel()
    reduced_image = np.array(reduced_image).ravel()

    if (len(orginal_image) != len(reduced_image)):
        raise ValueError(f'Orginal image ({len(orginal_image)}) \
            differs in size from reduced image ({len(reduced_image)})')

    img_sum = 0
    for i in range(len(orginal_image)):
        img_sum += math.pow((orginal_image[i] - reduced_image[i]) * 255, 2)

    return 10 * math.log10( (255 * 255) / (img_sum / (512 * 512)) )


def get_image(img, pattern_width, img_width):
    reshaped = []
    for pattern in img:
        reshaped.append(pattern.reshape(pattern_width, pattern_width))

    patterns_in_row = int(img_width / pattern_width)

    global_rows = []

    for i in range(patterns_in_row):
        rows = []
        for _ in range(pattern_width):
            rows.append([])

        for j in range(patterns_in_row):
            for k in range(pattern_width):
                rows[k] += reshaped[i * patterns_in_row + j][k].tolist()

        global_rows += rows

    return np.array(global_rows) 
