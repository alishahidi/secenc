from modules import loading

def key_generator(contentLen):
    key = loading.generate(2, ['-', ':'], 3, 10, type_of_value = 'char', capital = 'mix', seed = contentLen).get_key()
    return key

def encrypt(key, source, encode=True):
    try:
        key = loading.hashlib.sha256(str(key).encode('utf-8')).digest()
        IV = loading.Random.new().read(loading.AES.block_size)
        encryptor = loading.AES.new(key, loading.AES.MODE_CBC, IV)
        padding = loading.AES.block_size - len(source) % loading.AES.block_size
        source = bytes(source.encode('utf-8')) + bytes([padding]) * padding
        data = IV + encryptor.encrypt(source)
        return loading.base64.b64encode(data).decode("latin-1") if encode else data
    except:
        return False

def decrypt(key, source, decode=True):
    try:
        if decode:
            source = loading.base64.b64decode(source.encode("latin-1"))
        key = loading.hashlib.sha256(str(key).encode('utf-8')).digest()
        IV = source[:loading.AES.block_size]
        decryptor = loading.AES.new(key, loading.AES.MODE_CBC, IV)
        data = decryptor.decrypt(source[loading.AES.block_size:])
        padding = data[-1]
        if data[-padding:] != bytes([padding]) * padding:
            raise ValueError("Invalid padding...")
        return data[:-padding]
    except:
        return False


def jwtEncode(payload, key):
    try:
        return loading.jwt.encode(payload, key, algorithm="HS256")
    except:
        return False

def jwtDecode(secretJwt, key):
    try:
        return loading.jwt.decode(secretJwt, key, algorithms=["HS256"])
    except:
        return False


def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, loading.np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, loading.np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def random_color():
    rgbl=[255,0,0]
    loading.random.shuffle(rgbl)
    return tuple(rgbl)

def star():
    return f"{loading.colored('[', 'red')}{loading.colored('*', 'green')}{loading.colored(']', 'red')}"

def content_to_image(secret_data):
    try:
        img = loading.Image.new('RGB', (1000, 1000))
        randomColor = random_color()
        img.putdata(randomColor)
        img.save('Temp/rand-image.png')
        image = loading.cv2.imread("Temp/rand-image.png")
        # maximum bytes to encode
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print(f"{star()} Maximum bytes to encode:", n_bytes)
        if len(secret_data) > n_bytes:
            raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
        secret_data += "====="
        data_index = 0
        # convert data to binary
        binary_secret_data = to_bin(secret_data)
        # size of data to hide
        data_len = len(binary_secret_data)
        for row in image:
            for pixel in row:
                # convert RGB values to binary format
                r, g, b = to_bin(pixel)
                # modify the least significant bit only if there is still data to store
                if data_index < data_len:
                    # least significant red pixel bit
                    pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # least significant green pixel bit
                    pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                    data_index += 1
                if data_index < data_len:
                    # least significant blue pixel bit
                    pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                    data_index += 1
                # if data is encoded, just break out of the loop
                if data_index >= data_len:
                    break
        return image
    except:
        return False

def image_to_content(image_name):
    try:
        image = loading.cv2.imread(image_name)
        binary_data = ""
        for row in image:
            for pixel in row:
                r, g, b = to_bin(pixel)
                binary_data += r[-1]
                binary_data += g[-1]
                binary_data += b[-1]
        # split by 8-bits
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
        # convert from bits to characters
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====":
                break
        return decoded_data[:-5]
    except:
        return False

    
def encrypt_message( exp, outname):
    with open("message.txt", "r") as messageFile:
        message = messageFile.read()
    print(f"{star()} Get message len")
    loading.time.sleep(.1)
    messageLen = len(message)
    print(f"{star()} Generate key")
    loading.time.sleep(.1)
    keyGenerate = key_generator(messageLen)
    print(f"{star()} Encode message")
    loading.time.sleep(.1)
    encodeMessage = encrypt(keyGenerate, message)
    if encodeMessage:
        expTime = loading.datetime.datetime.utcnow() + loading.datetime.timedelta(minutes = exp)
        payload = {
            "data": encodeMessage,
            "exp": expTime
        }
        print(f"{star()} Convert key to binry")
        loading.time.sleep(.1)
        keyBinry = ''.join(format(ord(x), 'b') for x in keyGenerate)
        print(f"{star()} Create jwt")
        loading.time.sleep(.1)
        jwt = jwtEncode(payload, keyBinry)
        if jwt:
            print(f"{star()} Message to image")
            loading.time.sleep(.1)
            encoded_image = content_to_image(secret_data=jwt)
            print(f"{star()} Write image")
            loading.time.sleep(.1)
            loading.cv2.imwrite(f"result/{outname}.png", encoded_image)
            print(f"\n\nSave Image: [result/{outname}.png]")
            print(f"\n\nSecret key:\n\n{keyGenerate}")
        else:
            print(loading.colored("System error", "red", attrs=["bold"]))
    else:
        print(loading.colored("System error", "red", attrs=["bold"]))

def decrypt_message(image, key):
    print(f"{star()} Get data from image")
    loading.time.sleep(.1)
    decoded_data = image_to_content(image)
    if decoded_data:
        print(f"{star()} Convert key to binry")
        loading.time.sleep(.1)
        keyJwt = ''.join(format(x, 'b') for x in bytearray(key, 'utf-8'))
        print(f"{star()} get payload from jwt")
        loading.time.sleep(.1)
        print(f"{star()} Check valid jwt")
        loading.time.sleep(.1)
        payload = jwtDecode(decoded_data, keyJwt)
        if payload:
            print(f"{star()} Decode payload")
            loading.time.sleep(.1)
            decode_message = decrypt(key, payload["data"])
            if decode_message:
                print(f"\nDecoded Data:\n\n{str(decode_message.decode('utf-8'))}")
                print(loading.colored("\n\n**************************************\n\n", "green", attrs=["bold"]))
                print(loading.colored("\n\n**************************************\n\n", "green", attrs=["bold"]))
            else:
                print(loading.colored("Key|System error", "red", attrs=["bold"]))
        else:
            print("Signature Faild|Expired")
            return False
    else:
        print(loading.colored("System error", "red", attrs=["bold"]))