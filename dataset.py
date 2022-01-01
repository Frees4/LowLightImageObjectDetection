import splitfolders
import os


def train_val_test_split_folders(input_folder, output_folder, ratio):
    # ratio of split are in order of train/val/test.
    # You can change to whatever you want. For train/val sets only, you could do .75, .25 for example.
    splitfolders.ratio(input_folder, output_folder, seed=42, ratio=ratio)


def annotations_name_ending_removing(path_to_labels_folder, folder):
    list_of_files = os.listdir(path_to_labels_folder + folder)
    path = path_to_labels_folder + folder
    for file in list_of_files:
        os.rename(path + file,
                  path + file.replace('.jpg', '').replace('.JPEG', '').replace('.png', '').replace('.JPG', '').replace(
                      '.jpeg', ''))


def box_center_to_corner(box):
    """Convert from (center, width, height) to (upper-left, lower-right)."""
    cx, cy, w, h = box[0], box[1], box[2], box[3]
    x1 = cx - 0.5 * w
    y1 = cy - 0.5 * h
    x2 = cx + 0.5 * w
    y2 = cy + 0.5 * h
    return [(x1, y1), (x2, y2)]


def convert_exDark_annotation2yolo(class_name, l, t, w, h, image_w, image_h):
    dct = dict({'Bicycle': 0, 'Boat': 1, 'Bottle': 2, 'Bus': 3, 'Car': 4, 'Cat': 5, 'Chair': 6, 'Cup': 7, 'Dog': 8,
                'Motorbike': 9, 'People': 10, 'Table': 11})
    class_id = dct[class_name]
    bw = w / image_w
    bh = h / image_h
    x_center = (2 * l + w) / 2 / image_w
    y_center = (2 * t + h) / 2 / image_h
    return f"{class_id} {x_center} {y_center} {bw} {bh}"


def exDark2yolo(data):
    list_of_files = os.listdir("annotations/" + data)
    for file in list_of_files:
        annotation = "annotations/" + data + file
        lines = []
        with open(annotation, 'r') as f:
            lines = f.readlines()
        im = Image.open('images/' + data + file[:-4])
        (width, height) = im.size
        with open(annotation, 'w') as f:
            for i in range(1, len(lines)):
                str_params = lines[i].split()
                f.write(convert_exDark2yolo(str_params[0], float(str_params[1]),
                                            float(str_params[2]), float(str_params[3]), float(str_params[4]), width,
                                            height) + '\n')
