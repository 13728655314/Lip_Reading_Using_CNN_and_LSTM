import cv2
import numpy as np
import glob
from Lip_Reading_Using_CNN_and_LSTM.process_image import mouthTracker as mt
import pandas as pd
import csv

mouth_cascade = cv2.CascadeClassifier('C:\\Users\javinarfamily\\PycharmProjects\\Thesis\\Lip_Reading_Using_CNN_and_LSTM\\process_image\\haarcascade_mcs_mouth.xml')
mouthCsv = 'Lip_Reading_Using_CNN_and_LSTM\\process_image\\mouthData.csv'
pictCount = 16823
evenPicker = 1

for filename in glob.glob('D:\\Datasets\\s5\\*.mpg'):

    frame_counter = 0
    cap = cv2.VideoCapture(filename)
    ds_factor = 0.5

    while True:
        ret, frame = cap.read()

        frame_counter += 1

        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
            break

        mouth_rects = mouth_cascade.detectMultiScale(frame, 1.7, 11)

        for (x, y, w, h) in mouth_rects:
            y = int(y - 0.15 * h)

            if (evenPicker % 2) != 0:
                pictCount += 1
                mask = np.zeros(frame.shape, dtype="uint8")

                # get the coordinates/points of interest
                mouthPoints = mt.getMouthPoints(gray)

                # get  the x and y mean
                ymax = y + h
                xmax = x + w
                pictname = 'pict' + str(pictCount) + '.png'
                maskname = 'mask' + str(pictCount) + '.png'
                cv2.fillPoly(mask, [mouthPoints], (0, 255, 0))

                cv2.imwrite('D:\\Datasets\\picts\\pict' + str(pictCount) + '.png', frame)
                cv2.imwrite('D:\\Datasets\\picts\\mask' + str(pictCount) + '.png', mask)

                with open('mouthData.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)

                    with open('mouthData.csv', 'a', newline='') as csvappend_file:
                        csv_writer = csv.writer(csvappend_file)
                        csv_writer.writerow([pictname, '180', '144', 'Mouth', x, y, xmax, ymax])
                        print('Saved')

                # line of code to save data from the mask to csvfile.
                with open('maskData.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)

                    with open('maskData.csv', 'a+', newline='') as csvappend_file:
                        csv_writer = csv.writer(csvappend_file,delimiter = ',')
                        csv_writer.writerow([maskname, '180', '144', 'Mouth', mouthPoints])
                        print('Saved')

        evenPicker += 1
    # print('Saving pictures from: '+filename)

    cap.release()

# print('Saving pictures done.....')
