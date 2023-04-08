from flask import Blueprint

website = Blueprint('website', __name__)


@website.route('/', methods=['GET'])
def home():
    """ Returns the home page template """
    return 'Hello molecular world!'
