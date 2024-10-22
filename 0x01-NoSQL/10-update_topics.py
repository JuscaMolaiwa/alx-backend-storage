#!/usr/bin/env python3
"""
    Updates the list of topics of a school document based on the school name.
"""


def update_topics(mongo_collection, name, topics):
    '''Changes all topics of a collection's document based on the name.'''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
