import requests

class Bloomberg:
    con = pdblp.BCon(debug=True, port=8194, timeout=5000)
    con.start()

