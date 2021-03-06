import numpy as np
import tensorflow as tf
import cv2
import sys

# Import utilities
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# Define import paths
PATH_TO_CKPT = 'output_inference_graph.pb/frozen_inference_graph.pb'  # Import frozen model
PATH_TO_LABELS = 'frc_label_map.pbtxt'  # Import map of labels
NUM_CLASSES = 1  # Only one class (power cube)

# Load frozen model into memory
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# Load Label Map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes = NUM_CLASSES, use_display_name = True)
category_index = label_map_util.create_category_index(categories)


# Helper function for data format
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


# Define function for detecting objects within an image
def detect_objects(image_np, sess, detection_graph):
    # Define input
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Define outputs
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()

    # Predict
    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
                                             feed_dict={image_tensor: image_np_expanded})

    # Visualize
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np, np.squeeze(boxes), np.squeeze(classes).astype(np.int32),
        np.squeeze(scores), category_index, use_normalized_coordinates=True,
        min_score_thresh=.9,
        line_thickness=4
    )

    return image_np


# Define function for handling images
def detect_image(image_path, sess, detection_graph):
    # Import image
    image = cv2.imread(image_path.read())
    image = cv2.resize(image, (1080, 1920))
    image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect objects
    image_np = detect_objects(image_np, sess, detection_graph)

    # cv2.imwrite(output, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    cv2.imshow('img', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)


def detect_image_webcam(image, sess, detection_graph):
    # Format data
    image = cv2.resize(image, (480, 640))
    image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect objects
    image_np = detect_objects(image_np, sess, detection_graph)

    # cv2.imwrite(output, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    cv2.imshow('img', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    cv2.waitKey(1)
    return image_np


def detect_objects_coords(image_np, sess, detection_graph):
    # Define input
    image_np_expanded = np.expand_dims(image_np, axis=0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Define outputs
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()

    # Predict
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    # Find box vertices
    box_coords = []
    print(scores[0][:4])
    for i in range(0, len(scores[0])):
        if scores[0][i] > .4:
            box = boxes[0][i]
            rows = image_np.shape[0]
            cols = image_np.shape[1]
            # box[0] = box[0]
            # box[1] = box[1]
            # box[2] = box[2]
            # box[3] = box[3]
            box[0] = box[0] * rows
            box[1] = box[1] * cols
            box[2] = box[2] * rows
            box[3] = box[3] * cols
            box_coords.append(box)
            cv2.rectangle(image_np, (box[1], box[0]), (box[3], box[2]), (0, 255, 0), 3)
    # cv2.line(img, (0, 242), (height, 242), (255,0,0), thickness=3)
    # cv2.line(img, (0, 300), (height, 300), (255,0,0), thickness=3)
    # cv2.line(image_np, (242, 0), (242, height), (255,0,0), thickness=3)
    # cv2.line(image_np, (300, 0), (300, height), (255,0,0), thickness=3)

    cv2.imshow('img', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)

    # Returns coords of box in [y1, x1, y2, x2] format
    return box_coords


def detect_image_coords(image_path, sess, detection_graph):
    # Import image
    image = cv2.imread(image_path.read())
    image = cv2.resize(image, (640, 480))
    image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Detect objects
    coords = detect_objects_coords(image_np, sess, detection_graph)
    return coords


# Detect images
if __name__ == '__main__':
    # Start Session
    with detection_graph.as_default():
        sess = tf.Session(graph=detection_graph)

camInput = sys.argv[1]  # must be a number or it will chuch a tantrum
ret, cap = cv2.VideoCapture(camInput)
# Test Coord output
# print(detect_image_coords(image_paths[5], sess, detection_graph))
coords = detect_image_coords(inp, sess,
                             detection_graph)  # these coords need to be sent through to network tables or custom code
print(
"x coordinate : " + coords[0] + "y coordinate : " + coords[1] + "x2 coordinate : " + coords[2] + "y2 coordinate : " +
coords[3])
