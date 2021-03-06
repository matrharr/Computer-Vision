"""Problem Set 4: Motion Detection"""

import cv2
import os
import numpy as np

import ps4

# I/O directories
input_dir = "input_images"
output_dir = "output"
VID_DIR = "input_videos"

# Utility code
def quiver(u, v, scale, stride, color=(0, 255, 0)):

    img_out = np.zeros((v.shape[0], u.shape[1], 3), dtype=np.uint8)

    for y in range(0, v.shape[0], stride):

        for x in range(0, u.shape[1], stride):

            cv2.line(img_out, (x, y), (x + int(u[y, x] * scale),
                                       y + int(v[y, x] * scale)), color, 1)
            cv2.circle(img_out, (x + int(u[y, x] * scale),
                                 y + int(v[y, x] * scale)), 1, color, 1)
    return img_out


# Functions you need to complete:

def scale_u_and_v(u, v, level, pyr):
    """Scales up U and V arrays to match the image dimensions assigned 
    to the first pyramid level: pyr[0].

    You will use this method in part 3. In this section you are asked 
    to select a level in the gaussian pyramid which contains images 
    that are smaller than the one located in pyr[0]. This function 
    should take the U and V arrays computed from this lower level and 
    expand them to match a the size of pyr[0].

    This function consists of a sequence of ps4.expand_image operations 
    based on the pyramid level used to obtain both U and V. Multiply 
    the result of expand_image by 2 to scale the vector values. After 
    each expand_image operation you should adjust the resulting arrays 
    to match the current level shape 
    i.e. U.shape == pyr[current_level].shape and 
    V.shape == pyr[current_level].shape. In case they don't, adjust
    the U and V arrays by removing the extra rows and columns.

    Hint: create a for loop from level-1 to 0 inclusive.

    Both resulting arrays' shapes should match pyr[0].shape.

    Args:
        u: U array obtained from ps4.optic_flow_lk
        v: V array obtained from ps4.optic_flow_lk
        level: level value used in the gaussian pyramid to obtain U 
               and V (see part_3)
        pyr: gaussian pyramid used to verify the shapes of U and V at 
             each iteration until the level 0 has been met.

    Returns:
        tuple: two-element tuple containing:
            u (numpy.array): scaled U array of shape equal to 
                             pyr[0].shape
            v (numpy.array): scaled V array of shape equal to 
                             pyr[0].shape
    """

    # TODO: Your code here

    for i in range(level-1, -1, -1):
        u = ps4.expand_image(u)
        v = ps4.expand_image(v)
    return (u,v)

    raise NotImplementedError

def helper_for_part_6(video_name_base, fps, frame_ids, output_prefix, counter_init):

    video_base = os.path.join(VID_DIR, video_name_base)
    image_gen_base = ps4.video_frame_generator(video_base)

    image_base = image_gen_base.__next__()
    image_a = image_base
    h, w, d = image_base.shape

    out_path = "output/ar_{}-{}".format(output_prefix[4:], video_name_base)
    video_out = mp4_video_writer(out_path, (w, h), fps)

    output_counter = counter_init

    frame_num = 1

    # while image_base is not None:
    for i in range(150):

        print("Processing fame {}".format(frame_num))

        image_a_grey = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        image_grey = cv2.cvtColor(image_base, cv2.COLOR_BGR2GRAY)

        levels = 2
        k_size = 25
        k_type = "gaussian" 
        sigma = 0.001
        interpolation = cv2.INTER_CUBIC 
        border_mode = cv2.BORDER_REFLECT101
        u, v = ps4.hierarchical_lk(image_a_grey, image_grey, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)
        arr = quiver(u, v, scale=0.1, stride=14, color=(0, 255, 255))

        res = np.copy(image_base)

        res = cv2.addWeighted(res,0.7, arr, 1, -0.7)

        frame_id = frame_ids[(output_counter - 1) % 2]

        if frame_num == frame_id:
            out_str = output_prefix + "-{}.png".format(output_counter)
            save_image(out_str, res)
            output_counter += 1

        video_out.write(res)

        image_pre = image_base
        image_base = image_gen_base.__next__()
        # image_base = image_gen_base.__next__()

        frame_num += 1

    video_out.release()

