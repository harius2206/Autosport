from flask import Flask, render_template
from data_context import SimpleDataContext
from repositories import AutosportUnitOfWork

app = Flask(__name__)

context = SimpleDataContext()
if context.is_empty():
    context.create_testing_data()

uow = AutosportUnitOfWork(context)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tracks')
def objects_info():
    tracks = uow.tracks.get_all()
    return render_template('objects_info.html', objects=tracks)

if __name__ == '__main__':
    app.run(debug=True)