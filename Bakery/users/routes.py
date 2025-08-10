from flask import Blueprint, render_template, request,url_for,flash,redirect,session, make_response
from .forms import (ManunuziForm,BidhaaForm,MauzoForm,Mabadiliko_BeiForm,LipaForm,MapatoForm,MatumiziForm,
                    UzalishajiForm,MadeniForm,MpishiForm,StoreForm)
from Bakery.database import ManunuziData,Bidhaa,Uzalishaji,Mauzo,Madeni,Mpishi,Store,Mapato,Matumizi,User
from Bakery.factory import db
from flask_login import current_user, login_required
from datetime import datetime, date, timedelta
from Bakery.authorization.validate import manunuzi_required, mauzo_required, mpishi_required, admin_required, store_required

users = Blueprint('users', __name__)

@users.route('/manunuzi',methods=['GET','POST'])
@login_required
@manunuzi_required
def manunuzi():
    form = ManunuziForm()
    
    if form.validate_on_submit():
        mf = form.maligafi.data
        un = form.unit.data
        idadi = form.idadi.data
        jumla = idadi * form.bei.data
        manunuziData = ManunuziData(maligafi=mf,unit=un,idadi=idadi,bei=jumla,user_id=session['user_id'])
        matumizi = Matumizi(kiasi=jumla,aina="Manunuzi")
        db.session.add(matumizi)
        db.session.add(manunuziData)
        db.session.commit()
        
        return redirect(url_for('users.manunuzi'))
    else:

        manunuzidisp = ManunuziData.query.all()
        return render_template('manunuzi.html',manunuzidisp=manunuzidisp,form=form)
    
    


@users.route('/mauzo',methods=['GET','POST'])
@login_required
@mauzo_required
def mauzo():
    form = MauzoForm()
    
    if form.validate_on_submit():
        #mz means mauzo variable
        #create bei and foreign key from bidhaa
        bid_data = Bidhaa.query.filter_by(b_name=form.bid.data).first()
        mzs = Mauzo.query.filter_by(bid_id=bid_data.id).first()
        if mzs:
          baki = mzs.jumla - form.b_uza.data
          if baki >= 0:      
                bei = bid_data.b_bei * form.b_uza.data
                mzs.b_uza = form.b_uza.data
                mzs.b_bei_uza = bei 
                mzs.jumla = baki
                mapato = Mapato(kiasi=bei,aina="Mauzo")
                db.session.add(mapato)
                db.session.commit()
                return redirect(url_for('users.mauzo'))
          else:
                return f"Idadi iliyotoka {form.b_uza.data} ni kubwa kuliko kiasi kilichopo, Angalia kwa makini au wasiliana na Wahusika wa Uzalishaji"
        else:
            return f"Bidhaa hiyo bado haijaingia wasiliana na Wahusika wa Uzalishaji"
    else:
        #mzdisp for mauzo Query data
        mzdisp = Mauzo.query.order_by(Mauzo.id.desc()).all()
        return render_template('mauzo.html',form=form,title="Mauzo",mzdisp=mzdisp)

@users.route('/uzalishaji',methods=['GET','POST'])
@login_required
@mauzo_required
def uzalishaji():
    form = UzalishajiForm()
    if form.validate_on_submit():
        #uzal for uzalishaji variable and bid_data explained in mauzo route
        bid_data = Bidhaa.query.filter_by(b_name=form.bid.data).first()
        
        uzal = Uzalishaji(b_jumla = form.jumla.data, bid_id = bid_data.id)
        db.session.add(uzal)
        #db.session.commit()
        #update mauzo table with the new data
        mz = Mauzo.query.filter_by(bid_id=bid_data.id).first()
        if mz:
            mz.jumla = mz.jumla + form.jumla.data
            
        else:
            mauzo = Mauzo(jumla=form.jumla.data,bid_id=bid_data.id,user_id=session['user_id'])
            db.session.add(mauzo)
        db.session.commit()
        #flash message
        flash('Data is Sent Successfully','primary')
        return redirect(url_for('users.uzalishaji'))
    else:
        #uzaldisp for displaying in uzalishaji.html
        uzaldisp = Uzalishaji.query.all()
        return render_template('uzalishaji.html',form=form,uzaldisp=uzaldisp)
        
