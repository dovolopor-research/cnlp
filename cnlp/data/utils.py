import random
from typing import Union
from collections import defaultdict

import numpy as np


def split(dataset: list, split_size: Union[int, list, None] = None, shuffle: bool = False) -> tuple:
    """Split the dataset.

    Attributes:
        dataset: origin dataset.
        split_size: fixed number, train and test split size or train validate and test split size.
        shuffle:  Whether to shuffle dataset.
    """
    if split_size is None:
        split_size = [0.7, 0.3]

    if shuffle:
        np.random.shuffle(dataset)

    __all_data_num = len(dataset)
    # 切分出固定个数的 test
    if type(split_size) is int and split_size < __all_data_num:
        # train test
        return dataset[:__all_data_num-split_size], dataset[__all_data_num-split_size:]
    else:
        if len(split_size) in [2, 3]:
            if np.sum(split_size) == 1:
                # train test
                if len(split_size) == 2:
                    train_num = int(__all_data_num * split_size[0])
                    test_num = __all_data_num - train_num
                    print(f"all data num: {__all_data_num}, train num: {train_num}, test num: {test_num}")
                    return dataset[:train_num], dataset[train_num:]
                # train val test
                else:
                    train_num = int(__all_data_num * split_size[0])
                    val_num = int(__all_data_num * split_size[1])
                    test_num = __all_data_num - train_num - val_num
                    print(f"all data num: {__all_data_num}, train num: {train_num}, val num: {val_num} test num: {test_num}")
                    return dataset[:train_num], dataset[train_num: train_num + val_num], dataset[val_num:]
            else:
                raise ValueError(f"the sum of split_size must equal 1: {split_size}")
        else:
            raise ValueError(f"split_size length must be one of 1 (split number), 2 [train, test] \
            or 3 [train, val, test]: {len(split_size)}")


def sampling(dataset: list, mode: str = "over", seed: int = 0):
    """使用上采样或下采样处理类别不平衡问题

    Attributes:
        dataset: origin dataset.
        mode: over 过采样 under 欠采样
        seed: random seed.
    """
    random.seed(seed)

    dataset_dict = defaultdict(list)
    for data_item, data_class in dataset:
        dataset_dict[data_class].append(data_item)

    dataset_number_dict = defaultdict(int)
    for key, value in dataset_dict.items():
        dataset_number_dict[key] = len(value)

    max_class = max(dataset_number_dict.values())
    min_class = min(dataset_number_dict.values())

    sampled_dataset = []
    if mode == "over":
        for key, value in dataset_dict.items():
            repeat_multiple = max_class // dataset_number_dict[key]
            sample_number = max_class % dataset_number_dict[key]
            sample_data = random.sample(value, sample_number)
            for class_data in value * repeat_multiple + sample_data:
                sampled_dataset.append([class_data, key])
    elif mode == "under":
        for key, value in dataset_dict.items():
            for class_data in random.sample(value, min_class):
                sampled_dataset.append([class_data, key])
    else:
        raise ValueError("the mode must in [over, under]")

    return sampled_dataset
