"""
app.py

This module handles the creation of memes by
processing user input and generating images with quotes.
"""

import random
import os
import requests
from flask import Flask, render_template, request
from ingestor import Ingestor
from memegenerator import MemeGenerator


app = Flask(__name__)


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # Initialize an empty list to hold the quotes
    all_quotes = []

    # Loop through each file in the quote_files list
    for file in quote_files:
        try:
            # Use the Ingestor class to parse the file and get quotes
            parse_quotes = Ingestor.parse(file)
            all_quotes.extend(parse_quotes)
        except FileNotFoundError as error:
            print(f"An error occurred while processing {file}: {error}")

    print(all_quotes)

    images_path = "./_data/photos/dog/"

    # images within the images images_path directory
    image_files = []
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    for filename in os.listdir(images_path):
        file_path = os.path.join(images_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in allowed_extensions:
                image_files.append(file_path)
    print(image_files)
    return all_quotes, image_files


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # Select a random image
    random_image = random.choice(imgs)

    # Select a random quote
    random_quote = random.choice(quotes)
    text = random_quote.body  # The quote text
    author = random_quote.author  # The author of the quote

    # Now you can use random_image, text, and author in your meme generation
    print(f"Selected Image: {random_image}")
    print(f"Selected Quote: {text} - {author}")

    meme = MemeGenerator('./tmp')
    path = meme.make_meme(random_image, text, author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user-defined meme """

    # Get parameters from the form
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    # Define a temporary file path
    temp_image_path = './tmp/temp_image.jpg'

    # Step 1: Use requests to save the image from the image_url
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses
        with open(temp_image_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as error:
        print(f"Error downloading image: {error}")
        return render_template('meme.html', path=None)

    # Step 2: Use the meme object to generate a meme using this temp file
    meme_generator = MemeGenerator('./tmp')
    meme_path = meme_generator.make_meme(temp_image_path, body, author)

    # Step 3: Remove the temporary saved image
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

    return render_template('meme.html', path=meme_path)


if __name__ == "__main__":
    app.run(port=5003, debug=True)
