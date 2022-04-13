import numpy as np

class Rle:
    def __init__(self):
        pass

    def encode_image(self,binary_image):
        """
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        rle_code = []
        kat = 0
        cur = binary_image[0][0]
        rle_code.append(cur)
        for i in range(binary_image.shape[0]):
            for j in range(binary_image.shape[1]):
                if binary_image[i][j] != cur:
                    cur = binary_image[i][j]
                    rle_code.append(kat)
                    kat = 1
                else:
                    kat += 1

        return rle_code  # replace zeros with rle_code

    def decode_image(self, rle_code, height, width):
        """
        Get original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        box = np.zeros((height, width), np.uint8)
        hue = rle_code[0]
        index = 1
        l = rle_code[index]

        for i in range(box.shape[0]):
            for j in range(box.shape[1]):
                if l == 0:
                    if (index+1) == len(rle_code):
                        break
                    index += 1
                    l = rle_code[index]
                    if hue == 0:
                        hue = 255
                    else:
                        hue = 0
                box[i][j] = hue
                l -= 1


        return  box  # replace zeros with image reconstructed from rle_Code





        




