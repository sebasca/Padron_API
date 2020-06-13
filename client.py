import requests, json
from flask import Flask, render_template, request

inputValido = False
serverURL = "http://0.0.0.0:5000/api/v1/"

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and str(request.form['button']).upper() == 'CONSULTAR':
        tipoConsulta = int(request.form['dropdown_query'])
        nombreLugar = str(request.form['input_location']).upper().strip()
        firstLabel, secondLabel = "", ""

        if tipoConsulta == 1:
            firstLabel = "Estas son todas las provincias de Costa Rica: "
            secondLabel = consultarTodos("provincias")
            print(secondLabel)
        elif tipoConsulta == 2:
            firstLabel = "Estos son todos los cantones de Costa Rica: "
            secondLabel = consultarTodos("cantones")
        elif tipoConsulta == 3:
            firstLabel = "Estos son todos los distritos de Costa Rica: "
            secondLabel = consultarTodos("distritos")
        elif tipoConsulta == 4:
            firstLabel, secondLabel = consultarProvinciaUnica(nombreLugar)
        elif tipoConsulta == 5:
            firstLabel, secondLabel = consultarCantonUnico(nombreLugar)
        elif tipoConsulta == 6:
            firstLabel = consultarDistritoUnico(nombreLugar)
        return render_template('output.html', first_label=firstLabel, second_label=secondLabel)
    elif request.method == 'POST' and str(request.form['button']).upper() == 'REGRESAR':
        return render_template('client.html')
    else:
        return render_template('client.html')


def consultarTodos(tipoConsulta):
    requestURL = serverURL + tipoConsulta
    serverResponse = requests.get(requestURL)
    print("Status Code: " + str(serverResponse.status_code))
    result = ""

    if serverResponse.ok:
        data = json.loads(serverResponse.content)
        print("{0} ".format(len(data)) + tipoConsulta)
        for dict in data:
            for key in dict:
                if key == "nombre":
                    if tipoConsulta == "cantones" or tipoConsulta == "distritos":
                        if int(dict["provincia"]) < 8:
                            result += "\n" + str(dict[key]).title()
                    else:
                        if int(dict["codigo"]) < 8:
                            result += "\n" + str(dict[key]).title()
        print(result)
        return result
    else:
        serverResponse.raise_for_status()


def consultarNombre(tipoConsulta, codigoProvincia, codigoCanton):
    codigoProvincia = str(codigoProvincia)
    codigoCanton = str(codigoCanton)
    if tipoConsulta == "provincia":
        requestURL = serverURL + "provincia/" + codigoProvincia
    else:
        requestURL = serverURL + "provincia/" + codigoProvincia + "/canton/" + codigoCanton

    serverResponse = requests.get(requestURL)

    if serverResponse.ok:
        data = json.loads(serverResponse.content)
        return data["nombre"]
    else:
        serverResponse.raise_for_status()


def consultarPertenencias(tipoConsulta, codigoProvincia, codigoCanton):
    codigoProvincia = str(codigoProvincia)
    codigoCanton = str(codigoCanton)
    result = ""
    if tipoConsulta == "provincia":
        requestURL = serverURL + "provincia/" + codigoProvincia + "/cantones"
    else:
        requestURL = serverURL + "provincia/" + codigoProvincia + "/canton/" + codigoCanton + "/distritos"

    serverResponse = requests.get(requestURL)

    if serverResponse.ok:
        data = json.loads(serverResponse.content)
        for dict in data:
            for key in dict:
                if key == "nombre":
                    print(dict[key])
                    result += "\n" + str(dict[key]).title()
        return result
    else:
        serverResponse.raise_for_status()


def consultarProvinciaUnica(nombreProvincia):
    requestURL = serverURL + "provincias"
    serverResponse = requests.get(requestURL)
    codigoProvincia = ""
    print("Status Code: " + str(serverResponse.status_code))

    if serverResponse.ok:
        data = json.loads(serverResponse.content)
        for dict in data:
            for key in dict:
                if nombreProvincia.upper() == str(dict[key].strip().upper()):
                    codigoProvincia = str(dict["codigo"])
                    break

        if not codigoProvincia == "":
            output = "Estos son los cantonces que pertenecen a la provincia de " + nombreProvincia.title()
            output2 = consultarPertenencias("provincia", codigoProvincia, "")
            return output, output2
        else:
            return "La provincia ingresada no existe. Intente nuevamente.", ""
    else:
        serverResponse.raise_for_status()


def consultarCantonUnico(nombreCanton):
    requestURL = serverURL + "cantones"
    serverResponse = requests.get(requestURL)
    codigoCanton = ""
    print("Status Code: " + str(serverResponse.status_code))

    if serverResponse.ok:
        data = json.loads(serverResponse.content)
        for dict in data:
            for key in dict:
                if nombreCanton.upper() == str(dict[key].strip().upper()):
                    codigoCanton = str(dict["codigo"])
                    codigoProvincia = str(dict["provincia"])
                    break

        if not codigoCanton == "":
            nombreProvincia = consultarNombre("provincia", codigoProvincia, codigoCanton)
            output = "El canton de " + nombreCanton.title() + " pertenece a la provincia de " + nombreProvincia.title() + "\nEstos son los distritos que pertenecen al canton de " + nombreCanton.title()
            output2 = consultarPertenencias("canton", codigoProvincia, codigoCanton)
            return output, output2
        else:
            return "El canton ingresado no existe. Intente nuevamente.", ""
    else:
        serverResponse.raise_for_status()


def consultarDistritoUnico(nombreDistrito):
    requestURL = serverURL + "distritos"
    serverResponse = requests.get(requestURL)
    codigoDistrito = ""
    print("Status Code: " + str(serverResponse.status_code))

    if serverResponse.ok:
        data = json.loads(serverResponse.content)
        for dict in data:
            for key in dict:
                if nombreDistrito.upper() == str(dict[key].strip().upper()):
                    codigoDistrito = str(dict["codigo"])
                    codigoCanton = str(dict["canton"])
                    codigoProvincia = str(dict["provincia"])
                    break

        if not codigoDistrito == "":
            nombreProvincia = consultarNombre("provincia", codigoProvincia, codigoCanton)
            nombreCanton = consultarNombre("canton", codigoProvincia, codigoCanton)
            return "El distrito de " + nombreDistrito.title() + " pertence a la provincia de " + nombreProvincia.title() + " y al canton de " + nombreCanton.title()
        else:
            return "El distrito ingresado no existe. Intente nuevamente."
    else:
        serverResponse.raise_for_status()


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port="5001")
