import traceback

from flask import abort, Flask, request, jsonify

from wikithingsdb import query, util

app = Flask(__name__)


@app.route("/types", methods=['GET', 'POST'])
def get_types():
    article = request.values.get('article', '').decode('utf-8')
    methods = request.values.getlist('methods')

    if not article:
        abort(400)

    response = {}
    for function in methods:
        try:
            # calls query.function(article)
            returned = getattr(query, function)(article)
            response[function] = postprocess(returned, function)
        except:
            traceback.print_exc()

    return jsonify(**response)


def postprocess(result, function):
    """
    Clean up types for caller
    """
    if function == 'classes_of_article':
        result = [util.from_wikipedia_class(c) for c in result]
    elif function == 'hypernyms_of_article':
        # flatten DBpedia hypernyms to a set
        types = []
        for dbpedia_classes in result.values():
            types += dbpedia_classes
        result = set(types)
        if 'thing' in result:
            # every entity has type owl:Thing
            # remove it form the output because it is not informative
            result.remove('thing')

    # replace dashes with spaces
    return [s.replace('-', ' ').lower().strip() for s in result]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8056)
