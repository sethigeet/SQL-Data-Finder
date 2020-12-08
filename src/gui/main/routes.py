from flask import render_template, Blueprint

main = Blueprint(name='main', import_name=__name__)


@main.route('/')
@main.route('/home')
def home():
    posts = []
    return render_template('home.html', posts=posts, active="home")


@main.route('/about')
def about():
    return render_template('about.html', title='About', active="about")
