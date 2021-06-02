from flask import Flask,request
from flask_restful import Api, Resource, reqparse
from models import db, PacienteModel
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
api = Api(app)
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()
 
 
class PacienteVieww(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('sus_num',
        type=float,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('tipo_sangue',
        type=str,
        required=True,
        help = "Can't leave blank"
    )'''
 
    def get(self):
        pacientes = PacienteModel.query.all()
        return {'Pacientes':list(x.json() for x in pacientes)}
 
    def post(self):
        data = request.get_json()
        #data = BooksView.parser.parse_args()
 
        novo_paciente = PacienteModel(data['name'],data['sus_num'],data['tipo_sangue'])
        db.session.add(novo_paciente)
        db.session.commit()
        return novo_paciente.json(),201
 
 
class PacienteView(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('sus_num',
        type=float,
        required=True,
        help = "Can't leave blank"
        )
    parser.add_argument('tipo_sangue',
        type=str,
        required=True,
        help = "Can't leave blank"
        )'''
 
    def get(self,name):
        paciente = PacienteModel.query.filter_by(name=name).first()
        if paciente:
            return paciente.json()
        return {'message':'paciente não encontrado'},404
 
    def put(self,name):
        data = request.get_json()
        #data = BookView.parser.parse_args()
 
        paciente = PacienteModel.query.filter_by(name=name).first()
 
        if paciente:
            paciente.sus_num = data["sus_num"]
            paciente.tipo_sangue = data["tipo_sangue"]
        else:
            paciente= PacienteModel(name=name,**data)
 
        db.session.add(paciente)
        db.session.commit()
 
        return paciente.json()
 
    def delete(self,name):
        paciente= PacienteModel.query.filter_by(name=name).first()
        if paciente:
            db.session.delete(paciente)
            db.session.commit()
            return {'mensagem':'Apagado'}
        else:
            return {'mensagem': 'paciente não encontrado'},404
 
api.add_resource(PacienteVieww, '/pacientes')
api.add_resource(PacienteView,'/paciente/<string:name>')
 
app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5000)