@users.route('/bidhaa',methods=['POST','GET'])
@login_required
@mauzo_required
def bidhaa():

    form = BidhaaForm()
    if form.validate_on_submit():
        bid = Bidhaa(b_name=form.bidhaa.data,b_bei=form.bei.data)
        db.session.add(bid)
        db.session.commit()
        flash('New Entry Added','info')
        return redirect(url_for('users.bidhaa'))
    else:
        bid = Bidhaa.query.all()
        return render_template('bidhaa.html', form=form,bid=bid)
    
@users.route('/madeni',methods=['GET','POST'])
@login_required
@mauzo_required
def madeni():
    form = MadeniForm()
    collapse = False
    if form.validate_on_submit():
        # Get the selected product from the dropdown
        bid_data = Bidhaa.query.filter_by(b_name=form.bidhaa.data).first()
        baki = (bid_data.b_bei * form.idadi.data) - form.kiasi_kalipa.data

        #update number of product in Mauzo Table
        mz = Mauzo.query.filter_by(bid_id=bid_data.id).first()
        if mz:
            baki = mz.jumla - form.idadi.data
            if baki >= 0: 
                k_baki = (bid_data.b_bei * form.idadi.data) - form.kiasi_kalipa.data
                mz.jumla = baki
                md = Madeni(name=form.name.data, phone=form.phone.data, kiasi_kalipa=form.kiasi_kalipa.data, kiasi_baki=k_baki,status=form.idadi.data, bid_id=bid_data.id)
                mapato = Mapato(kiasi=form.kiasi_kalipa.data,aina="From Madeni")
                db.session.add(mapato)
                db.session.add(md)
                db.session.commit()
                collapse = False
                flash('New Entry Added','info')
                return redirect(url_for('users.madeni'))
            else:
                return f"Idadi iliyotoka {form.idadi.data} ni kubwa kuliko kiasi kilichopo, Angalia kwa makini au wasiliana na Wahusika wa Uzalishaji"
        else:
            return f"Bidhaa hiyo bado haijaingia wasiliana na Wahusika wa Uzalishaji"
    else:
        collapse = False
        md = Madeni.query.order_by(Madeni.id.desc()).all()
        return render_template('madeni.html', form=form, md=md, collapse=collapse)


@users.route('/mpishi',methods=['GET','POST'])
@login_required
@mpishi_required
def mpishi():
    form = MpishiForm()
    if form.validate_on_submit():
        #loading bidhaa data
        bid_data = Bidhaa.query.filter_by(b_name=form.bid.data).first()
        
        #inserting data to the database
        mpishi = Mpishi(pondo=form.pondo.data, idadi=form.idadi.data,bid_id=bid_data.id,user_id=session['user_id'])
        db.session.add(mpishi)
        db.session.commit()

        return redirect(url_for('users.mpishi'))
    else:

        #display on the screen 
        mpdsp = Mpishi.query.all()
        return render_template('mpishi.html', form=form, mpdsp=mpdsp)


@users.route('/store',methods=['GET','POST'])
@login_required
@store_required
def store():
    form = StoreForm()
    if form.validate_on_submit():

        #inserting data to the database
        store = Store(maligafi=form.maligafi.data, units=form.unit.data,idadi=form.idadi.data,user_id=session['user_id'])
        db.session.add(store)
        db.session.commit()
        return redirect(url_for('users.store'))
    else:
        
        #display on the screen 
        strdsp = Store.query.all()
        response = make_response(render_template('store.html', form=form, strdsp=strdsp))
        # prevent browser from caching
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

@users.route('/B_bei/<int:id>',methods=['GET','POST'])
@login_required
def mabaliko_Bei(id):
    bid_data = Bidhaa.query.get_or_404(id)
    form = Mabadiliko_BeiForm()
    if form.validate_on_submit():
        bid_data.b_bei = form.bei.data
        db.session.commit()
        flash('Bei updated','info')
        return redirect(url_for('users.bidhaa'))
    else:
        return render_template('bei.html',form=form)
        

