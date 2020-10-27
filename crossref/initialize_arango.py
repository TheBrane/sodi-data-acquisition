# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 17:55:52 2020

@author: rish-r
"""

from arango import ArangoClient, ArangoServerError, DocumentInsertError

db_name = 'SODI_TEST'
user = 'root'
password = 'Cro$$refkg'


def intialize_database(db_name, user, password):
    """
    Parameters
    ----------
    db_name : str
        Name of the ArangoDB instance.
    user : str
        Username.
    password : str
        Password.

    Returns
    -------
    None.
    """
    # Initialize the client for ArangoDB.
    client = ArangoClient(hosts='http://localhost:8529')

    # Connect to "_system" database as root user.
    sys_db = client.db('_system', username=user, password=password)

    # Create a new database named "test".
    sys_db.create_database(db_name)

    # Connect to "test" database as root user.
    db = client.db(db_name, username=user, password=password)

    # Create a new collection named "Person".
    Person = db.create_collection('Person')

    # Create a new collection named "Works".
    Works = db.create_collection('Works')

    # Add a hash index to the collection.
    Person.add_hash_index(fields=['URI'], unique=True)

    # Add a hash index to the collection.
    Works.add_hash_index(fields=['URI'], unique=True)

    # Add a hash index to the collection.
    Works.add_hash_index(fields=['DOI'], unique=True)

    # Create a new graph named "Publications".
    graph = db.create_graph('Publications')

    # Create vertex collections for the graph.
    Person = graph.create_vertex_collection('Person')

    # Create vertex collections for the graph.
    Works = graph.create_vertex_collection('Works')

    # Create an edge definition for works to works.
    References = graph.create_edge_definition(
        edge_collection='References',
        from_vertex_collections=['Works'],
        to_vertex_collections=['Works']
    )

    # Create an edge definition for works to person.
    Author = graph.create_edge_definition(
        edge_collection='Author',
        from_vertex_collections=['Works'],
        to_vertex_collections=['Person']
    )

    # Create an edge definition relation between persons.
    Collaborator = graph.create_edge_definition(
        edge_collection='Collaborator',
        from_vertex_collections=['Person'],
        to_vertex_collections=['Person']
    )


def intialize_client():
    """
    Returns
    -------
    database object
        db object for python-arango driver functions.
    """
    # Initialize the client for ArangoDB.
    client = ArangoClient(hosts='http://localhost:8529')
    # Connect to "test" database as root user.
    return client.db(db_name, user, password)