def mp4_video_writer(filename, frame_size, fps=20):
    """Opens and returns a video for writing.

    Use the VideoWriter's `write` method to save images.
    Remember to 'release' when finished.

    Args:
        filename (string): Filename for saved video
        frame_size (tuple): Width, height tuple of output video
        fps (int): Frames per second
    Returns:
        VideoWriter: Instance of VideoWriter ready for writing
    """
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    return cv2.VideoWriter(filename, fourcc, fps, frame_size)

def save_image(filename, image):
    """Convenient wrapper for writing images to the output directory."""
    cv2.imwrite(os.path.join(output_dir, filename), image)

def part_1a():

    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                      'Shift0.png'), 0) / 255.
    shift_r2 = cv2.imread(os.path.join(input_dir, 'TestSeq', 
                                       'ShiftR2.png'), 0) / 255.
    shift_r5_u5 = cv2.imread(os.path.join(input_dir, 'TestSeq', 
                                          'ShiftR5U5.png'), 0) / 255.
   
    # Optional: smooth the images if LK doesn't work well on raw images
    k_size = 35  # TODO: Select a kernel size
    k_type = "uniform"  # TODO: Select a kernel type
    sigma = 1  # TODO: Select a sigma value if you are using a gaussian kernel
    u, v = ps4.optic_flow_lk(shift_0, shift_r2, k_size, k_type, sigma)

    # Flow image
    u_v = quiver(u, v, scale=3, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-a-1.png"), u_v)

    # Now let's try with ShiftR5U5. You may want to try smoothing the
    # input images first.

    k_size = 61 # TODO: Select a kernel size
    k_type = "uniform"  # TODO: Select a kernel type
    sigma = 1 # TODO: Select a sigma value if you are using a gaussian kernel
    u, v = ps4.optic_flow_lk(shift_0, shift_r5_u5, k_size, k_type, sigma)

    # Flow image
    u_v = quiver(u, v, scale=4, stride=10)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-a-2.png"), u_v)


def part_1b():
    """Performs the same operations applied in part_1a using the images
    ShiftR10, ShiftR20 and ShiftR40.

    You will compare the base image Shift0.png with the remaining
    images located in the directory TestSeq:
    - ShiftR10.png
    - ShiftR20.png
    - ShiftR40.png

    Make sure you explore different parameters and/or pre-process the
    input images to improve your results.

    In this part you should save the following images:
    - ps4-1-b-1.png
    - ps4-1-b-2.png
    - ps4-1-b-3.png

    Returns:
        None
    """
    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                      'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR10.png'), 0) / 255.
    shift_r20 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR20.png'), 0) / 255.
    shift_r40 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR40.png'), 0) / 255.

    k_size = 99  # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 5  # TODO: Select a sigma value if you are using a gaussian kernel
    u, v = ps4.optic_flow_lk(shift_0, shift_r10, k_size, k_type, sigma)

    # Flow image
    u_v = quiver(u, v, scale=1, stride=12)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-b-1.png"), u_v)

    k_size = 99 # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 16 # TODO: Select a sigma value if you are using a gaussian kernel
    u, v = ps4.optic_flow_lk(shift_0, shift_r20, k_size, k_type, sigma)

    # Flow image
    u_v = quiver(u, v, scale=0.5, stride=12)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-b-2.png"), u_v)

    k_size = 99  # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 21  # TODO: Select a sigma value if you are using a gaussian kernel
    u, v = ps4.optic_flow_lk(shift_0, shift_r40, k_size, k_type, sigma)

    # Flow image
    u_v = quiver(u, v, scale=0.25, stride=12)
    cv2.imwrite(os.path.join(output_dir, "ps4-1-b-3.png"), u_v)



