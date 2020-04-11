#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment"""

__author__ = "Janelle Kuhns worked alongside demo"

import cProfile
import pstats
import functools
import timeit


def profile(func):
    """A function that can be used as a decorator to measure performance"""
    # You need to understand how decorators are constructed and used.
    # Be sure to review the lesson material on decorators, they are used
    # extensively in Django and Flask.
    @functools.wraps(func)
    def inner(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        #original function
        result = func(*args, **kwargs)
        #disable profiler
        profiler.disable()
        ps = pstats.Stats(profiler).strip_dirs().sort_stats('cumulative')
        ps.print_stats(10)
        return result

    return inner


def read_movies(src):
    """Returns a list of movie titles"""
    print('Reading file: {}'.format(src))
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """returns True if title is within movies list"""
    return title in movies
    
#@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list"""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates

@profile
def find_duplicate_movies_improved(src):
    """Improved version of findin duplicate movies from src list"""
    #lowercase the movie titles
    movies = [movie.lower() for movie in read_movies(src)]
    #sort the movies list
    movies.sort()
    duplicates = [m1 for m1, m2 in zip(movies[1:], movies[:-1]) if m1 == m2]
    return duplicates

def timeit_helper():
    """Part A:  Obtain some profiling measurements using timeit"""
    # YOUR CODE GOES HERE
    t = timeit.Timer(stmt="find duplicate movies('movies.txt')", setup="from __main__ import find_duplicate_movies")
    number__repeats = 7
    runs_per_repeat = 3
    result = t.repeat(repeat=number__repeats, number=runs_per_repeat)
    best_time = min(result) / float(runs_per_repeat)
    print("Best time across {} repeats of {} runs per repeat: {} sec".format(number__repeats, runs_per_repeat, best_time))
    


def main():
    """Computes a list of duplicate movie entries"""

    # Part A:  timeit helper
    #timeit_helper()

    # Part B:  create a profiler which can be used to "decorate" any function
    #result = find_duplicate_movies('movies.txt')
    # Part C:  improved version
    result = find_duplicate_movies_improved('movies.txt')

    print('Found {} duplicate movies:'.format(len(result)))
    print('\n'.join(result))


if __name__ == '__main__':
    main()
