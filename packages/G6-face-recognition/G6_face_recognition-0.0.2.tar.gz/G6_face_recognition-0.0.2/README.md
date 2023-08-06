### A Python package for face recognition.

## Project Description
# Gate6 Face Recognition Package
   G6_face_recognition is a module for face recognition. Using the image processing libraries and high-level mathematical functions, we will provide fast and secure face recognition solution.

## Installation 

#### Installations Required:(Before installing the package module)
  ```
     python 
     numpy
     opencv-python
     matplotlib
     opencv-contrib-python
     requests
     cmake
     dlib
     scikit-image
     scipy
     imutils==0.5.2
  ```  
  
#### - Install Python

[Windows](http://timmyreilly.azurewebsites.net/python-flask-windows-development-environment-setup/), [Mac](http://docs.python-guide.org/en/latest/starting/install/osx/), [Linux](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-linux-python.html)


#### - Install package module using ``pip``:
  ```
    $ pip install G6-face-recognition
  ```  
  
## Project Structure
  
  -   In your project folder, create an **encodingModel** directory.
  -   In the **encodingModel** directory create a file named **faceEncodings.pickle(encodingModel/faceEncodings.pickle)**.
  -   Create a directory named **Input_database**.
  -   In the **Input_database** directory put an individual's face images(in the directories made on their individual names).

```shell

    Project/
    ├── encodingModel/
    │   ├── faceEncodings.pickle/                               # train model
    |   ├── Face_model/                                         # Face model
    |       ├── face_recognition_model.dat/
    |       ├── shape_predictor.dat/
    ├── Input_database/ 
    │   ├── person1 name/                                       # person1 directory
    |   │   ├── face images of person1 /                    # images of person face
    │   ├── person2 name/                                       # person2 directory
    |   │   ├── face images of person2 /                    # images of person face
    │   ├── person3 name/                                       # person3 directory
    |   │   ├── face images of person3 /                    # images of person face                  
 
```

 

## How to use

Once all the settings of project are configured, you are ready to run the project. Import G6_face_recognition module in your project to start.


```shell
   import G6_face_recognition
```

Once the import is completed, users need to copy face models from the link below and paste it in the directory Face_model.

```shell
   https://github.com/gate6/iris-recognition-sample-code/tree/face-recognition/encodingModel/Face_model
```

After that, users need to train existing images (which are saved in the Input_database Folder).

```shell
   Input_database/
```

Once it’s done, create and train encoding module using Input_database Folder images, as per the instructions given below:


```shell
   G6_face_recognition.face_model_train(train_database_path,train_encoding_model_path)
   train_database_path        ===>  Input_database/
   train_encoding_model_path  ===>  encodingModel/faceEncodings.pickle
```

Once the model is trained, it’s ready to test with real-time images. Follow the process that is mentioned to test real time face image:

```shell
   face_name = G6_face_recognition.face_model_test(test_encoding_model_path,real_time_image_path) 
   test_encoding_model_path   ===>  encodingModel/faceEncodings.pickle
   real_time_image_path       ===>  real-time_image_path
   face_name                  ===>  In response you’ll get the registered person’s name. If an image matches with the person’s image in the trained image model it will return as matched & if the image doesn’t match then the name returns as unmatched.
```


## Requirements :

  * Need clearer images from the input device.
  * Images should be captured in light.
  * Person should not wear big glasses or anything that affects their image match.
  * Minimum 5 clear images are required to train the model.




## Support

If you face any difficulty in configuration or while using our  Gate6 Face Recognition Package (as per the instructions documented above), please feel free to contact our development team.

## License

[MIT](LICENSE)