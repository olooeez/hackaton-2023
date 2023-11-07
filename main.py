from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

def parse_arguments() -> dict:
    '''Parse CMD arguments'''
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    
    return vars(ap.parse_args())

def load_and_preprocess_image(image_path: str) -> tuple:
    '''Load the image, convert it to grayscale, blur it slightly, then find edges'''

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    return image, gray, edged

def find_document_contour(edged):
    # Find contours in the edge map, then initialize the contour that corresponds to the document
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None

    # Ensure that at least one contour was found
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # Loop over the sorted contours
        for c in cnts:
            # Approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            # If our approximated contour has four points, then we can assume we have found the paper
            if len(approx) == 4:
                docCnt = approx
                break
    
    return docCnt

def preprocess_paper_image(image, gray, docCnt):
    # Apply a four point perspective transform to both the original image and grayscale image to obtain a top-down birds eye view of the paper
    paper = four_point_transform(image, docCnt.reshape(4, 2))
    warped = four_point_transform(gray, docCnt.reshape(4, 2))

    # Apply Otsu's thresholding method to binarize the warped piece of paper
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    return paper, thresh

def find_question_contours(thresh):
    # Find contours in the thresholded image, then initialize the list of contours that correspond to questions
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []

    # Loop over the contours
    for c in cnts:
        # Compute the bounding box of the contour, then use the bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        # In order to label the contour as a question, region should be sufficiently wide, sufficiently tall, and have an aspect ratio approximately equal to 1
        if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
            questionCnts.append(c)

    # Sort the question contours top-to-bottom, then initialize the total number of correct answers
    questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]

    return questionCnts

def analyze_answers(questionCnts, thresh, paper):
    correct = 0
    gab = {}

    # Each question has 5 possible answers, to loop over the question in batches of 5
    for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
        # Sort the contours for the current question from left to right, then initialize the index of the bubbled answer
        cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
        bubbled = None

        # Loop over the sorted contours
        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)

            # Apply the mask to the thresholded image, then count the number of non-zero pixels in the bubble area
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)

            # if the current total has a larger number of total non-zero pixels, then we are examining the currently bubbled-in answer
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)

        # Initialize the contour color and the index of the *correct* answer
        color = (0, 0, 255)
        k = ANSWER_KEY[q]
        gab[q] = bubbled[1]

        # Check to see if the bubbled answer is correct
        if k == bubbled[1]:
            color = (0, 255, 0)
            correct += 1

        cv2.drawContours(paper, [cnts[k]], -1, color, 3)

    return correct, gab

def display_results(paper, correct):
    score = (correct / 5.0) * 100
    cv2.putText(paper, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    cv2.imshow("Exam", paper)
    cv2.waitKey(0)

def wait_user_close():
    # Wait for the user to close the windows (pressing ESC)
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        # Close all OpenCV windows
        cv2.destroyAllWindows()

def main():
    args = parse_arguments()
    image, gray, edged = load_and_preprocess_image(args["image"])
    docCnt = find_document_contour(edged)
    paper, thresh = preprocess_paper_image(image, gray, docCnt)
    questionCnts = find_question_contours(thresh)
    correct, _ = analyze_answers(questionCnts, thresh, paper)
    display_results(paper, correct)

if __name__ == '__main__':
    main()
