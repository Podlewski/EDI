import math
import numpy as np


def get_random_patterns(image, pattern_width, patterns_number):
    patterns = []
    patterns_indexes = []  
    image_width = len(image[0])

    img_pattern_ratio = image_width / pattern_width
    if not img_pattern_ratio.is_integer():
        raise ValueError(f'Incorrect pattern width ({img_pattern_ratio}) - required image width divider.')
    
    while len(patterns) < patterns_number:
        row_index = np.random.randint(0, image_width - pattern_width + 1)
        col_index = np.random.randint(0, image_width - pattern_width + 1)
        if [row_index, col_index] not in patterns_indexes:
            patterns_indexes.append([row_index, col_index])
            pattern = image[row_index : row_index + pattern_width,
                            col_index : col_index + pattern_width]
            patterns.append(pattern.ravel())
    return patterns


def get_all_patterns(image, pattern_width):
    patterns = []
    image_width = len(image[0])

    img_pattern_ratio = image_width / pattern_width
    if not img_pattern_ratio.is_integer():
        raise ValueError(f'Incorrect pattern width ({img_pattern_ratio}) - required image width divider.')

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


def get_pixels_mean_std(arraylike):
    array = arraylike.ravel()
    print(array(len))


def rescale_from_pixels(arraylike):
    return arraylike / 255 * 2 - 1


def rescale_to_pixels(arraylike):
    arraylike = np.clip(arraylike, -1, 1)
    return (arraylike + 1) * 255 / 2


def get_cr(image_width, hidden_neurones, pattern_width):
    BITS_IN_BYTE = 8
    BITS_TO_REMEMBER_HIDDEN_FACTOR = 12
    BITS_TO_REMEMBER_WEIGHT = 8
    pattern_pixels = pattern_width * pattern_width
    return (BITS_IN_BYTE * image_width * image_width) / \
        (pattern_pixels * hidden_neurones * BITS_TO_REMEMBER_WEIGHT +
         hidden_neurones * BITS_TO_REMEMBER_HIDDEN_FACTOR)


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