@users.route('/lipa/<int:id>',methods=['GET','POST'])
@login_required
def lipa(id):
    deni = Madeni.query.get_or_404(id)
    form = LipaForm()
    if form.validate_on_submit():
        deni.kiasi_kalipa = form.lipa.data + deni.kiasi_kalipa
        deni.kiasi_baki = (deni.bid.b_bei * deni.status) - deni.kiasi_kalipa
        mapato = Mapato(kiasi=form.lipa.data,aina="Lipa Deni")
        db.session.add(mapato)
        db.session.commit()
        flash('Deni updated','info')
        return redirect(url_for('users.madeni'))
    else:
        return render_template('lipa.html',form=form)
    
# These are boss (Admin) routes all

@users.route('/boss',methods=['GET','POST'])
@login_required
@admin_required
def boss():

    #get Mapato and Matumizi data all 
    mapato = Mapato.query.order_by(Mapato.date.desc()).all()
    matumizi = Matumizi.query.order_by(Matumizi.date.desc()).all()

    # Get 7 days before today + today
    today = date.today()
    
    date_range = [(today - timedelta(days=i)) for i in range(7)]
    date_range.remove(today)

    return render_template('boss.html',mapato=mapato,matumizi=matumizi,date_range=date_range,tarehe=today)
    
@users.route('/b_bidhaa', methods=['GET', 'POST'])
@login_required
@admin_required
def b_bidhaa():
    bid = Bidhaa.query.all()
    return render_template('b_bidhaa.html',bid=bid)

@users.route('/b_store', methods=['GET', 'POST'])
@login_required
@admin_required
def b_store():
    strdsp = Store.query.all()
    return render_template('b_store.html',strdsp=strdsp)

@users.route('/b_manunuzi', methods=['GET', 'POST'])
@login_required
@admin_required
def b_manunuzi():
    manunuzidisp = ManunuziData.query.all()
    return render_template('b_manunuzi.html',manunuzidisp=manunuzidisp)

@users.route('/deactivate_account/<int:id>', methods=['GET', 'POST'])
@login_required
def deactivate_account(id):
    #current_user.is_active = False
    user = User.query.get_or_404(id)
    user.is_active = False
    db.session.commit()
    return redirect(url_for('users.user_status'))

@users.route('/activate_account/<int:id>', methods=['GET', 'POST'])
@login_required
def activate_account(id):
    #current_user.is_active = False
    user = User.query.get_or_404(id)
    user.is_active = True
    db.session.commit()
    return redirect(url_for('users.user_status'))

@users.route('/delete_account/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_account(id):
    #current_user.is_active = False
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.user_status'))

@users.route('/b_uzalishaji', methods=['GET', 'POST'])
@login_required
@admin_required
def b_uzalishaji():
    #display on the screen 
    mpdsp = Mpishi.query.all()
    return render_template('b_uzalishaji.html', mpdsp=mpdsp)

@users.route('/b_mauzo', methods=['GET', 'POST'])
@login_required
@admin_required
def b_mauzo():
    #mzdisp for mauzo Query data
    mzdisp = Mauzo.query.order_by(Mauzo.id.desc()).all()
    return render_template('b_mauzo.html',mzdisp=mzdisp)

@users.route('/b_madeni', methods=['GET', 'POST'])
@login_required
@admin_required
def b_madeni():
    md = Madeni.query.order_by(Madeni.id.desc()).all()
    return render_template('b_madeni.html', md=md)


@users.route('/user_status', methods=['GET', 'POST'])
@login_required
@admin_required
def user_status():
    users = User.query.all()
    return render_template('user_status.html',users=users)

@users.route('/matumizi', methods=['GET', 'POST'])
@login_required
@mauzo_required
def matumizi():
    form = MatumiziForm()
    if form.validate_on_submit():
        data = Matumizi(kiasi=form.kiasi.data, aina=form.aina.data)
        db.session.add(data)
        db.session.commit()
        flash('Matumizi yamehifadhiwa','info')
        return redirect(url_for('users.mauzo'))
    return render_template('matumizi.html', form=form)

@users.route('/mapato_matumizi/<tarehe>', methods=['GET', 'POST'])
@login_required
def mapato_matumizi(tarehe):
    #get Mapato and Matumizi data all 
    mapato = Mapato.query.order_by(Mapato.date.desc()).all()
    matumizi = Matumizi.query.order_by(Matumizi.date.desc()).all()
    total = 0

    return render_template('mapato_matumizi.html',mapato=mapato,matumizi=matumizi,tarehe=tarehe,total=total)