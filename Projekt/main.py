from argument_parser import ArgumentParser
from functions import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import seaborn as sns
from sklearn.neural_network import MLPRegressor


sns.set_theme(style='darkgrid')

args = ArgumentParser().get_args()

training_data = []
test_images = []

img_width = 0

for image_path in args.training_images:
    if img_width is 0:
        img_width = len(np.asarray(Image.open(image_path)))
    img = np.asarray(Image.open(image_path))
    img = normalize_from_pixels(img)
    training_data = training_data + get_random_pattern(img, args.pattern_width, args.patterns_number)

for image_path in args.test_images:
    img = np.asarray(Image.open(image_path))
    img = normalize_from_pixels(img)
    test_images.append(get_all_patterns(img, args.pattern_width))

for neurones in args.neurones:
    mlp = MLPRegressor(hidden_layer_sizes=neurones, max_iter=args.iterations,
                       learning_rate_init=args.learning_rate,
                       activation='identity', solver='sgd', random_state=100,
                       alpha=0., momentum=0) # random_state, shuffle
    mlp.fit(training_data, training_data)

    for i in range(len(test_images)):
        processed_data = mlp.predict(test_images[i])


        psnr = get_psnr(test_images[i], processed_data)
        img = get_image(processed_data, args.pattern_width, img_width)
        img = normalize_to_pixels(img)

        img = Image.fromarray(img)
        if img.mode != 'L':
            img = img.convert('L')
        img.save('res/' + str(neurones) + '/out_' + args.short_test_images[i])

