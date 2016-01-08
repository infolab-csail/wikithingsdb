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
    response['types_of_article'] = ['foo', 'bar', 'baz']
    response['classes_of_article'] = ['bar']
    response['hypernyms_of_article'] = ['bar', 'aba', 'zaba', 'boom', 'thing']
    response['redirects_of_article'] = ['first really really long thing like crazy long lets try to push the limit here', 'second', 'third', 'fourth']
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
