import cv2
from PIL import Image
import os



def save_image(file_path, im):
    im.save(file_path)
    print "Image ",file_path, " saved"

def change_position_bit(number, index, zero_one):
    # positon to be changed set one
    position_made_one = 1 << index

    #negation -> that position value is zero and all the others one
    #and with negation -> only that position is turned to 0

    number &= ~position_made_one

    #if what we want to set is 1
    if zero_one:
        # Do or with original,so that that position would be converted to 1
        number |= position_made_one
    return number
cover_image_name = ""
steg_image_name = ""


def hide_image(two = 'no', encrypt = 'no'):
    global cover_image_name
    global steg_image_name

    cover_image_path = raw_input('Enter cover image: ')
    steg_image_path = raw_input('Enter stegno image: ')

    two = raw_input("Do you want to change to two least significant bit (yes): ")
    encrypt = raw_input("Do you want to change noise encrypted mode (yes): ")


    # cover_image_path = "coverimage1.jpg"
    # steg_image_path = "image1.jpg"

    cover_image_name = os.path.splitext(cover_image_path)[0]
    steg_image_name = os.path.splitext(steg_image_path)[0]



    cover_image_name = "images/"+cover_image_name


    # print cover_image_name


    steg_image_name = "images/" + steg_image_name

    img = cv2.imread("images/"+cover_image_path)
    # img = cv2.imread("images/coverimage3.jpg")

    two = 'no'

    #
    #
    # im = Image.open("b.jpg", 'r')
    # im_arr = im.load()
    #
    #
    # x_size, y_size = im.size
    #
    # key1 =123
    # key2 =45745742
    #




    # basic_encrypt_scramble(im_arr, x_size, y_size)
    # save_image("encrypt11.png", im)

    # steg_image = cv2.imread("images/image8.jpg")
    steg_image = cv2.imread("images/"+steg_image_path)


    # print img



    height, width, n = img.shape
    size = height * width

    # print height
    # print size
    # red = img[:, :, 2]
    # green = img[:, :, 1]
    # blue = img[:, :, 0]

    resized_image = cv2.resize(steg_image, (width, height))



    image_copy = img


    print "hiding the image in the least significant bits..."
    for i in range(size):

        coords = (i / width, i % width)

        original_px = img[coords[0]][coords[1]]

        steg_px = resized_image[coords[0]][coords[1]]

        original_red = original_px[2]
        original_green = original_px[1]
        original_blue = original_px[0]



        red = steg_px[2]
        green = steg_px[1]
        blue = steg_px[0]


        to_be_replaced_r_1 = '{0:08b}'.format(red)[:1]
        to_be_replaced_g_1 = '{0:08b}'.format(green)[:1]
        to_be_replaced_b_1 = '{0:08b}'.format(blue)[:1]



        to_be_replaced_r_2 = '{0:08b}'.format(red)[1:2]
        to_be_replaced_g_2 = '{0:08b}'.format(green)[1:2]
        to_be_replaced_b_2 = '{0:08b}'.format(blue)[1:2]

        to_be_replaced_r_3 = '{0:08b}'.format(red)[2:3]
        to_be_replaced_g_3 = '{0:08b}'.format(green)[2:3]
        to_be_replaced_b_3 = '{0:08b}'.format(blue)[2:3]
        # print to_be_replaced_r_1


        adjusted_byte_r = change_position_bit(original_red, 0, int(to_be_replaced_r_3))
        adjusted_byte_g = change_position_bit(original_green, 0, int(to_be_replaced_g_3))
        adjusted_byte_b = change_position_bit(original_blue, 0, int(to_be_replaced_b_3))

        adjusted_byte_r_2 = change_position_bit(adjusted_byte_r , 1, int(to_be_replaced_r_2))
        adjusted_byte_g_2 = change_position_bit(adjusted_byte_g , 1, int(to_be_replaced_g_2))
        adjusted_byte_b_2 = change_position_bit(adjusted_byte_b, 1, int(to_be_replaced_b_2))


        adjusted_byte_r_1 = change_position_bit(adjusted_byte_r_2, 2, int(to_be_replaced_r_1))
        adjusted_byte_g_1 = change_position_bit(adjusted_byte_g_2, 2, int(to_be_replaced_g_1))
        adjusted_byte_b_1 = change_position_bit(adjusted_byte_b_2, 2, int(to_be_replaced_b_1))

        # print adjusted_byte_r, 'adjusted_byte_r'




        if(two =='yes'):
            image_copy[coords[0]][coords[1]] = [adjusted_byte_b_2, adjusted_byte_g_2, adjusted_byte_r_2]
        else:
            image_copy[coords[0]][coords[1]] = [adjusted_byte_b_1, adjusted_byte_g_1, adjusted_byte_r_1]


    print "Saving the cover image with stegno image inside..."
    cv2.imwrite(cover_image_name+"_shifted.png", image_copy)

    if(encrypt=='yes'):
        im = Image.open(cover_image_name+"_shifted.png", 'r')
        im_arr = im.load()


        x_size, y_size = im.size


        for x in range(x_size):
            if x % 100 == 0:
                print "adding noise to image: ", x, "/", x_size
            for y in range(y_size - 1):
                # print y
                pixel = im_arr[x, y]
                noised_pixel = ((c + 1 if c % 2 == 0 else c) for c in pixel)
                im_arr[x, y] = tuple(int(c ** 43 % 256) for c in noised_pixel)


        save_image(cover_image_name + "_noise_encrypted.png", im)


        print 'image hiding finished'




