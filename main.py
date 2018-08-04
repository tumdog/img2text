
import cv2
import numpy as np

def dist(s1,s2):
    s1 = s1.split(',')
    s2 = s2.split(',')
    return (int(s1[0])-int(s2[0]))**2+(int(s1[1])-int(s2[1]))**2+(int(s1[2])-int(s2[2]))**2

def extract_valid_colors(img):

    symbols = ['.','o','-','x']
    symbol_color_map = {}

    # convert image to linear array of color strings
    img = img.reshape(len(img)*len(img[0]), 3).tolist()
    img_string = np.array([','.join([str(x) for x in t]) for t in img])
    color_frequency = np.unique(img_string, return_counts = True)

    symbol_color_map[color_frequency[0][0]] = symbols[0]

    last_used_color = color_frequency[0][0]
    current_symbol = 1
    updated = True

    while(updated and current_symbol<4):
        marked = None
        updated = False
        for color in color_frequency[0]:
            if symbol_color_map.get(color,'') == '':
                if(dist(last_used_color,color)<1):
                    symbol_color_map[color] = symbol_color_map[last_used_color]
                elif not marked:
                    symbol_color_map[color] = symbols[current_symbol]
                    current_symbol = current_symbol+1
                    marked = color
                    updated = True
        last_used_color = marked

    return symbol_color_map

def get_transformation_steps(width_limit = None, height_limit = None):
    if width_limit:
        height_limit = int(width_limit * len(timg)/len(timg[0]))
    elif height_limit:
        width_limit = int(height_limit * len(timg[0])/len(timg))
    else:
        return [0,0]
    wstep = int(len(timg[0])/width_limit)
    hstep = int(len(timg)/height_limit)
    return [wstep,hstep]


def draw_image(img, symbol_color_map):
    result = ''
    for px_list in img:
        temp_result = ''
        for px in px_list:
            color = ','.join([str(t) for t in px])
            try:
                temp_result = temp_result+symbol_color_map[color]
            except:
                temp_result = temp_result+'e'
        result = result + '\n' + temp_result

    print(result)


def main():
    img = cv2.imread('batman.png')
    wstep, hstep = get_transformation_steps(40)

    # step over the entire image matrix wstep along the width and hstep along the
    # height. Transpose is used to easily convert rows to columns and remove the
    # rows and transform back, saves from writing a loop and stepping

    img = img[0::hstep+1].transpose(1,0,2)[0::wstep+1].transpose(1,0,2)

    symbol_color_map = extract_valid_colors(img)

    draw_image(img, symbol_color_map)

main()
