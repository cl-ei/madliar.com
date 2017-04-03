"""
Entrance to run this script.

"""
from wsgiserver import management

if __name__ == "__main__":
    # management.execute_from_command_line()
    from wsgiserver.template import Template, Context

    template = Template('<html>{% if test %}<h1>{{ varvalue }}</h1>{% endif %}</html>')
    print template.__dict__
    # context = Context({'test': True, 'varvalue': 'Hello'})
    # print template.render(context)
