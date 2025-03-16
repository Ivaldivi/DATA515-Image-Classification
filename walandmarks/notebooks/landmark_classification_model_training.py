import glob
import random

from keras import datasets, layers, models
from keras.applications import EfficientNetB0
from keras.applications.efficientnet import preprocess_input
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from skimage.transform import resize
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import tensorflow as tf

def load_data():
    image_files = glob.glob("../data/**/*.jpg", recursive=True)

    # Create a DataFrame with the file paths
    washington_data = pd.DataFrame({'file_path': image_files})

    # Parse file paths in a platform-independent way
    washington_data['parent_file_path'] = washington_data['file_path'].apply(lambda x: os.path.dirname(x))
    washington_data['name'] = washington_data['file_path'].apply(lambda x: os.path.basename(os.path.dirname(x)))
    washington_data['image_id'] = washington_data['file_path'].apply(lambda x: os.path.basename(x).split('.')[0])

    # If you absolutely need all images loaded at once, you can do:
    # Warning: This might cause memory issues with large datasets
    washington_data['image_data'] = washington_data['file_path'].apply(lambda x: np.asarray(Image.open(x)))
    
    return washington_data

washington_data = load_data()
washington_data_cleaned = washington_data[['name', 'image_id', 'image_data']]

encoder = OneHotEncoder(handle_unknown='ignore')
encoder.fit(pd.DataFrame(washington_data_cleaned['name']))

labels_onehot = encoder.transform(pd.DataFrame(washington_data_cleaned['name'])).toarray()

washington_images_stack = np.stack(washington_data_cleaned['image_data'], axis=0)

def create_train_test_val_split(washington_images_stack, labels_onehot):
    x_train, x_test, y_train, y_test = train_test_split(washington_images_stack, labels_onehot, test_size=0.2, stratify=labels_onehot)

    x_train, x_val, y_train, y_val = train_test_split(
    x_train, y_train, test_size=0.2, stratify=y_train
    )
    return x_train, x_test, x_val, y_train, y_test, y_val

x_train, x_test, x_val, y_train, y_test, y_val = create_train_test_val_split(washington_images_stack, labels_onehot)

num_classes = washington_data_cleaned['name'].nunique()
dropout_rate = 0.3
img_dimension = (224, 224, 3)

def create_model_architecture(num_classes, dropout_rate, img_dimension):
    data_augmentation = tf.keras.Sequential([
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
    x = preprocess_input(x)

    # preps EfficientNetB0 model (with its weights) to train with our model
    base_model = EfficientNetB0(include_top=False, input_tensor=None, weights='imagenet')
    base_model.trainable = False

    # layers to train the model with our data
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)

    x = layers.BatchNormalization()(x)
    x = layers.Dropout(dropout_rate)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    return models.Model(inputs, outputs)

def train_model(model, x_train, y_train, x_val, y_val, batch_size=32, epochs=10):
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
    auc_metric = tf.keras.metrics.AUC(multi_label=True)
    top_five_accuracy_metric = tf.keras.metrics.TopKCategoricalAccuracy(k=5)

    EPOCHS = 10 
    BATCH_SIZE = 64

    model.compile(optimizer=optimizer,
                loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
                metrics=['accuracy', auc_metric, top_five_accuracy_metric])

    history = model.fit(
        x_train,
        y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_data = (x_val, y_val),
        callbacks=[early_stopping]
    )
    return history, model



def plot_model_accuracy(model_history): 
    plt.plot(model_history.history['accuracy'], label='accuracy')
    plt.plot(model_history.history['val_accuracy'], label = 'val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')

    plt.show()

def plot_model_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label = 'val_loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='upper right')

    plt.show()

def plot_model_auc(history):
    print(history.history.keys())
    plt.plot(history.history['auc_6'], label='auc')
    plt.plot(history.history['val_auc_6'], label = 'val_auc')
    plt.xlabel('Epoch')
    plt.ylabel('AUC')
    plt.legend(loc='lower right')
    plt.ylim(0.58,1.01)
    plt.show()

def save_model(model, model_path_name):
    """
    Save the model to a specified path.
    Made into a function so as to not accidentally overwrite the model.
    """
    
    model.save(model_path_name)


def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="uint8" )
    return data

def test_personal_images(model):
    img_needle = load_image("../notebooks/personal_test_images/space_needle_1.jpg")
    img_chinatown = load_image("../notebooks/personal_test_images/Chinatown_gate.jpg")
    img_fountain = load_image("../notebooks/personal_test_images/fountain.jpg")

    img_needle_resized = resize(np.array(img_needle), (224, 224, 3), anti_aliasing=True)
    img_chinatown_resized = resize(np.array(img_chinatown), (224, 224, 3), anti_aliasing=True)
    img_fountain_resized = resize(np.array(img_fountain), (224, 224, 3), anti_aliasing=True)

    img_needle_resized = preprocess_input(img_needle_resized * 255).astype(int)
    img_chinatown_resized = preprocess_input(img_chinatown_resized * 255).astype(int)
    img_fountain_resized = preprocess_input(img_fountain_resized * 255).astype(int)

    # print(img_needle_resized)

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
    test_loss, test_acc, test_auc, test_top_five_accuracy = model.evaluate(x_test, y_test, verbose=2)
    print(f"Test loss: {test_loss}")
    print(f"Test accuracy: {test_acc}")
    print(f"Test AUC: {test_auc}")
    print(f"Test top five accuracy: {test_top_five_accuracy}")

    return test_loss, test_acc, test_auc, test_top_five_accuracy

def create_dist_top_incorrect_guess_confidence_plot(x_test, model):
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
    median_value = np.median(inaccurate_guess_confidence)
    plt.boxplot(inaccurate_guess_confidence)
    plt.scatter(1, mean_value, color='red', zorder=3)  # Plot the mean point
    plt.text(1.09, mean_value+.015, f'Mean: {mean_value:.3f}', color='red')
    plt.text(1.08, median_value, f'Median: {median_value: .3f}', color='darkorange')
    plt.ylabel("Model Confidence of Top Guess")
    plt.title("Distribution of Top Guess Confidence when Incorrect")
    plt.show()

model = tf.keras.models.load_model('../model/final_EfficientNetb0_WA_landmarks_model.keras')
create_dist_top_incorrect_guess_confidence_plot(x_test, model)