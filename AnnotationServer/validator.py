body_types = ["Audio", "Video", "Image", "TextualBody"]
body_formats = ["audio/mpeg", "video/mp4", "image/jpeg", "image/png", "text/plain"]

def validate_body(data):
    if "@context" not in data:
        return "No context in request body."
    elif data["@context"] != "http://www.w3.org/ns/anno.jsonld":
        return "Wrong context value. It must be \"http://www.w3.org/ns/anno.jsonld\""
    elif "body" not in data:
        return "Annotation body is missing."
    elif "target" not in data:
        return "Annotation target is missing."
    elif "value" not in data["body"]:
        return "Value of annotation body is missing."
    elif "format" not in data["body"]:
        return "Format of annotation body is missing."
    elif "type" not in data["body"]:
        return "Type of annotation body is missing."
    elif data["body"]["type"] not in body_types:
        return "Invalid body type. Valid body types are Audio, Video, Image and TextualBody."
    elif data["body"]["format"] not in body_formats:
        return "Invalid body format."
    elif not validate_type_format(data["body"]["type"], data["body"]["format"]):
        return "Body type and format do not match."
    return True

def validate_type_format(type, format):
    if type == "Audio" and format == "audio/mpeg":
        return True
    elif type == "Video" and format == "video/mp4":
        return True
    elif type == "Image" and format == "image/jpeg":
        return True
    elif type == "Image" and format == "image/png":
        return True
    elif type == "TextualBody" and format == "text/plain":
        return True
    return False

