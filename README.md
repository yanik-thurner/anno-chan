# anno-chan

Python application to train neural networks iteratively. I developed it as part of my Bachelor thesis.

![image of the anno-chan interface](https://github.com/yanik-thurner/anno-chan/blob/main/images/anno-chan.png?raw=true)

The UI consists of the following elements:
- **Annotation Panels** Up to 3 panels are displayed: Old Annotations, Predicted Annota-
tions, and New Annotations. The Old Annotations panel shows existing annotations
and is hidden if there are none, i.e., when creating a new dataset. The Predicted
Annotations panel shows annotations predicted by a (partially) trained network. It
is only displayed when the AI Support checkbox is checked. On the lower half, the
panel displays the new annotations, which will get saved in the JSON file the next
time the dataset is saved. On each panel, the bounding boxes of the annotations
are drawn in the color of their category. Annotations generally have two states:
selected and unselected. Unselected annotations are drawn transparently, selected
annotations are opaque. When an unselected annotation in the Old or Predicted
panel is left-clicked inside, its state changes to selected and it is added to the New
panel. When a selected annotation in the Old or Predicted panel is left-clicked
inside, its state changes to unselected and it is removed from the New panel. Hence,
the New panel only contains selected annotations. It also allows the manual drawing
of annotations by pressing the left mouse button at one point, moving the mouse,
and releasing it at another point which creates a rectangular bounding box with
both points as diametrical corners. Left-clicking inside an annotation in the New
panel removes the bounding box, since this panel does not contain any unselected
annotations. If there are annotations inside other annotations, the oldest annotation
gets removed. To make annotating easier for images with small eyes, each image can
be point-zoomed by using the mouse wheel and translated by drag-and-dropping with the right mouse button.
- **Annotation List** The list left to the New Annotations panel contains the number of
annotations and for each annotation their category ID, position and confidence
level of the prediction. Manually drawn annotations get a score of 1. This list gives
an overview of the currently present annotation and helps to avoid invalid ones. If
the user checked the Select Predictions Checkbox, it could happen that the network
adds small invalid annotations that are hard to notice, especially on large images.
The user could compare the number of counted annotations in this panel with the
number of eyes in the picture to avoid such mistakes.
- **Navigation Buttons** The Next and the Previous buttons are used to navigate the
dataset. Pressing Next marks an image as reviewed before loading the next image.
- **Categories** The application allows the user to add and remove categories. Removing
a category does not remove all annotations with that ID in case one just wants
to rename it. The background category exists by default and cannot be removed.
It should be used when the image should not contain any images but the model
detects some anyway. This is because PyTorch does not allow images without
annotations. Which category a manually drawn annotation is depends on which
category button was clicked. The colors of the categories are chosen randomly and
can be reassigned whenever it is convenient by clicking on the Dataset menu and
then choosing Reroll Colors. For faster reviewing hotkeys with the corresponding category number are created automatically.
- **Skip Reviewed Checkbox** When this checkbox is checked, all already reviewed images
are skipped. This is especially useful when adding new images to an existing dataset.
With the checkbox checked, one could navigate to a newly added frame of a show
and uncheck it to see how the neighboring frames were annotated.
- **AI Support Checkbox** By unchecking this checkbox, the Predicted Annotations panel
is hidden and the image is not evaluated by the model. This can be useful when
one needs to quickly iterate through the dataset, e.g., when checking the dataset
for errors, since predicting increases the loading time of an image.
- **Score Threshold Slider** By using this slider, the user can change the score threshold
of the predictions that are shown in the Predicted Annotations panel and that get
selected when the Selected Predictions checkbox is checked. For example with a
threshold of 0.7, only predictions with a confidence level ≥ 0.7 are shown.
- **Select Predictions Checkbox** If the checkbox has been checked, the annotations that
are shown in the Predicted Annotations panel automatically get selected when
an image is loaded. Otherwise, the old annotations are marked as selected and
thus appear in the New Annotations panel. If at one point the performance of the
partially trained model is sufficient, checking this is advised, since it is faster to
remove wrong predictions than to manually select all the correct annotations from
the Prediction panel.
- **Prediction Model Drop-Down** The application supports switching between multiple
trained prediction models by selecting one in the drop-down in the lower-left corner.
This allows testing models to be trained with different hyper-parameters on specific
data to see where problems occur.
- **Progress Bar** This bar shows the percentage of reviewed images of all images of the
current dataset.
