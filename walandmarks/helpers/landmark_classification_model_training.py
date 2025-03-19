"""
This script contains functions to train a model to classify 
images of Washington landmarks.
"""

import glob
import os
from PIL import Image

import keras
from keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

def load_model_data():
    """
    Load the data from the images folder and create a dataframe 
    with the image data, name, and image id.
    """
    image_files = glob.glob("walandmarks/data/images/**/*.jpg", recursive=True)
    washington_data = pd.DataFrame({'file_path': image_files})

    # getting file_path, name, image_id, and image_data for each
    # image that we found in the images folder!
    washington_data['parent_file_path'] = (
        washington_data['file_path'].apply(os.path.dirname)
    )
    washington_data['name'] = (
        washington_data['file_path'].apply(lambda x: os.path.basename(os.path.dirname(x)))
    )
    washington_data['image_id'] = (
        washington_data['file_path'].apply(lambda x: os.path.basename(x).split('.')[0])
    )
    washington_data['image_data'] = (
        washington_data['file_path'].apply(lambda x: np.asarray(Image.open(x)))
    )
    return washington_data

def create_train_test_val_split(washington_images_stack, labels_onehot):
    """
    Function that creates the training, test, and validation sets
    for the model. Train: 64%, Validation: 16%, Test: 20%
    Parameters: 
        washington_images_stack: The image data for the model
        labels_onehot: The onehot-encoded labels for the model 
            (a.k.a. landmark names that are onehot-encoded)
    Returns: 
        x_train: The training image data
        x_test: The test image data
        x_val: The validation image data
        y_train: The test image labels
        y_test: The test image labels
        y_val: The validation image labels
    """

    x_train, x_test, y_train, y_test = train_test_split(washington_images_stack,
                                                        labels_onehot,
                                                        test_size=0.2,
                                                        random_state=42)
    x_train, x_val, y_train, y_val = train_test_split(x_train,
                                                      y_train,
                                                      test_size=0.2,
                                                      random_state=42)
    return x_train, x_test, x_val, y_train, y_test, y_val

def create_data_augmentation():
    """
    Function to set the data augmentation. 
    Broken-out into separate function for testing.
    """

    return keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomTranslation(0.1, 0.1),
        layers.RandomBrightness(0.1),
        layers.RandomContrast(0.1)
    ], name="data_augmentation")

def create_model_architecture(num_classes, dropout_rate, img_dimension):
    """
    Function that sets up model architecture that
    includes transfer learning using EfficientNetB0.
    Parameters:
        num_classes: The number of classes in the model
        dropout_rate: The dropout rate for the model
        img_dimension: The image dimension for the model
    Returns:
        model: The model architecture
    Raises:
        TypeError: if num_classes is not an integer
        TypeError: if dropout_rate is not a float
        TypeError: if img_dimension is not a tuple 
    """
    if not isinstance(num_classes, int):
        raise TypeError("num_classes must be an integer")
    if not isinstance(dropout_rate, float):
        raise TypeError("dropout_rate must be a float")
    if not isinstance(img_dimension, tuple):
        raise TypeError("img_dimension must be a tuple")
    if dropout_rate >1 or dropout_rate <0:
        raise ValueError("dropout rate mustt be between 0.0 and 1.0")

    data_augmentation = create_data_augmentation()

    # takes input data, augments, and preps it for EfficientNetB0
    inputs = layers.Input(shape=img_dimension)
    x = data_augmentation(inputs)
    x = keras.applications.efficientnet.preprocess_input(x)

    # preps EfficientNetB0 model (with its weights) to train with our model
    base_model = keras.applications.EfficientNetB0(
        include_top=False, input_tensor=None, weights='imagenet'
    )
    base_model.trainable = False

    # layers to train the model with our data
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)

    x = layers.BatchNormalization()(x)
    x = layers.Dropout(dropout_rate)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    return models.Model(inputs, outputs)

def train_model(model, x_train, y_train, x_val, y_val):
    """
    Function that trains the model using the training and validation data.
    Parameters:
        model: The model architecture
        x_train: The training image data
        y_train: The training image labels
        x_val: The validation image data
        y_val: The validation image labels
        batch_size: The batch size for the model
        epochs: The number of epochs for the model
    Returns:
        history: The model training history
        model: The trained model as a Keras model
    """
    if not isinstance(model, keras.Model):
        raise TypeError("model must be a keras model")

    for ds in [x_train, y_train, x_val, y_val]:
        if not isinstance(ds, np.ndarray):
            raise TypeError("x_train, y_train, "
            "x_val and y_val must be ndarrays") 

    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=5, restore_best_weights=True
    )

    optimizer = keras.optimizers.Adam(learning_rate=1e-3)
    auc_metric = keras.metrics.AUC(multi_label=True)
    top_five_accuracy_metric = keras.metrics.TopKCategoricalAccuracy(k=5)

    model.compile(optimizer=optimizer,
                loss= keras.losses.CategoricalCrossentropy(from_logits=False),
                metrics=['accuracy', auc_metric, top_five_accuracy_metric])

    history = model.fit(
        x_train,
        y_train,
        epochs=10,
        batch_size=64,
        validation_data = (x_val, y_val),
        callbacks=[early_stopping]
    )

    return (history, model)

