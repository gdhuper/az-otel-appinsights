import logging
import azure.functions as func

def main(req: func.HttpRequest, que: func.Out[str]) -> func.HttpResponse:
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
        message = name + "-test"
        
        print("Adding message: " + message)
        que.set(message)

        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        # Peek at the first message
        return func.HttpResponse(
             "This HTTP triggered function executed successfully.",
             status_code=200
        )
