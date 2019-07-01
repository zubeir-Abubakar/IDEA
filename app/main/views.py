from flask import render_template,request,redirect,url_for, abort
from . import main
from ..models import User, Pitch, Category, Vote, Comment
from flask_login import login_required, current_user
from .forms import UpdateProfile, PitchForm, CommentForm, CategoryForm
from .. import db, photos

#Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

   
    category = Category.get_categories()


    return render_template('index.html',  category = category)

@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    '''
    View new group route function that returns a page with a form to create a category
    '''
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    
    title = 'New category'
    return render_template('new_category.html', category_form = form,title=title)

@main.route('/categories/<int:id>')
def category(id):
    category_ = Category.query.get(id)
    pitches = Pitch.query.filter_by(category=category_.id).all()

    # pitches=Pitch.get_pitches(id)
    # title = f'{category.name} page'
    return render_template('category.html', pitches=pitches, category=category_)

#Route for adding a new pitch
@main.route('/categories/view_pitch/add/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    '''
    Function to check Pitches form and fetch data from the fields
    '''                                             
    form = PitchForm()
    category = Category.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_pitch= Pitch(content=content,category= category.id,user_id=current_user.id)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))


    title = 'New Pitch'
    return render_template('new_pitch.html', title = title, pitch_form = form, category = category)

#viewing a Pitch with its comments
@main.route('/categories/view_pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    '''
    Function the returns a single pitch for comment to be added
    '''

    print(id)
    pitches = Pitch.query.get(id)
    # pitches = P 2itch.query.filter_by(id=id).all()

    if pitches is None:
        abort(404)
    #
    comment = Comments.get_comments(id)
    return render_template('pitch.html', pitches=pitches, comment=comment, category_id=id)

# @main.route('/user/<uname>')
# def profile(uname)

@main.route('/user/<uname>/update/pic', methods = ['POST'])
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos'
        user.profile_pic_path = path
        db.session.commit()

    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname = user.username))

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

    return render_template("profile/profile.html", user = user)