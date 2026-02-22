from flask import Flask, render_template, request, redirect, url_for, flash
from data_context import SimpleDataContext
from repositories import AutosportUnitOfWork
from entities import Track

app = Flask(__name__)
app.secret_key = 'autosport_secret_key'  # Необхідно для роботи сповіщень flash

# Ініціалізація бази даних та Unit of Work
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


# Список трас (Index)
@app.route('/tracks')
def objects_info():
    tracks = uow.tracks.get_all()
    return render_template('objects_info.html', objects=tracks)


# Додавання нової траси (Create)
@app.route('/tracks/create', methods=['GET', 'POST'])
def create_track():
    if request.method == 'POST':
        name = request.form.get('name')
        country = request.form.get('country')
        try:
            length = float(request.form.get('length', 0))
        except ValueError:
            length = 0

        # Валідація (Лабораторна №9)
        if not name or len(name) < 3:
            flash("Назва траси повинна містити мінімум 3 символи", "danger")
            return render_template('tracks_form.html', action="Додати")

        new_track = Track(name, length, country)
        uow.tracks.add(new_track)
        uow.save()

        flash(f"Трасу '{name}' успішно додано!", "success")
        return redirect(url_for('objects_info'))

    return render_template('tracks_form.html', action="Додати")


# Редагування траси (Edit)
@app.route('/tracks/edit/<int:id>', methods=['GET', 'POST'])
def edit_track(id):
    track = uow.tracks.get_by_id(id)
    if not track:
        flash("Трасу не знайдено", "danger")
        return redirect(url_for('objects_info'))

    if request.method == 'POST':
        track.name = request.form.get('name')
        track.country = request.form.get('country')
        try:
            track.length = float(request.form.get('length'))
        except ValueError:
            pass

        uow.save()
        flash(f"Зміни для траси '{track.name}' збережено", "success")
        return redirect(url_for('objects_info'))

    return render_template('tracks_form.html', track=track, action="Редагувати")


# Видалення траси (Delete)
@app.route('/tracks/delete/<int:id>', methods=['POST'])
def delete_track(id):
    # Видалення об'єкта через фільтрацію списку в контексті
    context.tracks = [t for t in context.tracks if t.id != id]
    uow.save()
    flash("Трасу видалено", "warning")
    return redirect(url_for('objects_info'))


if __name__ == '__main__':
    app.run(debug=True)