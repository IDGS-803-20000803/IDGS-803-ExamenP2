from flask import Blueprint, render_template, request, redirect,url_for,flash
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from . models import Camaras
import uuid
import os
from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/profile')
@login_required
def profile():
    camara = Camaras.query.all()
    return render_template('profile.html', name = current_user.name, camara = camara)

@main.route('/admin')
@login_required
@roles_required('admin')
def admin():
    camara = Camaras.query.all()
    print(camara)
    return render_template('admin.html', camara = camara)

@main.route('/insertCamara', methods = ['GET', 'POST'])
@login_required
@roles_required('admin')
def insert_camara():
  if request.method == 'POST':
    nombre = request.form.get('nombre') 
    resolucion = request.form.get('resolucion')
    alimentacion = request.form.get('alimentacion')
    precio = request.form.get('precio')
    existencia = request.form.get('existencia')

    img = str(uuid.uuid4()) + '.png'
    imagen = request.files['imagen']
    ruta_imagen = os.path.abspath('project\\static\\img')
    imagen.save(os.path.join(ruta_imagen, img))       
  
    camara = Camaras(nombre=nombre, resolucion=resolucion,alimentacion=alimentacion, precio=precio,existencia=existencia, imagen=img) 
   
    db.session.add(camara)
    db.session.commit()
    flash("Camara agregada satisfactoriamente")
    return redirect(url_for('main.admin'))
  return render_template('insert_camara.html')

@main.route('/updateCamara', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def update_camara():
    if request.method == 'GET':
        id = request.args.get('id')
        camara = db.session.query(Camaras).filter(Camaras.id == id).first()
        nombre = request.form.get('nombre', camara.nombre)
        resolucion = request.form.get('resolucion', camara.resolucion)
        alimentacion = request.form.get('alimentacion', camara.alimentacion)
        precio = request.form.get('precio', camara.precio)
        existencia = request.form.get('existencia', camara.existencia)
        imagen = request.form.get('imagen', camara.imagen)
        return render_template('update_camara.html', id = id, nombre = nombre, resolucion = resolucion, alimentacion = alimentacion, precio = precio, existencia = existencia, imagen=imagen)
    
    if request.method == 'POST':
        id = request.form.get('id')
        camara = db.session.query(Camaras).filter(Camaras.id == id).first()

        camara.nombre = request.form.get('nombre')
        camara.resolucion = request.form.get('resolucion')
        camara.alimentacion = request.form.get('alimentacion')
        camara.precio = request.form.get('precio')
        camara.existencia = request.form.get('existencia')
        imagen = request.files['imagen']
        ruta_imagen = os.path.abspath('project\\static\\img')        
        img = str(uuid.uuid4()) + '.png'
        imagen.save(os.path.join(ruta_imagen, img))   
        camara.imagen = img
        db.session.add(camara)
        db.session.commit()
        flash("Camara actualizada satisfactoriamente")
        return redirect(url_for('main.admin'))
    return render_template('update_camara.html')

@main.route('/deleteCamara', methods = ['GET'])
@login_required
@roles_required('admin')
def delete_camara():
   id = request.args.get('id')
   camara = db.session.query(Camaras).filter(Camaras.id == id).first()

   db.session.delete(camara)
   db.session.commit()
   flash("Camara eliminada satisfactoriamente")
   return redirect(url_for('main.admin'))