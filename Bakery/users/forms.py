from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,SelectField, ValidationError
from wtforms.validators import DataRequired,InputRequired
from Bakery.database import Bidhaa, Madeni , Uzalishaji

class ManunuziForm(FlaskForm):
    maligafi = StringField('Jina La Malighafi',validators=[DataRequired()])
    unit = StringField('Units (kg/ltr/dozen/)',validators=[DataRequired()])
    idadi = IntegerField('Idadi',validators=[InputRequired()])
    bei = IntegerField('Bei (Tsh)',validators=[InputRequired()])
    submit = SubmitField('Ingiza Taarifa')

class BidhaaForm(FlaskForm):
    bidhaa = StringField('Bidhaa',validators=[DataRequired()])
    bei = IntegerField('Bei (Tsh)',validators=[DataRequired()])
    submit = SubmitField('Ingiza Taarifa')

    def validate_bidhaa(self, bidhaa):
        bid = Bidhaa.query.filter_by(b_name=bidhaa.data).first()
        if bid:
            raise ValidationError("Bidhaa is Tayari Imesajiliwa Andika Bidhaa Nyingine")
        
class MadeniForm(FlaskForm):
    dt = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Now we are inside an app/request context!
        bids = Bidhaa.query.all()
        for bid in bids:
            self.dt.append(bid.b_name)
            

    name = StringField('Jina la Mteja',validators=[DataRequired()])
    phone = IntegerField('Namba za Simu',validators=[DataRequired()])
    bidhaa = SelectField('Bidhaa',choices=dt,validators=[DataRequired()])
    idadi = IntegerField('Idadi ya Bidhaa')
    kiasi_kalipa = IntegerField('Kiasi Kilicholipwa',validators=[InputRequired()])
    submit = SubmitField('Ingiza Taarifa')

    '''
    def validate_name(self, name):
        md = Madeni.query.filter_by(name=name.data).first()
        if md:
            raise ValidationError("Mteja Tayari Anapatikana Andika Jina Nyingine")
    
    '''
            
class MauzoForm(FlaskForm):
    dt = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Now we are inside an app/request context!
        bids = Bidhaa.query.all()
        for bid in bids:
            self.dt.append(bid.b_name)
            
    bid = SelectField('Bidhaa',choices = dt)
    b_uza = IntegerField('Idadi Iliyotoka',validators=[DataRequired()])
    submit = SubmitField('Ingiza Taarifa')
    

class UzalishajiForm(FlaskForm): 
    dt = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Now we are inside an app/request context!
        bids = Bidhaa.query.all()
        for bid in bids:
            self.dt.append(bid.b_name)
            
    bid = SelectField('Bidhaa',choices = dt)
    jumla = IntegerField('Bidhaa Nilizopokea(Kutoka Kwa Mpishi)',validators=[InputRequired()])
    submit = SubmitField('Ingiza Taarifa')
    
        
class MpishiForm(FlaskForm):
    dt = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Now we are inside an app/request context!
        bids = Bidhaa.query.all()
        for bid in bids:
            self.dt.append(bid.b_name)
            
    bid = SelectField('Bidhaa',choices = dt)
    pondo = IntegerField('Mzunguko (Pondo)',validators=[DataRequired()])
    idadi = IntegerField('Idadi Iliyotoka',validators=[DataRequired()])
    submit = SubmitField('Ingiza Taarifa')

class StoreForm(FlaskForm):
    maligafi = StringField('Jina La Malighafi',validators=[DataRequired()])
    unit = StringField('Units (kg/ltr/...)',validators=[DataRequired()])
    idadi = IntegerField('Idadi',validators=[DataRequired()])
    submit = SubmitField('Ingiza Taarifa')
     
class Mabadiliko_BeiForm(FlaskForm):
    
    bei = IntegerField('Bei (Tsh)',validators=[DataRequired()])
    submit = SubmitField('Ingiza Taarifa')

class LipaForm(FlaskForm):
    
    lipa = IntegerField('Bei (Tsh)',validators=[DataRequired()])
    submit = SubmitField('Ingiza Taarifa')

class MapatoForm(FlaskForm):
    pass

class MatumiziForm(FlaskForm):
    aina = StringField('Aina Ya Matumizi',validators=[DataRequired()])
    kiasi = IntegerField('Kiasi (Tsh)',validators=[DataRequired()])
    submit = SubmitField('Ingiza Taarifa')