def part_2():

    yos_img_01 = cv2.imread(os.path.join(input_dir, 'DataSeq1',
                                         'yos_img_01.jpg'), 0) / 255.
    
    # 2a
    levels = 4
    yos_img_01_g_pyr = ps4.gaussian_pyramid(yos_img_01, levels)
    yos_img_01_g_pyr_img = ps4.create_combined_img(yos_img_01_g_pyr)
    # cv2.imshow('test',yos_img_01_g_pyr_img)
    # cv2.waitKey(0)
    # cv2.imwrite(os.path.join(output_dir, "ps4-2-a-1.png"), yos_img_01_g_pyr_img)
    cv2.imwrite(os.path.join(output_dir, "ps4-2-a-1.png"),
                yos_img_01_g_pyr_img)

    # 2b
    yos_img_01_l_pyr = ps4.laplacian_pyramid(yos_img_01_g_pyr)

    yos_img_01_l_pyr_img = ps4.create_combined_img(yos_img_01_l_pyr)
    # cv2.imshow('test',yos_img_01_l_pyr_img)
    # cv2.waitKey(0)
    cv2.imwrite(os.path.join(output_dir, "ps4-2-b-1.png"),
                yos_img_01_l_pyr_img)


def part_3a_1():
    yos_img_01 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_01.jpg'), 0) / 255.
    yos_img_02 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_02.jpg'), 0) / 255.

    levels = 4  # Define the number of pyramid levels
    yos_img_01_g_pyr = ps4.gaussian_pyramid(yos_img_01, levels)
    yos_img_02_g_pyr = ps4.gaussian_pyramid(yos_img_02, levels)

    level_id = 0  # TODO: Select the level number (or id) you wish to use
    k_size = 99 # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 10  # TODO: Select a sigma value if you are using a gaussian kernel
    u, v = ps4.optic_flow_lk(yos_img_01_g_pyr[level_id],
                             yos_img_02_g_pyr[level_id],
                             k_size, k_type, sigma)

    u, v = scale_u_and_v(u, v, level_id, yos_img_02_g_pyr)

    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values
    yos_img_02_warped = ps4.warp(yos_img_02, u, v, interpolation, border_mode)

    diff_yos_img_01_02 = yos_img_01 - yos_img_02_warped
    cv2.imwrite(os.path.join(output_dir, "ps4-3-a-1.png"),
                ps4.normalize_and_scale(diff_yos_img_01_02))


def part_3a_2():
    yos_img_02 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_02.jpg'), 0) / 255.
    yos_img_03 = cv2.imread(
        os.path.join(input_dir, 'DataSeq1', 'yos_img_03.jpg'), 0) / 255.

    levels = 4  # Define the number of pyramid levels
    yos_img_02_g_pyr = ps4.gaussian_pyramid(yos_img_02, levels)
    yos_img_03_g_pyr = ps4.gaussian_pyramid(yos_img_03, levels)

    level_id = 0 # TODO: Select the level number (or id) you wish to use
    k_size = 111 # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 10 # TODO: Select a sigma value if you are using a gaussian kernel
    u, v = ps4.optic_flow_lk(yos_img_02_g_pyr[level_id],
                             yos_img_03_g_pyr[level_id],
                             k_size, k_type, sigma)

    u, v = scale_u_and_v(u, v, level_id, yos_img_03_g_pyr)

    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values
    yos_img_03_warped = ps4.warp(yos_img_03, u, v, interpolation, border_mode)

    diff_yos_img = yos_img_02 - yos_img_03_warped
    cv2.imwrite(os.path.join(output_dir, "ps4-3-a-2.png"),
                ps4.normalize_and_scale(diff_yos_img))


