--- 

author: "Sarah Innis, Anthony Nguyen, Annie Staker, Izzy Valdivia" 

date: "2025-02-27" 

--- 

# Technology Review for Landmark Classification: Which Machine Learning Library is Best for Our Use Case?

## Background
For our project, we hope to identify landmarks in the state of Washington, based on a user-inputted photo. As a result, we will need a Python library that will allow us to build and train a machine learning model for landmark image classification.

## Possible Libraries

We have identified three possible libraries to use to build our convolutional neural network: PyTorch, TensorFlow, and Scikit-Learn.

Pytorch is a complex deep learning framework for machine learning, created by Meta in 2016. Although there is a significant learning curve for PyTorch, it allows for more intensive model development (e.g. with Deep Learning capabilities). TensorFlow is a complex deep learning framework for machine learning, created by Google in 2015. Although there is a significant learning curve for Tensorflow, it also allows for more intensive model development (e.g. with Deep Learning capabilities). Scikit Learn is an accessible machine learning library first created by Dr. David Cournapeau in 2007. It is possibly the most user-friendly library for basic machine learning tasks. It is open source, and the latest version of Scikit Learn is compatible with Python 3.7 and later.

## Comparison
### PyTorch
PyTorch is relatively user-friendly but requires knowledge of deep learning going in. It is very well-documented, and the documentation contains a walkthrough on how to train a basic image classifier using the CIFAR10 dataset. They also have recommendations for other test datasets and image pre-processing libraries so users can easily learn to adjust the model created in the walkthrough. 

This walkthrough tests the capabilities of the PyTorch library as well as the robustness of the documentation and online community. In the tutorial, they describe how to load data, create a transformer, and customize the model by changing the loss calculation and optimizer. There are sections in the documentation that describe different helper packages (tensor.nn and tensor.optim) that are used in the example model development. The documentation is quite thorough and has some recommendations on how to tailor their pre-built models to meet the needs of the one the user is trying to develop. 

There are a few potential downsides of the PyTorch library. There are some basic warnings online from community forums saying PyTorch does not perform as well as TensorFlow on large-scale projects or in a production environment. Although, the model we develop should be relatively lightweight so this may not be a limiting factor. 
The video below shows model status output during training.

<video src="PyTorch-demo.mov" width="320" height="240" controls></video>

### TensorFlow
TensorFlow, like PyTorch, is a powerful framework for performing deep learning capabilities. Users are able to implement and adjust individual CNN layers for their models, allowing for complex functionality. With TensorFlow, however, many aspects of this layer-creation process have been simplified through pre-made classes.

One important feature that we observed was that TensorFlow was much easier to get running out-of-the-box, in comparison to PyTorch. For instance, with PyTorch, we had to create a custom data loader for our data, while TensorFlow worked immediately from our Pandas DataFrame. Additionally, TensorFlow has significant documentation and a mature ecosystem.

As of recently, however, online communities have gravitated toward PyTorch, emphasizing its flexibility, ease of use, and presence in current Deep Learning research papers., For this project, we experimented with both PyTorch and TensorFlow to see which option better suits our needs and goals.

<video src="TensorFlow-demo.mp4" width="320" height="240" controls></video>

### Scikit-Learn
The biggest upside of Scikit Learn is that it is user-friendly. It has a straightforward framework, a robust API, and extensive documentation. There is also a large amount of online support available via forums like Medium, GeeksForGeeks, and Stack Overflow. Additionally, it is useful for training a large number of machine learning models and comparing their performance.

However, Scikit Learn has some downsides. Because of its focus on user-friendliness and catering to beginners, it has more limited capabilities in the deep learning space. Its primary focus is traditional machine learning, so it does not have the extended capabilities for deep and reinforcement learning that are found in PyTorch or TensorFlow. Since we are training a convolutional neural network, we would prefer to use a library that is well-suited for deep learning. That said, we may still use Scikit Learn for tasks that are model-agnostic, such as label encoding, resizing images, and getting a train/test split of the data.

## Final Choice

We have decided to use PyTorch as the primary library for training our model. However, as noted above, we will likely also use Scikit-Learn for performing more general machine learning tasks–label encoding, resizing images, and performing a train/test split of the data.

## Drawbacks

Although PyTorch has strong capabilities for creating Convolutional Neural Networks and is very adaptable for what we need to do, we still need to keep in mind that CNN-based architectures are black box models. As a result, we have limited interpretability of how PyTorch handles and understands our data, making debugging processes much more difficult. Additionally, we will need to continuously refine our model, which may require significant computational resources.