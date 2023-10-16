from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

destbp = Blueprint('destination', __name__, url_prefix='/destinations')

@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    form = CommentForm()    
    return render_template('destinations/show.html', destination=destination, form=form)

@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():

    db_file_path = check_upload_file(form)
    destination = Destination(name=form.name.data,description=form.description.data, 
    image=db_file_path,currency=form.currency.data)

    db.session.add(destination)

    db.session.commit()
    flash('Successfully created new travel destination', 'success')

    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

def check_upload_file(form):
  fp = form.image.data
  filename = fp.filename
  BASE_PATH = os.path.dirname(__file__)
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  db_upload_path = '/static/image/' + secure_filename(filename)
  fp.save(upload_path)
  return db_upload_path

@destbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    if form.validate_on_submit():  
  
      comment = Comment(text=form.text.data, destination=destination,
                        user=current_user) 
      db.session.add(comment) 
      db.session.commit() 
      
      flash('Your comment has been added', 'success')  

    return redirect(url_for('destination.show', id=id))