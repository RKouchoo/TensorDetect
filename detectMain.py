'''
Main detect class that is run on the pi/phone/jetson

anything that has an '_' is tensorflow related
anything that is camel case is networking/camera stuff
'''


import numpy as np
import os
import tensorflow as tf
import cv2

import Constants

# PI camera stuff that has to be replaced later.
from picamera.array import PiRGBArray
from picamera.array import PiRGBAnalysis
from picamera import PiCamera

import sys
import time

# Import utilities
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from object_detection.utils import label_map_util

# Define import paths
PATH_TO_CKPT = 'output_inference_graph-1.4.1.pb/frozen_inference_graph.pb' # Import frozen model
PATH_TO_LABELS = 'frc_label_map.pbtxt' # Import map of labels

# Load frozen model into memory
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name = '')

# Load Label Map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes = Constants.tensor.NUM_CLASSES, use_display_name = True)
category_index = label_map_util.create_category_index(categories)

# Helper function for data format
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


# Define function for detecting objects within an image
def detect_objects(image_np, sess, detection_graph):
  #Define input
  image_np_expanded = np.expand_dims(image_np, axis=0)
  image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

  #Define outputs
  detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
  detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
  detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
  num_detections = detection_graph.get_tensor_by_name('num_detections:0')

  options = tf.RunOptions(trace_level = tf.RunOptions.FULL_TRACE)
  run_metadata = tf.RunMetadata()

  #Predict
  (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict = {image_tensor: image_np_expanded})

  return image_np


def detect_image_webcam(image, sess, detection_graph, debugDisplay):

  # Format data
  image = cv2.resize(image, (Constants.vision.CAMERA_WIDTH, Constants.vision.CAMERA_HEIGHT))
  image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  # Detect objects
  image_np = detect_objects(image_np, sess, detection_graph)

  if debugDisplay:
      cv2.imshow('img', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))
      cv2.waitKey(1)

  return image_np

def detect_objects_coords(image_np, sess, detection_graph):
    # Define input
    image_np_expanded = np.expand_dims(image_np, axis = 0)
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Define outputs
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    options = tf.RunOptions(trace_level = tf.RunOptions.FULL_TRACE)
    run_metadata = tf.RunMetadata()

    # Predict
    (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections], feed_dict={image_tensor: image_np_expanded})

    # Find object vertices
    box_coords = []
    for i in range(0, len(scores[0])):
        if scores[0][i] > Constants.tensor.MINIMUM_SCORE_THRESHOLD:
            box = boxes[0, i]
            box_coords.append(box)
        return box_coords


def detect_image_coords(image_path, sess, detection_graph):
    #Import image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (Constants.vision.CAMERA_WIDTH, Constants.vision.CAMERA_HEIGHT))
    image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #Detect objects
    coords = detect_objects_coords(image_np, sess, detection_graph)
    return coords

# Detect images
if (__name__ == '__main__'):
    # Start Session
    with detection_graph.as_default():
        sess = tf.Session(graph = detection_graph, config = tf.ConfigProto(intra_op_parallelism_threads = Constants.machine.MACHINE_CONCURRENT_TENSORFLOW_THREADS))

    # Loop through webcam frames
    cam = PiCamera()
    cam.awb_mode = 'off'
    cam.awb_gains = (1.15, 2.46)
    cam.exposure_mode = 'auto'
    cam.framerate = 30
    cam.rotation = 270
    cam.shutter_speed = 10000
    cam.resolution = (Constants.vision.CAMERA_WIDTH, Constants.vision.CAMERA_HEIGHT)

