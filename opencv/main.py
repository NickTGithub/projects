from Detector import *
import os

videoPath = 1
modelPath = 'model_data/frozen_inference_graph.pb'
configPath = 'model_data/ssd_mobilenet_v3_large_coco.pbtxt'
classesPath = 'model_data/coco.names'

def main():
    videoPath = 1

    configPath = os.path.join("model_data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("model_data", "frozen_inference_graph.pb")
    classesPath = os.path.join("model_data", "coco.names")

    detector = Detector(videoPath, configPath, modelPath, classesPath)
    detector.onVideo()

if __name__ == '__main__':
    main()

