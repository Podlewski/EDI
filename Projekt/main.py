from argument_parser import ArgumentParser
from functions import *
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.neural_network import MLPRegressor


args = ArgumentParser().get_args()

training_data = []
test_images = []
img_width = 0
results = {}

for image_path in args.training_images:
    if img_width is 0:
        img_width = len(np.asarray(Image.open(image_path)))
    img = np.asarray(Image.open(image_path))
    img = rescale_from_pixels(img)
    training_data += get_random_patterns(img, args.pattern_width, args.patterns_number)

for image_path in args.test_images:
    img = np.asarray(Image.open(image_path))
    img = rescale_from_pixels(img)
    test_images.append(get_all_patterns(img, args.pattern_width))

for img_name in args.short_test_images:
    results[img_name] = {}

for neurones in args.neurones:
    mlp = MLPRegressor(hidden_layer_sizes=neurones, max_iter=args.iterations,
                       learning_rate_init=args.learning_rate,  solver='sgd',
                       activation='identity', alpha=0, momentum=0)
    mlp.fit(training_data, training_data)

    for i in range(len(test_images)):
        processed_data = mlp.predict(test_images[i])

        cr = get_cr(img_width, neurones, args.pattern_width)
        psnr = get_psnr(test_images[i], processed_data)
        img = get_image(processed_data, args.pattern_width, img_width)
        img = rescale_to_pixels(img)

        img = Image.fromarray(img)
        if img.mode != 'L':
            img = img.convert('L')
        img.save('res/' + args.chart_name + '/' + str(neurones) + '/out_' + args.short_test_images[i])

        results[args.short_test_images[i]][cr] = [psnr]

for name, dict in results.items():
    plt.plot(dict.keys(), dict.values(), label=name, marker='o', markersize=3)

plt.xlabel('Stopień kompresji')
plt.ylabel('PSNR')
plt.legend()
plt.savefig('res/chart_' + args.chart_name)
