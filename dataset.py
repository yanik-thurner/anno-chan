import copy
import glob
import json
import os
from datetime import datetime
from typing import Optional

from helper import Reference


class ImageIdExistsException(Exception):
    def __init__(self, index):
        self.message = f'Image ID {index}, already exists'

    def __str__(self):
        print(self.message)


class CocoDataset:

    @staticmethod
    def empty_data() -> dict:
        return {'image': CocoDataset.empty_image(), 'image_pil': None, 'annotations': [], 'scores': [], 'selected': []}

    @staticmethod
    def empty_image() -> dict:
        return {'id': None, 'width': None, 'height': None, 'file_name': None}

    @staticmethod
    def empty_annotation() -> dict:
        return {'id': None, 'image_id': None, 'category_id': None, 'area': None, 'bbox': None, 'iscrowd': None}

    @staticmethod
    def _map_data(annotations_unmapped: list, images) -> (dict, dict, dict):
        annotations = {}
        selected = {}
        scores = {}
        for annotation in annotations_unmapped:
            id = annotation['image_id']
            if id not in annotations.keys():
                annotations[id] = [annotation]
                selected[id] = [True]
                scores[id] = [1]
            else:
                annotations[id].append(annotation)
                selected[id].append(True)
                scores[id].append(1)

        for image in images:
            if image['id'] not in annotations.keys():
                annotations[image['id']] = []
                selected[image['id']] = []
                scores[image['id']] = []

        return annotations, selected, scores

    @staticmethod
    def add_annotation(data: dict, annotation: dict, score: float = 1, selected: bool = True) -> bool:
        if annotation['bbox'] in [x['bbox'] for x in data['annotations']]:
            return False
        data['annotations'].append(annotation)
        data['scores'].append(score)
        data['selected'].append(selected)
        return True

    @staticmethod
    def delete_annotation(data: dict, index: int):
        del data['annotations'][index]
        del data['scores'][index]
        del data['selected'][index]

    @staticmethod
    def index_of_bbox(data: dict, annotation: dict) -> Optional[int]:
        for i, a in enumerate(data['annotations']):
            if annotation['bbox'] == a['bbox'] and annotation['id'] == a['id']:
                return i
        return None

    def __init__(self, root_path: str, annotation_file_path: str,  skip_load=False):
        """
        loads all the images and data in the json file, creates data structures and resets indexes of images and annotations

        :param root_path: path to the folder containing the images
        :param annotation_file_path: path to the annotation file
        """
        self.root = root_path
        self.annotation_file = annotation_file_path

        if not skip_load:
            print(f'loading images in annotation file')

            if not os.path.isfile(self.annotation_file ):
                self._create_annotation_file()

            dataset = json.load(open(annotation_file_path, 'r'))

            self._images = sorted(dataset['images'], key=lambda x: x['file_name'])
            self.files = [x['file_name'] for x in self._images]
            self._images_pil = [Reference(None) for i in range(len(self._images))]
            self._annotations, self._selected, self._scores = CocoDataset._map_data(dataset['annotations'], self._images)

            self.reviewed = dataset['reviewed']
            self.categories = dataset['categories']
            if 0 not in [category['id'] for category in self.categories]:
                self.categories.insert(0, {'id':0, 'name': 'background'})

            self._reset_indexes()
            print(
                f'the dataset in {root_path} has {len(self._images)} files and {len(dataset["annotations"])} annotations')

    def _create_annotation_file(self):
        data = {'images': [], 'annotations': [], 'categories': [{'id':0, 'name': 'background'}], 'reviewed': []}
        json.dump(data, open(self.annotation_file, 'w'))

    def _reset_indexes(self):
        """
        goes through all the image data and corresponding annotations and starts reassigning the indexes starting at 0.
        returns without changes if the id of the last item is what it should be (len - 1)
        """
        if len(self) == 0:
            return

        image_id = 0
        annotation_id = 0
        files_new = []
        annotations_new = {}
        selected_new = {}
        scores_new = {}

        for image in self._images:
            image_id_old = image['id']
            image['id'] = image_id

            for annotation in self._annotations[image_id_old]:
                annotation['id'] = annotation_id
                annotation['image_id'] = image_id
                annotation_id = annotation_id + 1

            files_new.append(image['file_name'])
            annotations_new[image['id']] = self._annotations[image_id_old]
            selected_new[image['id']] = self._selected[image_id_old]
            scores_new[image['id']] = self._scores[image_id_old]
            image_id = image_id + 1

        self.files = files_new
        self._annotations = annotations_new
        self._selected = selected_new
        self._scores = scores_new

    def _add_new(self, image: dict):
        """
        adds image data to the dataset and creates all other corresponding entries
        :param image:
        :return:
        """
        image_id = image['id']
        if image_id < len(self):
            raise ImageIdExistsException

        self._images.append(image)
        self._images_pil.append(Reference(None))
        self._annotations[image_id] = []
        self._selected[image_id] = []
        self._scores[image_id] = []

    def scan_for_new(self):
        """
        scans the root folder for images that are not in the data json and adds them to the dataset.
        :return:
        """
        print(f'loading new images in {self.root}')
        new_paths = glob.glob(os.path.join(self.root, '*'))
        files = [os.path.basename(x['file_name']) for x in self._images]

        for file_path in new_paths:
            file_name = os.path.basename(file_path)
            if file_name not in files:
                image = CocoDataset.empty_image()
                image['id'] = self._images[-1]['id'] + 1 if len(self) > 0 else 0
                image['file_name'] = file_name
                self._add_new(image)

        self._images = sorted(self._images, key=lambda x: x['file_name'])
        self._reset_indexes()
        print('finished loading images')

    def get_next(self, current_file: str, skip_reviewed: bool = False) -> Optional[str]:
        start_index = 0 if current_file is None else self.files.index(current_file) + 1
        for i in range(start_index, len(self.files)):
            if skip_reviewed and self._images[i]['file_name'] in self.reviewed:
                continue
            else:
                return self._images[i]['file_name']
        return None

    def get_previous(self, current_file: str) -> Optional[str]:
        if self.files[0] == current_file:
            return None
        if current_file is None:
            return self.files[-1]
        return self.files[self.files.index(current_file) - 1]

    def __getitem__(self, file_name: str) -> Optional[dict]:
        if file_name not in self.files:
            return None

        image_id = self.files.index(file_name)
        return {'image': self._images[image_id],
                'image_pil': self._images_pil[image_id],
                'annotations': self._annotations[image_id],
                'scores': self._scores[image_id],
                'selected': self._selected[image_id]}

    def __len__(self):
        return len(self._images)

    def save(self, secure: bool = True):
        """
        saves the data to the original json file
        :param secure: additionally creates a .json_backup
        """
        print('saving data...')
        _images = copy.deepcopy(self._images)
        _annotations = copy.deepcopy(self._annotations)
        images = []
        annotations = []

        image_id = 0
        annotation_id = 0
        category_distribution = {}
        for category in self.categories:
            category_distribution[category['id']] = 0

        for image in _images:
            if len(_annotations[image['id']]) == 0:
                continue

            for annotation in _annotations[image['id']]:
                annotation['id'] = annotation_id
                annotation['image_id'] = image_id
                annotation['area'] = annotation['bbox'][2] * annotation['bbox'][3]
                annotation['iscrowd'] = False
                annotations.append(annotation)
                category_distribution[annotation['category_id']] = category_distribution[annotation['category_id']] + 1
                annotation_id = annotation_id + 1

            image['id'] = image_id
            images.append(image)
            image_id = image_id + 1

        data = {'images': images, 'annotations': annotations, 'categories': self.categories, 'reviewed': self.reviewed}
        json.dump(data, open(self.annotation_file, 'w'), indent=2)
        if secure:
            timestamp = datetime.now()
            timestampstr = str(timestamp).replace(' ', '-').replace(':', '-').replace('.', '-')
            json.dump(data, open(self.annotation_file + '_' + timestampstr, 'w'), indent=2)

        print(f'saved {len(images)} images and {len(annotations)} annotations: {category_distribution}')
