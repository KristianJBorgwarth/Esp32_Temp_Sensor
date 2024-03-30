def url_decode(url_string):
        if not url_string:
            return b''
        if isinstance(url_string, str):
            url_string = url_string.encode('utf-8')
        bits = url_string.split(b'%')
        if len(bits) == 1:
            return url_string
        res = [bits[0]]
        appnd = res.append
        hextobyte_cache = {}
        for item in bits[1:]:
            try:
                code = item[:2]
                char = hextobyte_cache.get(code)
                if char is None:
                    char = hextobyte_cache[code] = bytes([int(code, 16)])
                appnd(char)
                appnd(item[2:])
            except Exception as error:
                print(error)
                appnd(b'%')
                appnd(item)
        return b''.join(res)