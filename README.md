#License Plate Recognition Project
------------------

Python version = 3.10.11
Requirements: [detection\requirements.txt](https://github.com/rankum26/licenseplate-recognition-kumarran26/blob/main/detection/requirements.txt)

#Problem and Motivation
------------------
Every year I drive to the Côte d’Azure by car and there's always traffic jams due to tolls in Italy and France. It would be better if you could just swipe the credit card at the beginning of the highway and have it automatically charge you based on where you exit. This would save time and be more efficient.

This is just one example of how barriers can cause delays and inefficiencies. We see them everywhere, from toll booths to parking garages. Each time we stop to pay a fee or wait for a gate to open, we lose time.

Imagine a world without barriers. With electronic toll collection systems, we could drive through without stopping. We could enter parking garages without taking a ticket.

This is not a dream of the future, it's a reality today. There are already a number of cities and countries that are using these technologies to make their transportation systems more efficient. For example, in the Archhöfe Winterthur parking garage, drivers can pre-register their license plate and payment method in the ParkingPay app, allowing them to enter the garage without taking a ticket. Upon entering, their license plate is recognized and their parking fee is automatically deducted upon exit.

I am passionate about this project because I believe it has the potential to make our lives easier and more efficient.

#Data Collection
------------------
To gather data, I used all available car pictures from my smartphone that clearly show license plates. Although the dataset is not big, it is challenging to find a publicly available dataset with license plates, especially from Switzerland. [Dataset](https://github.com/rankum26/licenseplate-recognition-training-kumarran26/tree/main/data_new/images/train) 

#Annotation
------------------
For the annotation process, I used [CVAT](https://www.cvat.ai/). I uploaded all 249 images to CVAT and manually annotated them, marking the license plates. The annotations were then exported in YOLOv1.1 format, resulting in a set of label files (.txt) corresponding to each image. These label files are crucial for training the model.
![alt text](/README_pictures/image.png)

#Training
------------------
The training section of the project is excluded from this repository because it became too cluttered, lost its clarity and it's easy to copy-paste the trained model into the model folder here. You can find the training repository [here](https://github.com/rankum26/licenseplate-recognition-training-kumarran26). In that repository, I trained the model for 100 epochs, which took approximately 8.5 hours. Shorter training sessions did not yield usable results.

![alt text](/README_pictures/image4.png)

The training process generated valuable metrics such as confusion matrices, F1 curves, precision-recall curves, and detailed training and validation logs.
![alt text](/README_pictures/image2.png)

The best model from the training process is stored as best.pt in the runs/detect/trainXX folder, which you can find in the training repository. Copy this model and place it in this project's detection/model directory. This repository already includes the best.pt model for your convenience, but you can replace it with your own trained model if desired.

#Running the Application
------------------

Python version = 3.10.11
install requirements.txt

To run the Flask application, use the following command:
python app.py

The application provides a frontend where you can upload an image. If you don't have images of cars with license plates, you can use the provided example images in the example_pictures folder. After uploading an image, click the green submit button. The model will attempt to recognize the license plate and extract the characters with OCR. The output will display the recognized characters along with the confidence score.
Additionally, the page will show the uploaded image, the recognized plate, and a grayscale thresholded version of the plate. You can repeat the process by clicking "Upload another image."
![alt text](/README_pictures/image3.png)


#Help or Questions
------------------
If you need help don't hesitate to contact me over Teams: kumarran@students.zhaw.ch 
Otherwise you can [ask my bestfriend](https://chatgpt.com/) :D 