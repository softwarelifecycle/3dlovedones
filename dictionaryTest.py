import CameraImage

image1 = CameraImage.ImageData("192.168.0.106",  "192.168.0.106-pic.jpg")
image2 = CameraImage.ImageData("192.168.0.107",  "192.168.0.107-pic.jpg")

print(image1.ipaddress)
print(image1)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    print(data)
    for i in range(num_rows):
        data[i] = [image1. ipaddress, image1]

    return data

table = make_table(10,2)

print(table)

