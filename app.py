from flask import Flask, render_template, request, jsonify
from flask_api import status
import configparser
import psycopg2

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('padron.ini')
cnx = psycopg2.connect(dbname=config['DB']['name'], user=config['DB']['user'], password=config['DB']['password'],
                       host=config['DB']['host'], port=config['DB']['port'])
cur = cnx.cursor()


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/api/v1/provincias', methods=['POST', 'GET', 'DELETE', 'PUT'])
def provincias():
    if request.method == 'GET':
        cur.execute("SELECT * FROM provincia;")
        dataJson = []
        for provincia in cur.fetchall():
            dataDict = {
                'codigo': provincia[0],
                'nombre': provincia[1]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para provincias'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/provincia/<string:codigo>', methods=['POST', 'GET', 'DELETE', 'PUT'])
def provincia(codigo):
    if request.method == 'GET':
        cur.execute("SELECT * FROM provincia WHERE codigo=%s;", (codigo,))
        provincia = cur.fetchone()
        if provincia is None:
            content = {'Error de codigo': 'La provincia con el codigo {} no existe.'.format(codigo)}
            return content, status.HTTP_404_NOT_FOUND
        else:
            dataDict = {
                'codigo': provincia[0],
                'nombre': provincia[1]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para provincia'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED

@app.route('/api/v1/provincia/<string:codigo>/cantones', methods=['POST', 'GET', 'DELETE', 'PUT'])
def provinciaCantones(codigo):
    if request.method == 'GET':
        cur.execute("SELECT * FROM canton WHERE provincia=%s;", (codigo,))
        dataJson = []
        for canton in cur.fetchall():
            dataDict = {
                'provincia': canton[0],
                'codigo': canton[1],
                'nombre': canton[2]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para Cantones de Provincia'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/cantones', methods=['POST', 'GET', 'DELETE', 'PUT'])
def cantones():
    if request.method == 'GET':
        cur.execute("SELECT * FROM canton;")
        dataJson = []
        for canton in cur.fetchall():
            dataDict = {
                'provincia': canton[0],
                'codigo': canton[1],
                'nombre': canton[2]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para cantones'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/provincia/<string:codigoProvincia>/canton/<string:codigoCanton>', methods=['POST', 'GET', 'DELETE', 'PUT'])
def canton(codigoProvincia, codigoCanton):
    if request.method == 'GET':
        cur.execute("SELECT * FROM canton WHERE provincia=%s AND codigo=%s;", (codigoProvincia, codigoCanton))
        canton = cur.fetchone()
        if canton is None:
            content = {'Error de codigo': 'El canton con el codigo {} no existe.'.format(codigoCanton)}
            return content, status.HTTP_404_NOT_FOUND
        else:
            dataDict = {
                'provincia': canton[0],
                'codigo': canton[1],
                'nombre': canton[2]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para canton'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/provincia/<string:codigoProvincia>/canton/<string:codigoCanton>/distritos', methods=['POST', 'GET', 'DELETE', 'PUT'])
def cantonDistrito(codigoProvincia, codigoCanton):
    if request.method == 'GET':
        cur.execute("SELECT * FROM distrito WHERE provincia=%s AND canton=%s;", (codigoProvincia, codigoCanton))
        dataJson = []
        for distrito in cur.fetchall():
            dataDict = {
                'provincia': distrito[0],
                'canton': distrito[1],
                'codigo': distrito[2],
                'nombre': distrito[3]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para Distrito de Canton'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/distritos', methods=['POST', 'GET', 'DELETE', 'PUT'])
def distritos():
    if request.method == 'GET':
        cur.execute("SELECT * FROM distrito;")
        dataJson = []
        for distrito in cur.fetchall():
            dataDict = {
                'provincia': distrito[0],
                'canton': distrito[1],
                'codigo': distrito[2],
                'nombre': distrito[3]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para distritos'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


@app.route('/api/v1/provincia/<string:codigoProvincia>/canton/<string:codigoCanton>/distrito/<string:codigoDistrito>', methods=['POST', 'GET', 'DELETE', 'PUT'])
def distrito(codigoProvincia, codigoCanton, codigoDistrito):
    if request.method == 'GET':
        cur.execute("SELECT * FROM distrito where provincia = %s And canton = %s And codigo = %s;", (codigoProvincia,codigoCanton,codigoDistrito))

        distrito = cur.fetchone()
        if distrito is None:
            content = {'Error de codigo': 'El distrito con el codigo {} no existe.'.format(codigoDistrito)}
            return content, status.HTTP_404_NOT_FOUND
        else:
            dataDict = {
                'provincia': distrito[0],
                'canton': distrito[1],
                'codigo': distrito[2],
                'nombre': distrito[3]
            }
            return jsonify(dataDict), status.HTTP_200_OK
    else:
        content = {'Error de metodo': 'Solo se soporta GET para distrito'}
        return content, status.HTTP_405_METHOD_NOT_ALLOWED


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port="5000")
