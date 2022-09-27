def warning_message():
    """
    Returns a warning message if not the longitude & latitude has not been saved into the Maps table.
    Used for backend API and for user front end.
    For backend API reference both tuple indexes.
    For front end warning messages we only need to use the first tuple index : warning_message()[0]['Warning']

    warning_message( )[1] = {'status': 199}
    warning_message( )[1] = 200

    warning_message( )[0] = warning message 
    warning_message( )[1] = status code
    
    Returns a tuple of dictionaries with the warning message and status.
    """
    warning = {
        'Warning': 'Your address has been uploaded to Trust House, but the coordinates to your postcode could not be saved.'
    }
    status = {'status': 199}
    return warning, status


def error_message():
    """
    Returns an error message if unable to get the request.
    Used for backend API and for user front end messages.
    For backend API reference both tuple indexes.
    For front end error messages we only need to use the first tuple index : error_message()[0]['Error']

    error_message( )[2] = {'status': 400}
    error_message( )[2] = 400

    error_message( )[0] = error message 
    error_message( )[1] = no match found
    error_message( )[2] = status code
    error_message( )[3] = business error
    error_message( )[4] = incident error

    Returns a tuple of dictionaries with the error message and status.
    """
    error = {
        'Error': 'Could not make your request. Please check and try again.'
    }
    no_match = {'Error': 'No match found. Please check and try again.'}
    status = {'status': 400}
    business_error = {'Error': 'Your listing could not be uploaded. We could not locate the co-ordinates of the postcode given.'}
    incident_error = {'Error': 'Your incident could not be uploaded. We could not locat ethe co-ordinates of the postcode.'}
    return error, no_match, status, business_error, incident_error


def ok_message():
    """
    Returns a message to let the user the request went through.
    Used for backend API and front end messages.
    For backend API reference both tuple indexes.
    For front end OK messages we only need to use the first tuple index : ok_message()[0]['Success']

    ok_message( )[2] = {'status': 200}
    ok_message( )[2] = 200

    ok_message( )[0] = good address & map details
    ok_message( )[1] = good review
    ok_message( )[2] = match found
    ok_message( )[3] = status code
    ok_message( )[4] = good business upload

    returns a tuple of dictionaries with OK messages and the status.
    """
    good_address = {
        'Success': 'Your address has been uploaded to Trust House.'
    }
    good_review = {
        'Success': 'Your review has been successfully uploaded to Trust House.'
    }
    match_found = {'Success': 'A match was found!'}
    status = {'status': 201}
    good_buisness = {'Success': 'Your business has been successfully uploaded to Trust House.'}
    return good_address, good_review, match_found, status, good_buisness
