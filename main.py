import numpy as np
import pandas as pd

from utils.consts import FRAMES_USED, MAX_HEIGHT, MAX_WIDTH, FRAMES_PER_SECOND


def calculate_object_width_and_height(row_in_dataset):
    return np.abs(row_in_dataset[0] - row_in_dataset[2]), np.abs(row_in_dataset[1] - row_in_dataset[3])


# 1. Посчитать все объекты с размерами больше определенных
def calculate_number_objects_bigger_size(data_as_rows, height, width):
    counter = 0
    for row in data_as_rows:
        obj_width, obj_height = calculate_object_width_and_height(row)
        if obj_height > height and obj_width > width:
            counter += 1
    return counter


# 5-6. Определить кадры, когда в кадре было более N объектов одновременно
def get_frames_with_objects(data_as_rows, N):
    objects_count = np.zeros(FRAMES_USED)
    for row in data_as_rows:
        objects_count[row[5]] += 1

    return np.argwhere(objects_count >= N)


# 7. Рассчитать для всех объектов среднее время нахождения в кадре (время жизни объекта)
def calculate_middle_object_lifetime(data_as_rows):
    dictionary_obj_idx_to_frames_appeared = {}

    for row in data_as_rows:
        tmp_obj_id = row[4]

        if tmp_obj_id not in dictionary_obj_idx_to_frames_appeared.keys():
            dictionary_obj_idx_to_frames_appeared[tmp_obj_id] = 1
        else:
            dictionary_obj_idx_to_frames_appeared[tmp_obj_id] += 1

    avg_lifetime_value = np.mean(np.array(list(dictionary_obj_idx_to_frames_appeared.values())))

    return avg_lifetime_value


def main():
    dataframe    = pd.read_csv("resources/trajectories.csv", sep=';')
    dataframe    = dataframe.drop(columns=['Unnamed: 0'])
    dataframe    = dataframe[dataframe['frame'] < FRAMES_USED]
    obj_quantity = calculate_number_objects_bigger_size(dataframe.values, MAX_HEIGHT, MAX_WIDTH)
    empty_frames = get_frames_with_objects(dataframe.values, 5)
    avg_lifetime = calculate_middle_object_lifetime(dataframe.values)

    print(f"Objects quantity with size more then {MAX_HEIGHT}x{MAX_WIDTH} (HEIGHT x WIDTH): {obj_quantity}")
    print("Frame indicies with zero objects :", empty_frames.flatten())
    print("Average lifetime in seconds for frame is: ", avg_lifetime/FRAMES_PER_SECOND)
