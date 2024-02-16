# flask basics 
## what is flask
et framework for web applicationer
## jinja
template der kombinere dom og data kilder for at skabe dynamiske sider
### route()
er en decorator der fortæller appen hvilken url at bruge. 
    - @app.route(rule, options)
    - rule: url
    - parametere der bliver givet til rule.
    f.eks. @app.route('/hello')
        def hello_world():
            retuen 'hello world!'
    - med data 
        @app.route('/hello/)
### hoved elementer i flask web apps
    - static: data, css 
    - templates: html
    - app: instantiation
    - views: logik og referencer til url
    - webapp: kombinere app og views 
### run local
    - install flask 
    - use: flask --app app_name run
    - terminate: ctrl + æ
### azure
    - cloud in general
    - shared responsibility model
    - cloud models: public, private and hybrid
    - use cases for each model
    - consumption based mdel 
    - pricing models
# to be continued




