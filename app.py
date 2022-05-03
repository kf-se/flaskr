from flaskr import create_app
import os

if __name__ == "__main__":
    ON_HEROKU = os.environ.get('ON_HEROKU')

    if ON_HEROKU:
        port = int(os.environ.get('PORT', 5000))
    else:
        port = 5000

    app = create_app()
    app.run(host='0.0.0.0', port=port)
    