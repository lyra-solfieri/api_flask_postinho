from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class PacienteModel(db.Model):
    __tablename__ = 'pacientes'
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    sus_num = db.Column(db.Integer())
    tipo_sangue = db.Column(db.String(80))
 
    def __init__(self, name, sus_num, tipo_sangue):
        self.name = name
        self.sus_num = sus_num
        self.tipo_sangue = tipo_sangue
     
    def json(self):
        return {"name":self.name, "sus_num":self.sus_num, "tipo_sangue":self.tipo_sangue}