def plot_model_metric(history, metric):
    """
    Function to plot the model AUC.
    parameters:
        history: the history of the model
    returns:
        plt: the plot of the model AUC
    """
    if not isinstance(metric, str):
        raise TypeError("metric must be a string")
    if metric not in ("loss", "accuracy", "auc"):
        raise ValueError("metric must be 'loss', 'accuracy', or 'auc'")
    if not isinstance(history, keras.callbacks.History):
        raise TypeError("history must be a Keras history object")

    if metric == "loss":
        plt.plot(history.history['loss'], label='loss')
        plt.plot(history.history['val_loss'], label = 'val_loss')
        plt.ylabel('Loss')
        plt.legend(loc='upper right')

    elif metric == "accuracy":
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
        plt.ylabel('Accuracy')
        plt.legend(loc='lower right')

    else:
        plt.plot(history.history['auc'], label='auc')
        plt.plot(history.history['val_auc'], label = 'val_auc')
        plt.ylabel('AUC')
        plt.legend(loc='lower right')

    plt.xlabel('Epoch')
    plt.show()

def save_model(model, model_path_name):
    """
    Save the model to a specified path.
    Made into a function so as to not accidentally overwrite the model.
    Parameters: 
        model: the .keras model to be saved
        model_path_name: the path to save the model
    Returns:
        None
    """
    if not isinstance(model_path_name, str):
        raise TypeError("model_path_name must be a string")
    if not isinstance(model, keras.Model):
        raise TypeError("The model must be a Keras model")

    model.save(model_path_name)

def load_image(image_path):
    """
    Function to get image data from filepath.
    Parameters:
        filename: the file path of the image
    Returns:
        data: the image data
    Raises:
        TypeError: if the filename is not a string.
    """
    if not isinstance(image_path, str):
        raise TypeError("filename must be a string")

    img = Image.open(image_path)
    img.load()
    data = np.asarray( img, dtype="uint8" )
    return data

def test_model_on_test_data(model, x_test, y_test):
    """
    Function to test the model on the test data.
    Prints the test loss, accuracy, AUC, and top five accuracy.
    Parameters:
        model: the trained model
        x_test: the test image data
        y_test: the test image labels
    Returns:
        test_loss: the test loss
        test_acc: the test accuracy
        test_auc: the test AUC
        test_top_five_accuracy: the test top five accuracy
    """
    if not isinstance(model, keras.Model):
        raise TypeError("The model must be a Keras model")
    if not isinstance(x_test, np.ndarray):
        raise TypeError("x_test must be a numpy array")
    if not isinstance(y_test, np.ndarray):
        raise TypeError("y_test must be a numpy array")

    test_loss, test_acc, test_auc, test_top_five_accuracy = (
        model.evaluate(x_test, y_test, verbose=2)
    )

    return test_loss, test_acc, test_auc, test_top_five_accuracy

def create_train_analyze_model(
        save_model_flag,
        save_model_path_name="walandmarks/model/test_model.keras",
        dropout_rate = 0.3,
        img_dimension = (224, 224, 3)
        ):
    """
    Function to create model architecture,
    train the model, display model metrics, 
    and test the model on personal images.
    Parameters:
        None
    Returns:
        model: trained model
        accuracy_plot: plot of model accuracy
        loss_plot: plot of model loss
        auc_plot: plot of model auc
        top_five_accuracy_plot: plot of model top five accuracy
    """

    if not isinstance(save_model_flag, bool):
        raise TypeError("save_model_flag must be a boolean")
    if not isinstance(save_model_path_name, str):
        raise TypeError("save_model_path_name must be a string")
    if not isinstance(dropout_rate, float):
        raise TypeError("dropout rate must be a float!")
    if not isinstance(img_dimension, tuple):
        raise TypeError("img_dimension must be a tuple!")

    washington_data_cleaned = load_model_data()[['name', 'image_id', 'image_data']]
    encoder = OneHotEncoder(handle_unknown='ignore').fit(
        pd.DataFrame(washington_data_cleaned['name'])
    )

    x_train, x_test, x_val, y_train, y_test, y_val = create_train_test_val_split(
        np.stack(washington_data_cleaned['image_data'], axis=0), encoder.transform(
            pd.DataFrame(washington_data_cleaned['name'])
        ).toarray()
    )

    model_architecture = create_model_architecture(
        washington_data_cleaned['name'].nunique(), dropout_rate, img_dimension
    )
    model_history, trained_model = train_model(model_architecture,
                                                x_train,
                                                y_train,
                                                x_val,
                                                y_val)

    test_model_on_test_data(trained_model, x_test, y_test)
    plot_model_metric(model_history, "loss")
    plot_model_metric(model_history, "accuracy")
    plot_model_metric(model_history, "auc")

    if save_model_flag:
        save_model(trained_model, save_model_path_name)
