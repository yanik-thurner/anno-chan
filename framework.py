import copy
import os
from typing import Optional

import torch
from PIL import Image
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.transforms import transforms

from dataset import CocoDataset


class AnnotationFramework:
    def __init__(self, root_path, annotation_file_path, save_rate, score_threshold):
        self.SKIP_REVIEWED = False
        self.AI_SUPPORT = True
        self.SELECT_PREDICTIONS = False
        self.SAVE_RATE = save_rate
        self.SCORE_THRESHOLD = score_threshold

        self.current_file: Optional[str] = None
        self.current_pred: dict = CocoDataset.empty_data()

        self._dataset_old: Optional[CocoDataset] = None
        self._dataset_new: Optional[CocoDataset] = None
        self._model: Optional[FastRCNNPredictor] = None
        self.categories: Optional[list] = None

        if root_path is not None and annotation_file_path is not None:
            self.init_datasets(root_path, annotation_file_path)
            self.categories = self._dataset_new.categories

        self._review_len_old = len(self._dataset_new.reviewed)

    def init_datasets(self, root_path, annotation_file_path):
        self._dataset_old = CocoDataset(root_path, annotation_file_path)
        self._dataset_new = copy.deepcopy(self._dataset_old)
        self._dataset_new.scan_for_new()

    def init_predictor(self, model_path):
        print(f'using model {model_path}')
        if torch.cuda.is_available():
            print('using cuda...')
            self._model = torch.load(model_path)
            self._model.to('cuda')
        else:
            print('using cpu...')
            self._model = torch.load(model_path, map_location=torch.device('cpu'))
        self._model.eval()

    def annotations_changed(self, load=False):
        """
        :param load: if the annotations changed form a load event (not a click on a widget)
        """
        data_dict = self.get_current_dataset()
        if data_dict is None:
            return

        # go through data new, unselect all annotations also not selected in the other datasets, then remove them (if not a load event)
        for i, annotation in enumerate(data_dict['new']['annotations']):
            index_old = CocoDataset.index_of_bbox(data_dict['old'], annotation) if data_dict['old'] is not None else None
            index_pred = CocoDataset.index_of_bbox(data_dict['pred'], annotation) if data_dict['pred'] is not None else None

            if not data_dict['new']['selected'][i]:
                CocoDataset.delete_annotation(data_dict['new'], i)
                if index_old is not None:
                    data_dict['old']['selected'][index_old] = False
                if index_pred is not None:
                    data_dict['pred']['selected'][index_pred] = False
            elif load:
                if index_old is not None:
                    data_dict['old']['selected'][index_old] = True
                if index_pred is not None:
                    data_dict['pred']['selected'][index_pred] = True

        # go through old and predicted data, remove all not selected and existing annotations in new and add all
        # selected and not existing
        for data in (data_dict['old'], data_dict['pred']):
            if data is None:
                continue
            for i, annotation in enumerate(data['annotations']):
                bbox_index = CocoDataset.index_of_bbox(data_dict['new'], annotation)
                if data['selected'][i] and bbox_index is None:
                    added = CocoDataset.add_annotation(data_dict['new'], annotation, data['scores'][i])
                    data['selected'][i] = added
                elif not data['selected'][i] and bbox_index is not None:
                    CocoDataset.delete_annotation(data_dict['new'], bbox_index)

    def _load_image_pil(self, data):
        image = Image.open(os.path.join(self._dataset_new.root, data['image']['file_name'])).convert('RGB')
        data['image_pil'].value = image
        data['image']['width'] = image.width
        data['image']['height'] = image.height

    def predict_current(self) -> dict:
        if self.current_pred is not None:
            return self.current_pred

        trans = transforms.Compose([
            transforms.ToTensor(),
        ])
        image = trans(self._dataset_new[self.current_file]['image_pil'].value)
        w = self._dataset_new[self.current_file]['image']['width']
        h = self._dataset_new[self.current_file]['image']['height']
        if torch.cuda.is_available():
            image = image.to(torch.device('cuda'))

        prediction = self._model([image])[0]
        annotations = []
        scores = []
        for i in range(len(prediction['labels'])):
            scores.append(prediction['scores'][i].item())
            bbox = [prediction['boxes'][i][0].item(),
                    prediction['boxes'][i][1].item(),
                    prediction['boxes'][i][2].item() - prediction['boxes'][i][0].item(),
                    prediction['boxes'][i][3].item() - prediction['boxes'][i][1].item()]
            bbox = [bbox[0]/w, bbox[1]/h, bbox[2]/w, bbox[3]/h]
            annotation = CocoDataset.empty_annotation()
            annotation['bbox'] = bbox
            annotation['category_id'] = prediction['labels'][i].item()
            annotations.append(annotation)

        self.current_pred = CocoDataset.empty_data()
        self.current_pred['image'] = copy.deepcopy(self._dataset_new[self.current_file]['image'])
        self.current_pred['image']['id'] = None

        for i, annotation in enumerate(annotations):
            CocoDataset.add_annotation(self.current_pred, annotation, selected=False, score=scores[i])

        return self.current_pred

    def _select_predictions(self, data):
        if data['old'] is not None:
            data['old']['selected'].clear()
            data['old']['selected'].extend([False] * len(data['old']['annotations']))
        data['new']['annotations'].clear()
        data['new']['selected'].clear()
        data['new']['scores'].clear()

        for i, annotation in enumerate(data['pred']['annotations']):
            if data['pred']['scores'][i] >= self.SCORE_THRESHOLD:
                data['new']['annotations'].append(annotation)
                data['new']['selected'].append(True)
                data['pred']['selected'][i] = True
                data['new']['scores'].append(data['pred']['scores'][i])

    def get_next_dataset(self) -> Optional[dict]:
        if self.current_file is not None:
            if len(self._dataset_new.reviewed) % self.SAVE_RATE == 0 and len(self._dataset_new.reviewed) != self._review_len_old:
                self._dataset_new.save()
                self._review_len_old = len(self._dataset_new.reviewed)

            if self.current_file not in self._dataset_new.reviewed:
                self._dataset_new.reviewed.append(self.current_file)

        self.current_file = self._dataset_new.get_next(self.current_file, self.SKIP_REVIEWED)
        self.current_pred = None

        data = self.get_current_dataset()
        if self.AI_SUPPORT and self.SELECT_PREDICTIONS:
            self._select_predictions(data)
        return data

    def get_current_dataset(self):
        if self._dataset_new[self.current_file] is None:
            return None

        if self._dataset_new[self.current_file]['image_pil'].value is None:
            self._load_image_pil(self._dataset_new[self.current_file])

        data = {'old': self._dataset_old[self.current_file],
                'new': self._dataset_new[self.current_file],
                'pred': self.predict_current() if self.AI_SUPPORT else None}
        return data

    def get_previous_dataset(self):
        self.current_file = self._dataset_new.get_previous(self.current_file)
        self.current_pred = None

        return self.get_current_dataset()

    def save(self):
        self._dataset_new.save()

    def reset_reviewed(self):
        self._dataset_new.reviewed = []

    def len_reviewed(self):
        return len(self._dataset_new.reviewed)

    def len_new_files(self):
        return len(self._dataset_new.files)
