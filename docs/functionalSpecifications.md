# BACKGROUND
 
Create a multiclass image classification tool that can correctly identify landmarks (tentatively within Washington state) if given an image. 

# USER STORIES 

## USER 1: Tourist- Bob 
Bob is a tourist in the state of Washington, who is seeing a lot of cool buildings, and does not know how to easily look up the landmarks he's seeing. He will take pictures of the landmarks he is curious about and upload them to the web app. He needs an easy to use user interface, and easily understandable output from the website- that does not assume he is an expert on the local area or machine learning. He needs to be able to take pictures, upload them, and ability to use the internet. After he uploads the image, the display needs to show what the model classified the landmark as and its confidence level. If it cannot classify the image to a set level of confidence, it will tell him it cannot be classified. If Bob is going to Spokane for the day and wants to know if landmarks on his trip can be classified by the model, he can use the search page to search for a landmark. If a landmark he wants to try to see is not on the list, he can submit a feedback form to ask for the model to be trained to identify it. 

## TECHNICIAN 1: ML model maintainer
The technician will be maintaining the image classification model. They need the ability to update the data, fine tune the model, and retrain the model with any new data. They would have to monitor user requests for new landmarks, and feedback from incorrect model output. They need access to the existing requirements.txt file, and update it as any new requirements arise. 

# DATA SOURCES

* Images of Landmarks across the world, provided by [Google](https://github.com/cvdfoundation/google-landmark?tab=readme-ov-file)
  * More than 4 million labeled landmark photos
  * **Structure:** train.csv is a table with fields "image id, image url, landmark id"
* [Wikimedia](https://www.wikimedia.org/) 
  * (specifically, the Wikimedia link for a given landmark)
  * Determine location information about a landmark
  * Provide additional information about a landmark
  * **Structure:** html data processed to create relational data table in .csv file
  * **Join::** Wikimedia data was scraped from the link in the Google Landmarks dataset. This data was then concatenated together based on the url. The Google Landmarks dataset was filtered to remove images that did not contain landmarks. A left join was used to create a table with landmark id, landmark details, and only clean image urls. 
* User-taken Photos of Landmarks in Washington
  * Use to validate model & demonstrate model accuracy and precision
  * **Structure:** jpg files

# USE CASES

## Use Case 1: 
Objective: User wants to upload photo and view results
- user input: user navigates to home page and clicks on "Classifier" tab
- system: website displays guidelines on photo best practices and an upload photo button
- user: clicks "upload photo" button, and uploads photo from their computer 
- System: Loading icons show while classifier is running. 
- System: Displays name, category, location, and accuracy score for landmark classification. 

## Use Case 2: 
Objective: User uploads photo that we can't identify
- user input: user navigates to home page and clicks on "Classifier" tab
- system: website displays guidelines on photo best practices and an upload photo button
- user: clicks "upload photo" button, and uploads photo from their computer 
- System: Displays loading icone while classifier is running. 
- System: Displays name, category, location, and accuracy score for landmark classification.
- system: If the model cannot identify the landmark present in the photo, it displays the top 5 most likely model guesses. 

## Use Case 3: 
Objective: User comes to the website to search for landmark 
- user: searches for a specific landmark 
- system: if landmark exists in the model, the name, location, category, and a map for the landmark are displayed

## Use Case 4: 
Objective: User leaves feedback on missing landmark 
- user: searches for a specific landmark on 'Search' page
- system: landmark not present in our model, so it displays a message saying this landmark is missing
- user: navigates to 'Feedback' page
- System: displays simple open-text form that allows user to input what landmark they want to see included in the future

