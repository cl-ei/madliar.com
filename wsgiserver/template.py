def get_template(template_name, using=None):
    """
    Loads and returns a template for the given name.

    Raises TemplateDoesNotExist if no such template exists.
    """
    return template_name


def render_to_string(template_name, context=None, request=None, using=None):
    """
    Loads a template and renders it with a context. Returns a string.

    """
    template = get_template(template_name, using=using)
    return template.render(context, request)
