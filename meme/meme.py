"""
meme.py

This module generates memes by combining images with quotes.
"""
import os
import random
import argparse
from ingestor import Ingestor
from QuoteEngine.quote_model import QuoteModel
from memegenerator import MemeGenerator


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given a path and a quote.

    Args:
        path (str): Path to the image file.
        body (str): The quote text to display on the meme.
        author (str): The author of the quote.
    """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]
            print(dirs)
        img = random.choice(imgs)
    else:
        img = path
        print(img)

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for file in quote_files:
            quotes.extend(Ingestor.parse(file))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeGenerator('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    print(path)
    return path

def main():
    """Main function to parse command-line arguments and generate a meme."""

    # Create the parser
    parser = argparse.ArgumentParser(description='Generate a meme with quote.')

    # Add arguments
    parser.add_argument('--path', type=str, help='Path to an image file')
    parser.add_argument('--body', type=str, help='Quote body on the image')
    parser.add_argument('--author', type=str, help='Quote author on the image')

    # Parse the arguments
    parsed_args = parser.parse_args()

    # access the arguments using args.path, args.body, and args.author
    print(f'Image path: {parsed_args.path}')
    print(f'Quote body: {parsed_args.body}')
    print(f'Quote author: {parsed_args.author}')
    return parsed_args


if __name__ == '__main__':
    args = main()
    print(generate_meme(args.path, args.body, args.author))
