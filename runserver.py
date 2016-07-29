from rescue_class import app


if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=5590)
