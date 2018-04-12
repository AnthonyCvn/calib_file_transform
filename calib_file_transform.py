#!/usr/bin/env python
""" Transform calibration file.
"""
import os
import linecache
import numpy as np
import cv2

def main():
    input_file_name = "SN17103.yml"
    image_width = 1280
    image_height = 720
    camera_name = "camera"
    distortion_model = "plumb_bob"

    output_text = ""

    fs = cv2.FileStorage("./SN17103.yml", cv2.FILE_STORAGE_READ)

    K1 = fs.getNode("K1").mat()
    K2 = fs.getNode("K2").mat()
    D1 = fs.getNode("D1").mat()
    D2 = fs.getNode("D1").mat()
    R2 = fs.getNode("R").mat()
    T2 = fs.getNode("T").mat().T
    RT2 = np.hstack((R2, T2))
    R1 = np.eye(3, 3)
    T1 = np.zeros((3, 1))
    RT1 = np.hstack((R1, T1))

    P1 = np.dot(K1, RT1)
    P2 = np.dot(K2, RT2)

    output_text += "image_width: " + str(image_width) + "\n"
    output_text += "image_height: " + str(image_height) + "\n"
    output_text += "camera_name: " + camera_name + "\n"

    output_text += "camera_matrix: " + "\n"
    output_text += "  rows: 3" + "\n"
    output_text += "  cols: 3" + "\n"
    output_text += "  data:  " + str(np.reshape(K1, 9).tolist()) + "\n"

    output_text += "distortion_model: " + distortion_model + "\n"

    output_text += "distortion_coefficients: " + "\n"
    output_text += "  rows: 1" + "\n"
    output_text += "  cols: 5" + "\n"
    output_text += "  data:  " + str(np.reshape(D1, 5).tolist()) + "\n"

    output_text += "rectification_matrix: " + "\n"
    output_text += "  rows: 3" + "\n"
    output_text += "  cols: 3" + "\n"
    output_text += "  data:  " + str(np.reshape(R1, 9).tolist()) + "\n"

    output_text += "projection_matrix: " + "\n"
    output_text += "  rows: 3" + "\n"
    output_text += "  cols: 4" + "\n"
    output_text += "  data:  " + str(np.reshape(P1, 12).tolist()) + "\n"


    with open("camera.yaml", "w") as output_file:
        output_file.write(output_text)

    with open("camera.yaml", "r") as verification_file:
        verification_text = verification_file.read()

    print("Output file: \n")
    print(verification_text)



if __name__ == "__main__":
    main()