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
import skimage.transform as skt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

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
    """

    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomTranslation(0.1, 0.1),
        layers.RandomBrightness(0.1),
        layers.RandomContrast(0.1)
    ], name="data_augmentation")

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
    return history, model


def plot_model_accuracy(model_history):
    """
    Function to plot the model accuracy.
    parameters:
        model_history: the history of the model
    returns:
        plt: the plot of the model accuracy
    """

    plt.plot(model_history.history['accuracy'], label='accuracy')
    plt.plot(model_history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')

    plt.show()
    return plt

def plot_model_loss(history):
    """ 
    Function to plot the model loss.
    parameters:
        history: the history of the model
    returns:
        plt: the plot of the model loss
    """
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label = 'val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='upper right')

    plt.show()
    return plt

def plot_model_auc(history):
    """
    Function to plot the model AUC.
    parameters:
        history: the history of the model
    returns:
        plt: the plot of the model AUC
    """
    plt.plot(history.history['auc'], label='auc')
    plt.plot(history.history['val_auc'], label = 'val_auc')
    plt.xlabel('Epoch')
    plt.ylabel('AUC')
    plt.legend(loc='lower right')
    plt.ylim(0.58,1.01)

    plt.show()
    return plt

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

def test_personal_images(model, washington_data_cleaned):
    """
    Function to test the model on personal images.
    Prints the top five guesses for each personal image.
    Parameters:
        model: the trained model
        washington_data_cleaned: the cleaned Washington data
    Returns:
        None
    """
    img_needle = load_image("walandmarks/notebooks/personal_test_images/space_needle_1.jpg")
    img_chinatown = load_image("walandmarks/notebooks/personal_test_images/Chinatown_gate.jpg")
    img_fountain = load_image("walandmarks/notebooks/personal_test_images/fountain.jpg")

    img_needle_resized = skt.resize(np.array(img_needle), (224, 224, 3), anti_aliasing=True)
    img_chinatown_resized = skt.resize(np.array(img_chinatown), (224, 224, 3), anti_aliasing=True)
    img_fountain_resized = skt.resize(np.array(img_fountain), (224, 224, 3), anti_aliasing=True)

    img_needle_resized = keras.applications.efficientnet.preprocess_input(
        img_needle_resized * 255
    ).astype(int)
    img_chinatown_resized = keras.applications.efficientnet.preprocess_input(
        img_chinatown_resized * 255
    ).astype(int)
    img_fountain_resized = keras.applications.efficientnet.preprocess_input(
        img_fountain_resized * 255
    ).astype(int)

    image_batch = np.array([img_needle_resized, img_chinatown_resized, img_fountain_resized])

    output = model.predict(image_batch)

    classes = np.sort(washington_data_cleaned['name'].unique())
    for picture in output:
        guesses = np.argsort(picture)[-5:]
        print(np.round(picture[guesses][::-1], 3))

        for guess in guesses[::-1]:
            print(classes[guess])

        print("----------")

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

    test_loss, test_acc, test_auc, test_top_five_accuracy = (
        model.evaluate(x_test, y_test, verbose=2)
    )
    print(f"Test loss: {test_loss}")
    print(f"Test accuracy: {test_acc}")
    print(f"Test AUC: {test_auc}")
    print(f"Test top five accuracy: {test_top_five_accuracy}")

    return test_loss, test_acc, test_auc, test_top_five_accuracy

def create_dist_top_incorrect_guess_confidence_plot(x_test, y_test, model, washington_data_cleaned):
    """
    Function to create a boxplot of the distribution of the top guess
    confidence when the model is incorrect.
    Parameters:
        x_test: the test image data
        y_test: the test image labels
        model: the trained model
        washington_data_cleaned: the cleaned Washington data
    Returns:
        None
    """

    test_output = model.predict(x_test)
    classes = np.sort(washington_data_cleaned['name'].unique())
    index=0
    inaccurate_guess_confidence = []

    ## Check if correct output is in the most confident output:
    for single_guess_output in test_output:
        guesses = np.argsort(single_guess_output)[-1:]
        actual_test_label_index = np.argmax(y_test[index])
        actual_label = classes[actual_test_label_index]

        prioritized_guesses = guesses[::-1]
        guess = classes[prioritized_guesses[0]]
        index+=1

        if guess != actual_label:
            inaccurate_guess_confidence.append(single_guess_output[prioritized_guesses[0]])

    mean_value = np.mean(inaccurate_guess_confidence)
    plt.boxplot(inaccurate_guess_confidence)
    plt.scatter(1, mean_value, color='red', zorder=3)
    plt.text(1.09, mean_value+.015, f'Mean: {mean_value:.3f}', color='red')
    plt.text(1.08, np.median(inaccurate_guess_confidence),
             f'Median: {np.median(inaccurate_guess_confidence): .3f}', color='darkorange')
    plt.ylabel("Model Confidence of Top Guess")
    plt.title("Distribution of Top Guess Confidence when Incorrect")
    plt.show()



def create_train_analyze_model(
        save_model_flag,
        save_model_path_name,
        dropout_rate = 0.3,
        img_dimension = (224, 224, 3)
        ):
    """
    Function to create model acrchigecture,
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

    washington_data_cleaned = load_model_data()
    washington_data_cleaned = washington_data_cleaned[['name', 'image_id', 'image_data']]

    encoder = OneHotEncoder(handle_unknown='ignore')
    encoder.fit(pd.DataFrame(washington_data_cleaned['name']))
    washington_images_stack = np.stack(washington_data_cleaned['image_data'], axis=0)

    x_train, x_test, x_val, y_train, y_test, y_val = (
        create_train_test_val_split(washington_images_stack, encoder.transform(
            pd.DataFrame(washington_data_cleaned['name'])).toarray()
        )
    )

    model_architecture = create_model_architecture(
        washington_data_cleaned['name'].nunique(),
        dropout_rate,
        img_dimension)
    trained_model = train_model(model_architecture, x_train, y_train, x_val, y_val)

    if not isinstance(trained_model, keras.Model):
        raise TypeError("Model is not a Keras model")

    test_model_on_test_data(trained_model, x_test, y_test)
    create_dist_top_incorrect_guess_confidence_plot(x_test,
                                                    y_test,
                                                    trained_model,
                                                    washington_data_cleaned)
    if save_model_flag:
        save_model(trained_model, save_model_path_name)
