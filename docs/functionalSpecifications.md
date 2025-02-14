# USER STORIES 

## USER 1: Tourist- Bob 
Bob is a tourist in the state of Washington, who is seeing a lot of cool buildings, and does not know how to easily look up the landmarks he's seeing. He will take pictures of the landmarks he is curious about and upload them to the web app. He needs an easy to use user interface, and easily understandable output from the website- that does not assume he is an expert on architecture or local lore. He needs to be able to take pictures, upload them, have access to wi-fi, and ability to use the internet. 


## USER 2: Architect- Doug (Annie's Dad)
Doug is an architect visiting Seattle for the first time. He wants to figure out the name and architect of the buildings and landmarks he sees. He needs to be able to upload photos, have access to wi-fi, and know how to use the internet. As an architect, he wants to be able to learn the name of the landmark as well as where to learn more about its history. 

## TECHNICIAN 1: ML model maintainer
The technician will be maintaining the image classification model. They need the ability to update the data, fine tune the model, and retrain the model with any new data. They would have to monitor user requests for new landmarks, and feedback from incorrect model output. They need access to the existing requirements.txt file, and update it as any new requirements arise. 


# Use Cases 

## Use Case 1: 
Objective: User wants to upload photo and view results
- user input: user navigates to home page and clicks on "upload photo" tab
- system: website displays guidelines on photo best practices and an upload photo button
- user: clicks "upload photo" button, and uploads photo from their computer 
- System: "Photo Uploaded" message displayed if successful. "We're working on it" or loading screen if it takes more than 3 seconds. 
- Displays name, picture, location, and accuracy score for landmark classification. 

## Use Case 2: 
Objective: User uploads photo that we can't identify
- user input: user navigates to home page and clicks on "upload photo" tab
- system: website displays guidelines on photo best practices and an upload photo button
- user: clicks "upload photo" button, and uploads photo from their computer 
- system: "Photo Uploaded" message displayed if successful. "We're working on it" or loading screen if it takes more than 3 seconds. 
- system: If the model cannot identify the landmark present in the photo, it displays the top 5 most likely model guesses. 

## Use Case 3: 
Objective: User leaves feedback on missing landmark 
- user: searches for a specific landmark 
- system: landmark not present in our model, so it displays a message saying this landmark is missing
- user: clicks on "leave feedback" button at the bottom of searching page
- System: displays simple open-text form that allows user to input what landmark they want to see included in the future

## Use Case 4: 
Objective: User comes to the website to search for landmark 
- user: searches for a specific landmark 
- system: if landmark exists in the model, the name, location, architect, and wikipedia link for the landmark are displayed

## Use Case 5: 
Objective: User Plays landmark guessing game 
- user: clicks on "game" tab 
- system: switches to game tab, with instructions and start button
- user: clicks "start game" 
- system: displays picture of landmark user is supposed to guess, along with interactive map used for placing the guess
- user: clicks the spot on the map that they think corresponds to the landmark's location
- system: if the user guesses within 1 mile of the true landmark location, it displays a congratulations message. If they guess more than a mile away from the true landmark location, it displays "better luck next time." Whether or not the user wins, the website displays information about the landmark. 
