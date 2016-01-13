import logging
from logging.handlers import RotatingFileHandler
from flask import abort, Flask, request
import json
from wikithingsdb import fetch

app = Flask(__name__)


@app.route("/types", methods=['GET'])
def get_types():
    article = request.form.get('article', None)
    methods = request.form.get('methods', None)

    app.logger.debug("Recieved article [%s] and methods:", article)
    app.logger.debug(methods)
    
    # TODO: uncomment when MySQL migration is done
    response = {}
    # for function in methods:
    #     try:
    #         # calls fetch.function(article)
    #         returned = gettattr(fetch, function)(article)
    #     except KeyError:
    #         pass                # no such article in database
    #     except RuntimeError as e:
    #         # this should never happen, so log it
    #         app.logger.exception(e)
    #         app.logger.log("When error happened, called: {function}('{arg}')"\
    #                        .format(function=function, arg=article))
    #     else:
    #         response[function] = returned

    # for now, fake some data
    # if article == "Brooklyn Bridge":
    # if 'types_of_article' in methods:
    response['types_of_article'] = ['bridge',\
                                    'cable-stayed/suspension bridge',\
                                    'hybrid cable-stayed/suspension bridge']
    # if 'classes_of_article' in methods:
    response['classes_of_article'] = ['nrhp', 'bridge']
    # if 'hypernyms_of_article' in methods:
    response['hypernyms_of_article'] = ['bridge',\
                                        'route of transportation',\
                                        'infrastructure',\
                                        'architectural structure',\
                                        'place',\
                                        'thing',\
                                        'building',\
                                        'structure']
    # if 'redirects_of_article' in methods:
    # response['redirects_of_article'] = ['The Brooklyn Bridge',\
    #                                     'Brooklyn bridge',\
    #                                     'East River Bridge',\
    #                                     "I've got a bridge to sell you"]
    app.logger.debug("My response is:")
    app.logger.debug(response)
    
    return json.dumps(response)


if __name__ == "__main__":
    LOG_FILENAME = '/data/infolab/misc/elasticstart/log/wikithingsdb-server.log'
    formatter = logging.Formatter("[%(levelname)s %(name)s %(funcName)s:%(lineno)d]\t\t%(message)s")
    handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=5)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    logging.getLogger('wikithingsdb').addHandler(handler)
    app.run(host='0.0.0.0')
