# Reel-Radar
Reel Radar is a Django web application for recommending movies to users based on inputted movies. The main idea is that users can input three movies that they
like and Reel Radar will provide them with five movies closest to their three selections. 

Logic: Reel Radar uses a content based filtering approach to recommend movies based on the genres of the inputted movies. This matrix contains the cosine similarity 
scores between all pairs of movies in the dataset. The cosine similarity is a measure that calculates the cosine of the angle between two vectors. It is a judgement 
of orientation and not magnitude: the two vectors may be completely different in length but if they’re pointing in the same direction, it makes sense they are 
seen as similar. When users input their movies the backend obtains their distinct index from the database. With the movie indexes, Reel Radar then adds up the 
similarity scores with all other movies, effectively calculating a running total of similarities. enumerate the final similarity scores, creating a list of tuples 
where each tuple contains a movie's index and its similarity score. Then it sorts this list of tuples based on the similarity score in descending order. Reel Radar
then looks past movies recommended that were user inputs to select the top 5 most similar movies. This is easily scalable to handle more user inputted movies and 
more recommendations. The three inputs and five recommendations were purely a stylistic choice for the user experience.


Data: MovieLens developer dataset was used and consists of 9741 movies, the list was last updated in 2018, so no movie made past that date will be included. A 
Postgresql database was set up to handle the data. 
