from pathlib import Path
from flask import Flask,render_template,jsonify
from dotenv import load_dotenv
import os
load_dotenv()
def create_app():
    app=Flask(__name__)
    app.config['MAX_CONTENT_LENGTH']=int(os.getenv('MAX_CONTENT_LENGTH_MB','8'))*1024*1024
    for module in ('prediction','classification','chatbot','news'):
        imported=__import__('routes.'+module,fromlist=['bp']); app.register_blueprint(imported.bp)
    for route,template in [('/','index.html'),('/prediction','prediction.html'),('/scanner','scanner.html'),('/chatbot','chatbot.html'),('/about','about.html')]:
        app.add_url_rule(route,endpoint=template,view_func=lambda t=template:render_template(t))
    @app.errorhandler(413)
    def too_large(e): return jsonify(error='Upload exceeds server size limit'),413
    @app.get('/api/health')
    def health(): return jsonify(status='ok',classifier_ready=(Path(__file__).parent/'models'/'waste_classifier.keras').exists())
    return app
app=create_app()
if __name__=='__main__': app.run(debug=os.getenv('FLASK_DEBUG')=='1')
