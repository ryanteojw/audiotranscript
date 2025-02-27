from __init__ import app, db

# create tables 
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)