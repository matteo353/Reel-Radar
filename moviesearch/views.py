from django.shortcuts import render
from .models import MovieData
from django.http import HttpResponse
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import boto3
from io import BytesIO
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'index.html')

# Function to update the cache by accessing the similarity matrix stored in AWS S3
def get_similarity_matrix():
    matrix = cache.get('similarity_matrix')

    if matrix is None:
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        obj = s3.get_object(Bucket='reel-radar', Key='similarity_matrix.npy')
        matrix = np.load(BytesIO(obj['Body'].read()), allow_pickle=True)

        # Store the file in cache for future use
        cache.set('similarity_matrix', matrix)

    return matrix


def recommend(request):
    movie1 = request.POST['movie1']
    movie2 = request.POST['movie2']
    movie3 = request.POST['movie3']

    movies = [movie1, movie2, movie3]
    fetched_movies = []
    movie_indexes = []

    for movie in movies:
        try:
            fetched_movie = MovieData.objects.filter(title__istartswith=movie).first()
            fetched_movies.append(fetched_movie.title)
            movie_indexes.append(int(fetched_movie.index))

        except MovieData.DoesNotExist:
            fetched_movie = 'Movie Not Found in Database'
            fetched_movies.append(fetched_movie)

    # Names of fetched movies if found, if not "Movie Not Found in Database"
    movie1 = fetched_movies[0]
    movie2 = fetched_movies[1]
    movie3 = fetched_movies[2]

    # Un-comment if fetching from the cloud
    # similarity_matrix = get_similarity_matrix()

    # Load cosine similarity matrix
    similarity_matrix = np.load('similarity_matrix.npy')

    # Initialise empty cosine matrix
    final_sim = np.zeros(similarity_matrix.shape[0])

    # Compute running total of cosine similarity for each movie
    for index in movie_indexes:

        # update final matrix
        final_sim += similarity_matrix[index]

    # Number each value
    sim_scores = list(enumerate(final_sim))

    # Sort the matrix
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_five_indexes = []
    count = 0
    for movie in sim_scores:
        if count == 5:
            break
        if movie[0] != movie_indexes[0] and movie[0] != movie_indexes[1] and movie[0] != movie_indexes[2]:
            top_five_indexes.append(movie[0])
            count += 1
        else:
            continue

    # Get the top 5 movie indices
    # top_movie_indexes = [i[0] for i in sim_scores[:5]]

    recommended_movies = []

    # Get the name of the movies from their index
    for index in top_five_indexes:
        try:
            fetched_movie = MovieData.objects.get(index=index)
            recommended_movies.append(fetched_movie.title)
        except MovieData.DoesNotExist:
            fetched_movie = 'Could not find'
            recommended_movies.append(fetched_movie)


    context = {
        'result1': movie1,
        'result2': movie2,
        'result3': movie3,
        'rec1': recommended_movies[0],
        'rec2': recommended_movies[1],
        'rec3': recommended_movies[2],
        'rec4': recommended_movies[3],
        'rec5': recommended_movies[4]

    }

    return render(request, 'results.html', context)

@csrf_exempt
def search_movies(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        movies = MovieData.objects.filter(title__icontains=term)[:10]
        results = []
        for movie in movies:
            movie_dict = {'id': movie.index, 'value': movie.title}
            results.append(movie_dict)
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

