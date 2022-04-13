class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""
        hist = [0] * 256
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                hist[image[i][j]] += 1
        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram it to find the otsu's threshold assuming that the input hstogram is bimodal histogram
        takes as input
        hist: a bimodal histogram
        returns: an optimal threshold value (otsu's threshold)"""
        prob = [0] * len(hist)
        histsum = 0
        zombie = dict()
        #m1 is the left side of the histogram(0 -> t), m2 is the right side of the hist (t->256)
        #calculating hist summation
        for i in range(len(hist)):
            histsum += hist[i]
        #calculate probability
        for i in range(len(hist)):
            prob[i] = (hist[i] / histsum)
        #cal weights
        for t in range(256):
            m1 = m2 = temp = s_l = s_r = v_l = v_r = 0
            minvar_l = minvar_r = intvar_l = intvar_r = kat = 0
            for i in range(256):
                if i <= t:
                    s_l += prob[i]
                if i > t:
                    s_r += prob[i]
            if s_l == 0 or s_r == 0:
                continue
            for i in range(256):
                if i <= t:
                    m1 += ((i * prob[i]) / s_l)
                if i > t:
                    m2 += ((i * prob[i]) / s_r)
            #cal variance
            for i in range(256):
                if i <= t:
                    intvar_l += ( ( ((i-m1)**2) * prob[i] ) / s_l)
                if i > t:
                    intvar_r += ( ( ((i-m2)**2) * prob[i] ) / s_r)
            #weighted class sum
            temp = (s_l * (intvar_l)) + (s_r * (intvar_r))
            zombie[t] = temp

        kat = min(zombie.values())
        for k in zombie:
            if zombie[k] == kat:
                threshold = k

        return threshold

    def binarize(self, image):
        """Comptues the binary image of the input image based on histogram analysis and thresholding
        take as input
        image: an grey scale image
        returns: a binary image"""
        kat = self.find_otsu_threshold(self.compute_histogram(image))
        bin_img = image.copy()
        for i in range(bin_img.shape[0]):
            for j in range(bin_img.shape[1]):
                if bin_img[i][j] < kat:
                    bin_img[i][j] = 255
                else:
                    bin_img[i][j] = 0
        return bin_img
