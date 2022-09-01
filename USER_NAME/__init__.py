import json
import logging
import jsonschema
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    STATUS_CODE = 200
    BODY_VALIDATION = {
        "title" : "Request",
        "type" : "object",
        "required" : ["email", "password"],
        "properties" : {
            "email" : {
                "type" : "string",
                "pattern" : "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
            },
            "password" : {
                "type" : "string"
            },
        }
    }
    try:
        req_body = req.get_json()
        jsonschema.validate(req_body, BODY_VALIDATION)
        response = req_body

    except jsonschema.exceptions.ValidationError as validation_error: 
        STATUS_CODE = 400
        response = {
            "error" : f"JSON inválido - {validation_error.message}"
        }
    except:
        STATUS_CODE: 503
        response = {'error' : 'Deu Erro'}

    finally:
        return func.HttpResponse(body=json.dumps(response), status_code=STATUS_CODE, mimetype='Aplication/json')
