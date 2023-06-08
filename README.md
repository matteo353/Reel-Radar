# Reel Radar
Reel Radar is a Django web application for recommending movies to users based on inputted movies. The main idea is that users can input three movies that they
like and Reel Radar will provide them with five movies closest to a combination of their three selections. 

## Logic
Reel Radar uses a content based filtering approach to recommend movies based on the genres of the inputted movies. It uses a consine similarity matrix created using SKlearn and imported into the project. The cosine similarity is a measure that calculates the cosine of the angle between two vectors. It is a judgement of orientation and not magnitude: the two vectors may be completely different in length but if they’re pointing in the same direction, it makes sense they are seen as similar. When users input their movies the backend obtains their distinct index from the database. With the movie indexes, Reel Radar then adds up the 
similarity scores with all other movies, effectively calculating a running total of similarities. It then enumerates the final similarity scores, creating a list 
of tuples where each tuple contains a movie's index and its similarity score. Then it sorts this list of tuples based on the similarity score in descending order. Reel Radar then looks past movies recommended that were user inputs to select the top 5 most similar movies. This is easily scalable to handle more user inputted movies and more recommendations. The three inputs and five recommendations are purely a stylistic choice for the user experience.

## Data
MovieLens developer dataset was used and consists of 9741 movies, the list was last updated in 2018, so no movie made past that date will be included. A 
Postgresql database was set up to handle the data. 

## UI/UX
The application uses a fresh looking color scheme making use of emerald green, imperial blue, and eggshell. The layout is simple and straightforward, 
allowing users to engage in the use of the website without being distracted by anything unimportant. There are two pages: a homepage and recommendation page with
buttons allowing for easy access back to the homepage if the user wants to use the application again.
