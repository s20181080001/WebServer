import os

from flask import Flask, request, render_template
from wtforms import Form, TextAreaField, validators

import extractFeatures

project_root = os.path.dirname(os.path.realpath('__file__'))
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')
app = Flask(__name__, template_folder=template_path, static_folder=static_path)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/cite')
def cite():
    return render_template('cite.html', title='Citation')


@app.route('/supl')
def supl():
    return render_template('supl.html', title='Supplementary Data')


@app.route('/about')
def about():
    return render_template('about.html', title='About us')


@app.route('/sample')
def sample():
    return render_template('sample.html', title="sample")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


class PredForm(Form):
    sequence = TextAreaField(u'Protein Sequence &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp(Enter A Fasta \
        Format Sequence or Just Sequence Text)', [validators.DataRequired()])


def SimpleFastaParser(fasta_sequence):
    seq = fasta_sequence.split('\n')
    seq = seq[1:]
    re = ''
    for x in seq:
        re = re + x[:len(x)]
    return re


def SimpleParser(sequence):
    seq = sequence.split('\n')
    re = ''
    for x in seq:
        re = re + x[:len(x)]
    return re


@app.route("/pred", methods=['GET', 'POST'])
def pred():
    form = PredForm(request.form)
    if request.method == 'POST':
        input_seq = request.form['sequence']
        if '>' in input_seq:
            sequence = SimpleFastaParser(input_seq)
        else:
            sequence = SimpleParser(input_seq)
        result = extractFeatures.feature_result(sequence)
        return resultPage(result)

    return render_template('pred.html', form=form, title="Prediction")


def resultPage(result):
    return render_template('result.html', results=result, title="Results")


if __name__ == "__main__":
    # app.debug = True
    app.run()