def unhide_image(two = 'no', encrypt = 'no'):
    global cover_image_name

    unhide_img = raw_input("Enter the image to get unhide: ")
    unhide_img = "images/" + unhide_img
    two = raw_input("Is this image two bits changed? (yes): ")
    encrypt = raw_input("Is this image in noise encrypted mode (yes): ")


    # unhide_img = 'images/coverimage1_shifted.png'

    if(encrypt=='yes'):



        im = Image.open(unhide_img, 'r')
        im_arr = im.load()


        x_size, y_size = im.size



        for x in range(x_size):
            if x % 100 == 0:
                print "removing noise from image: ", x, "/", x_size
            for y in range(y_size):
                pixel = im_arr[x, y]
                im_arr[x, y] = tuple(int(c ** 3 % 256) for c in pixel)

        # two_key_decryption(im_arr, x_size, y_size, key1, key2)
        # basic_decrypt_unscramble(im_arr, x_size, y_size)
        save_image(unhide_img, im)




    image_copy = cv2.imread(unhide_img)
    height, width, n = image_copy.shape
    size = height * width
    # print height
    # print size
    image_copy_2 = image_copy

    print "Revealing the image..."
    for i in range(size):
        coords = (i / width, i % width)



        original_px_2 = image_copy[coords[0]][coords[1]]

        if (two == 'yes'):
            red = original_px_2[2] & 3
            green = original_px_2[1] & 3
            blue = original_px_2[0] & 3


        else:
            # print 'else'
            red = original_px_2[2] & 7
            green = original_px_2[1] & 7
            blue = original_px_2[0] & 7




        red = int(bin(red) + '00000', 2)
        green = int(bin(green) + '00000', 2)
        blue = int(bin(blue) + '00000', 2)



        image_copy_2[coords[0]][coords[1]] = [blue, green, red]


    if (two == 'yes'):
        if(encrypt == 'yes'):
            cv2.imwrite(unhide_img+'_recovered_two_bits_encrypted.png', image_copy_2)
            cv2.imshow('recovered_two_bits_encrypted image',image_copy_2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            cv2.imwrite(unhide_img + '_recovered_two_bits.png', image_copy_2)
            cv2.imshow('recovered_two_bits image',image_copy_2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        if (encrypt == 'yes'):
            cv2.imwrite(unhide_img + '_recovered_three_bits_encrypted.png', image_copy_2)

            cv2.imshow('recovered image_three_bits_encrypted',image_copy_2)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        else:
            cv2.imwrite(unhide_img+'_recovered_three_bits.png', image_copy_2)
        cv2.imshow('recovered image_three_bits', image_copy_2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()










hide_image(two='no',encrypt='no')
unhide_image(two='no',encrypt='no')





