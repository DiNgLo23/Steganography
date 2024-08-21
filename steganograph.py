import cv2
import numpy as np



def to_bin(data):
    if isinstance(data, str):return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes):return ''.join([format(i, "08b") for i in data])
    elif isinstance(data, np.ndarray):return ''.join([format(i, "08b") for i in data])
    elif isinstance(data, int) or isinstance(data, np.uint8):return format(data, "08b")
    else:raise TypeError("Type not supported.")




def encode(image_name, secret_data):
    image = cv2.imread(image_name)

    n_bytes = image.size // 8
    print("[*] Maximum bytes to encode:", n_bytes)

    if len(secret_data) > n_bytes:raise ValueError("[!] Insufficient bytes, need bigger image or less data.")

    print("[*] Encoding data...")
    secret_data += "====="

    binary_secret_data = to_bin(secret_data)
    data_len = len(binary_secret_data)
    

    flat_image = image.flatten()
    for i in range(data_len):flat_image[i] = (flat_image[i] & 0xFE) | int(binary_secret_data[i])
    encoded_image = flat_image.reshape(image.shape)

    return encoded_image

def decode(image_name):
    print("[+] Decoding...")

    image = cv2.imread(image_name)

    flat_image = image.flatten()
    binary_data = ""

    for i in range(flat_image.size):binary_data += str(flat_image[i] & 1)

    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":break
    
    return decoded_data[:-5]

if __name__ == "__main__":
    input_image = "i.png"
    output_image = "encoded_image.png"
    secret_data = ""

    encoded_image = encode(image_name=input_image, secret_data=secret_data)

    cv2.imwrite(output_image, encoded_image)

    decoded_data = decode(output_image)
    print("[+] Decoded data:", decoded_data)
