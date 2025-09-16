import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="cri_hack")
def cri_hack(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "~ Wishing you a great day ahead !!! ~ Divakar",
             status_code=200  
        )
    
@app.route(route="subscribe")
def subscribe(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    email = req.params.get('email')
    tags = req.params.get('tags') # this must be a comma-separated string of tags 
    if not email:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            email = req_body.get('email')

    if email:
        return func.HttpResponse(f"Subscription successful for {email}.")
    else:
        return func.HttpResponse(
            "Please provide a valid email address.",
            status_code=400
        )

        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "~ Wishing you a great day ahead !!! ~",
             status_code=200  
        )