import argparse
from os import listdir, makedirs, path


class ArgumentParser:
    args = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='EDI - e-learning', formatter_class=argparse.RawTextHelpFormatter,
            description='Politechnika Łódzka\
                         \nEksploracja Danych Internetowych - e-learning\
                         \n\nAutorzy:\
                         \n  Paweł Jeziorski\t234066\
                         \n  Karol Podlewski\t234106')

        self.parser.add_argument('-n', metavar='N', dest='neurones', type=int,
                                 nargs='+', default=[2, 4, 6, 8, 10, 12, 20, 30],
                                 help='Neurons in hidden layer quantity')

        self.parser.add_argument('-i', metavar='I', dest='iterations',
                                 type=int, default=10000,
                                 help='MLP iterations')

        self.parser.add_argument('-l', metavar='RATE', dest='learning_rate',
                                 type=float, default=0.01,
                                 help='Learning rate')                               

        self.parser.add_argument('-k', metavar='K', dest='patterns_number',
                                 type=int, default=512,
                                 help='Number of patterns')     

        self.parser.add_argument('-w', metavar='W', dest='pattern_width',
                                 type=int, default=8,
                                 help='Pattern width') 

        self.parser.add_argument('--training-img', metavar='PATH',
                                 dest='training_images', type=str, nargs='+',
                                 default=['./img/01.bmp', './img/03.bmp'],
                                 help='Training images')

        self.parser.add_argument('--test-img-folder', metavar='PATH',
                                 dest='test_images_folder', type=str,
                                 default='./img/', help='Test images folder')

        self.args = self.parser.parse_args()

    def get_args(self):
        self.args.short_test_images = [f for f in listdir(self.args.test_images_folder) \
            if path.isfile(path.join(self.args.test_images_folder, f))]
        self.args.test_images = [self.args.test_images_folder + f \
            for f in listdir(self.args.test_images_folder) \
            if path.isfile(path.join(self.args.test_images_folder, f))]

        for i in self.args.neurones:
            if not path.exists('res/' + str(i)):
                makedirs('res/' + str(i))

        return self.args