def part_4a():
    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                      'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR10.png'), 0) / 255.
    shift_r20 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR20.png'), 0) / 255.
    shift_r40 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR40.png'), 0) / 255.

    levels = 5  # TODO: Define the number of levels
    k_size = 31  # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 2  # TODO: Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_LANCZOS4 #cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values

    u10, v10 = ps4.hierarchical_lk(shift_0, shift_r10, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    u_v = quiver(u10, v10, scale=0.6, stride=12)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-a-1.png"), u_v)

    # You may want to try different parameters for the remaining function
    # calls.
    u20, v20 = ps4.hierarchical_lk(shift_0, shift_r20, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    u_v = quiver(u20, v20, scale=0.3, stride=12)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-a-2.png"), u_v)

    k_size = 11  # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 1  # TODO: Select a sigma value if you are using a gaussian kernel

    u40, v40 = ps4.hierarchical_lk(shift_0, shift_r40, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)
    u_v = quiver(u40, v40, scale=0.1, stride=12)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-a-3.png"), u_v)


def part_4b():
    urban_img_01 = cv2.imread(
        os.path.join(input_dir, 'Urban2', 'urban01.png'), 0) / 255.
    urban_img_02 = cv2.imread(
        os.path.join(input_dir, 'Urban2', 'urban02.png'), 0) / 255.

    levels = 5  # TODO: Define the number of levels
    k_size = 23  # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 2  # TODO: Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values

    u, v = ps4.hierarchical_lk(urban_img_01, urban_img_02, levels, k_size,
                               k_type, sigma, interpolation, border_mode)

    u_v = quiver(u, v, scale=0.1, stride=12)
    cv2.imwrite(os.path.join(output_dir, "ps4-4-b-1.png"), u_v)

    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values
    urban_img_02_warped = ps4.warp(urban_img_02, u, v, interpolation,
                                   border_mode)

    diff_img = urban_img_01 - urban_img_02_warped
    cv2.imwrite(os.path.join(output_dir, "ps4-4-b-2.png"),
                ps4.normalize_and_scale(diff_img))


def part_5a():
    """Frame interpolation

    Follow the instructions in the problem set instructions.

    Place all your work in this file and this section.
    """
    shift_0 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                      'Shift0.png'), 0) / 255.
    shift_r10 = cv2.imread(os.path.join(input_dir, 'TestSeq',
                                        'ShiftR10.png'), 0) / 255.
    levels = 5  # TODO: Define the number of levels
    k_size = 35  # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 1  # TODO: Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values

    u, v = ps4.hierarchical_lk(shift_0, shift_r10, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    t = 0.2
    shift_r10_wraped_1 = ps4.warp(shift_0, -t*u, -t*v, interpolation, border_mode)

    t = 0.4
    shift_r10_wraped_2 = ps4.warp(shift_0, -t*u, -t*v, interpolation, border_mode)

    t = 0.6
    shift_r10_wraped_3 = ps4.warp(shift_0, -t*u, -t*v, interpolation, border_mode)

    t = 0.8
    shift_r10_wraped_4 = ps4.warp(shift_0, -t*u, -t*v, interpolation, border_mode)

    H, W = shift_0.shape
    target = np.ones((2*H, 3*W), dtype = np.float64)

    target[0 : H, 0 : W] = ps4.normalize_and_scale(shift_0)
    target[0 : H, W : 2*W] = ps4.normalize_and_scale(shift_r10_wraped_1)
    target[0 : H, 2*W : 3*W] = ps4.normalize_and_scale(shift_r10_wraped_2)
    target[H : 2*H, 0 : W] = ps4.normalize_and_scale(shift_r10_wraped_3)
    target[H : 2*H, W : 2*W] = ps4.normalize_and_scale(shift_r10_wraped_4)
    target[H : 2*H, 2*W : 3*W] = ps4.normalize_and_scale(shift_r10)
    cv2.imwrite(os.path.join(output_dir, "ps4-5-a-1.png"),
                ps4.normalize_and_scale(target))


def part_5b():
    """Frame interpolation

    Follow the instructions in the problem set instructions.

    Place all your work in this file and this section.
    """

    mc01 = cv2.imread(os.path.join(input_dir, 'MiniCooper',
                                      'mc01.png'), 0) / 255.
    mc02 = cv2.imread(os.path.join(input_dir, 'MiniCooper',
                                        'mc02.png'), 0) / 255.
    levels = 5  # TODO: Define the number of levels
    k_size = 99  # TODO: Select a kernel size
    k_type = "gaussian"  # TODO: Select a kernel type
    sigma = 4  # TODO: Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values

    u, v = ps4.hierarchical_lk(mc01, mc02, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    t = 0.1
    n = 2*t
    shift_r10_wraped_1 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    n = 5*t
    shift_r10_wraped_2 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    n = 8*t
    shift_r10_wraped_3 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    n = 10*t
    shift_r10_wraped_4 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    H, W = mc01.shape
    target = np.zeros((2*H, 3*W), dtype = np.float64)

    target[0 : H, 0 : W] = ps4.normalize_and_scale(mc01)
    target[0 : H, W : 2*W] = ps4.normalize_and_scale(shift_r10_wraped_1)
    target[0 : H, 2*W : 3*W] = ps4.normalize_and_scale(shift_r10_wraped_2)
    target[H : 2*H, 0 : W] = ps4.normalize_and_scale(shift_r10_wraped_3)
    target[H : 2*H, W : 2*W] = ps4.normalize_and_scale(shift_r10_wraped_4)
    target[H : 2*H, 2*W : 3*W] = ps4.normalize_and_scale(mc02)
    cv2.imwrite(os.path.join(output_dir, "ps4-5-b-1.png"),
                ps4.normalize_and_scale(target))


    mc01 = cv2.imread(os.path.join(input_dir, 'MiniCooper',
                                      'mc02.png'), 0) / 255.
    mc02 = cv2.imread(os.path.join(input_dir, 'MiniCooper',
                                        'mc03.png'), 0) / 255.
    levels = 5  # TODO: Define the number of levels
    k_size = 111  # TODO: Select a kernel size
    k_type = "uniform"  # TODO: Select a kernel type
    sigma = 1  # TODO: Select a sigma value if you are using a gaussian kernel
    interpolation = cv2.INTER_CUBIC  # You may try different values
    border_mode = cv2.BORDER_REFLECT101  # You may try different values

    u, v = ps4.hierarchical_lk(mc01, mc02, levels, k_size, k_type,
                                   sigma, interpolation, border_mode)

    t = 0.1
    n = 2*t
    shift_r10_wraped_1 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    n = 5*t
    shift_r10_wraped_2 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    n = 30*t
    shift_r10_wraped_3 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    n = 70*t
    shift_r10_wraped_4 = ps4.warp(mc01, -n*u, -n*v, interpolation, border_mode)

    H, W = mc01.shape
    target = np.ones((2*H, 3*W), dtype = np.float64)

    target[0 : H, 0 : W] = ps4.normalize_and_scale(mc01)
    target[0 : H, W : 2*W] = ps4.normalize_and_scale(shift_r10_wraped_1)
    target[0 : H, 2*W : 3*W] = ps4.normalize_and_scale(shift_r10_wraped_2)
    target[H : 2*H, 0 : W] = ps4.normalize_and_scale(shift_r10_wraped_3)
    target[H : 2*H, W : 2*W] = ps4.normalize_and_scale(shift_r10_wraped_4)
    target[H : 2*H, 2*W : 3*W] = ps4.normalize_and_scale(mc02)
    cv2.imwrite(os.path.join(output_dir, "ps4-5-b-2.png"),
                ps4.normalize_and_scale(target))


def part_6():
    """Challenge Problem

    Follow the instructions in the problem set instructions.

    Place all your work in this file and this section.
    """

    video_file = "ps4-my-video.mp4"
    frame_ids = [40, 60]
    # frame_ids = [1,3,5]
    fps = 20

    helper_for_part_6(video_file, fps, frame_ids, "ps4-6-a",1)


if __name__ == '__main__':
    part_1a()
    part_1b()
    part_2()
    part_3a_1()
    part_3a_2()
    part_4a()
    part_4b()
    part_5a()
    part_5b()
    part_6()
