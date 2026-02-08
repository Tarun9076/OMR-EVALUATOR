# Overview
This project is a Python-based Optical Mark Recognition (OMR) Evaluation System designed to automatically evaluate scanned OMR answer sheets used in schools, colleges, and competitive examinations.

The system uses template-based OMR detection combined with computer vision techniques to achieve high accuracy. Users can upload their own answer keys in Excel, CSV, or JSON format, upload scanned OMR sheets, and instantly receive evaluated results with downloadable reports.

#Tech Stack
1-Python
2-OpenCV
3-NumPy
4-Pandas
5-Pillow
6-Streamlit

# How the System Works

1. Answer Key Upload
Users can upload answer keys in Excel, CSV, or JSON format. The system converts this into a dictionary mapping question numbers to correct answers.

2. OMR Sheet Upload
The user uploads a scanned OMR sheet image, which is converted into a NumPy array for processing.

3. Image Preprocessing
The image is converted to grayscale, blurred to reduce noise, and thresholded so filled bubbles become clearly visible.

4. Template-Based Detection
Instead of guessing bubble positions, the system uses a predefined JSON template containing exact bubble coordinates, improving accuracy.

5. Evaluation Logic
For each question, the system calculates the fill ratio of each bubble. Multiple marks are flagged as invalid, and results are compared with the answer key.

6. Result Generation
The system generates per-question results, confidence scores, and total marks.

7. Download Results
Results can be downloaded in CSV or JSON format.

# Use Cases
1-School and college examinations
2-Practice tests
3-Competitive exams
4-Academic projects

Author
Tarun Kumar
B.Tech CSE (AI & ML)
