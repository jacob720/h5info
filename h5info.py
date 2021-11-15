#!/scratch/miniconda3/bin/python

# This is a simple command line tool which displays the names of groups and datasets in a HDF file, and some basic information about the datasets.
# Author: Jacob Williamson

import h5py


def print_dataset(slice):
    if len(slice.shape) >= 3:
        print("\nVOLUME")
        for i in range(len(slice)):
            print(f'SLICE {i+1}')
            print_dataset(slice[i])
    elif len(slice.shape) == 2:
        print(slice)
    elif len(slice.shape) == 0:
        print(slice[()])
    else:
        print(slice[0:])

def print_metadata(h5_object):
    print('attributes: ', list(h5_object.attrs.items()), '\n')


def print_dataset_info(dataset):
    print(dataset.name, 'is a dataset!')
    shape = dataset.shape
    print('shape: ', shape)
    print('data type: ', dataset.dtype)
    print_metadata(dataset)
    u_input = input("Type 'v' to view the data, or enter to continue: ")
    if u_input == 'v':
        print_dataset(dataset)
        print()


def print_groups(group):
    if isinstance(group, h5py.Dataset):
        print_dataset_info(group)
        return 'dataset'
    else:
        print(f'In {group.name} :')
        print(f'{list(group.keys())}\n')
        return 'group'


def groups(group):
    while True:
        type = print_groups(group)
        if type == 'dataset':
            return 'b'
        u_input = input("Type name of next group/dataset, 'a' to view attributes (metadata) of current group, 'b' to go back 1 layer, or 'exit' to exit:\n")
        if u_input == 'b' or u_input == 'exit':
            return u_input
        elif u_input == 'a':
            print_metadata(group)
        elif u_input not in list(group.keys()):
            print('Not a correct group name')
        else:
            print(list(group.keys()))
            try:
                status = groups(group[u_input])
                if status == 'exit':
                    return status
            except KeyError as error:
                print(error)
                print('Bad link: component not found')


while True:
    file_name = input("Hi there! Enter a hdf5 file to get some info on it, or type 'quit' to quit the program:\n")
    if file_name == 'quit':
        break
    try:
        f = h5py.File(file_name, 'r')
        print(f"Looking inside {file_name} now, here's what I found:")
        groups(f)
    except (OSError, ValueError) as error:
        print(error)
        print("Oh dear! I can't find that file :( ")

