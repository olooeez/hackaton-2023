# Import necessary libraries
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# Define the correct answers for each question (0-based index)
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

def load_image(image_path):
    '''Function to load an image from a file'''
    return cv2.imread(image_path)

def preprocess_image(image):
    '''Function to preprocess the image (convert to grayscale, blur, and detect edges)'''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    return gray, edged

def find_document_contour(edged):
    '''Function to find the contour of the document in the image'''
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                return approx.reshape(4, 2)
    return None

def threshold_document(warped):
    '''Function to threshold the document to extract answers'''
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    return thresh

def find_question_contours(thresh):
    '''Function to find contours of the answer bubbles'''
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
            questionCnts.append(c)
    return contours.sort_contours(questionCnts, method="top-to-bottom")[0]

def evaluate_answers(thresh, questionCnts):
    '''Function to evaluate the answers based on bubble detection'''
    correct = 0
    for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
        cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
        bubbled = None
        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            if bubbled is None or total > bubbled[0]:
                bubbled = (total, j)
        k = ANSWER_KEY[q]
        if k == bubbled[1]:
            correct += 1
    return correct

def main():
    '''Main function'''

    # Parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    args = vars(ap.parse_args())

    # Load the input image
    image = load_image(args["image"])
    
    # Preprocess the image
    gray, edged = preprocess_image(image)
    
    # Find the document contour
    docCnt = find_document_contour(edged)

    if docCnt is not None:
        # Apply a perspective transform to the document
        paper = four_point_transform(image, docCnt)
        warped = four_point_transform(gray, docCnt)
        
        # Threshold the document to get binary representation
        thresh = threshold_document(warped)

        # Find contours of the answer bubbles
        questionCnts = find_question_contours(thresh)

        # Evaluate the answers and calculate the score
        correct = evaluate_answers(thresh, questionCnts)

        score = (correct / 5.0) * 100
        print("[INFO] score: {:.2f}%".format(score))

        # Display the score on the image
        cv2.putText(paper, "{:.2f}%".format(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        
        # Show the original image and the processed exam
        cv2.imshow("Original", image)
        cv2.imshow("Exam", paper)

        # Wait for user to close the windows (pressing ESC)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

        # Close all OpenCV windows
        cv2.destroyAllWindows()

# Entry point to the script
if __name__ == "__main__":
    main()
