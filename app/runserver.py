import sys
from tracingexample import app

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port=port, host="0.0.0.0")
