from app import app

@app.route('/')
@app.route('/start')
def start():
    return 'placeholder for start function'