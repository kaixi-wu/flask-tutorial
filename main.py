from exts import create_app, db
from flask_migrate import Migrate

if __name__ == '__main__':
    app = create_app()
    # migrate = Migrate(app, db)

    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            links.append((rule.endpoint, rule.rule))
        return str(links)

    app.run(debug=True, host="0.0.0.0", port=80)
