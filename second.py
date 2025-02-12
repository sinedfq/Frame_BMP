import random
import struct

def read_bmp(filename):
    with open(filename, 'rb') as f:
        # Чтение заголовка файла (14 байт)
        bmp_header = f.read(14)
        if bmp_header[:2] != b'BM':
            raise ValueError("Not a valid BMP file")

        # Чтение заголовка изображения (DIB header, 40 байт)
        dib_header = f.read(40)
        width = int.from_bytes(dib_header[4:8], byteorder='little')
        height = int.from_bytes(dib_header[8:12], byteorder='little')
        bits_per_pixel = int.from_bytes(dib_header[14:16], byteorder='little')

        # Чтение палитры (если есть)
        palette = bytearray()
        if bits_per_pixel == 8:
            palette = f.read(1024)  # 256 * 4 (RGBA)

        # Чтение данных пикселей, размер строки с выравниванием
        row_size = ((width * bits_per_pixel + 31) // 32) * 4
        pixel_data = []

        # Чтение строк изображения
        for _ in range(height):
            row = f.read(row_size)
            pixel_data.append(row)

    return width, height, bits_per_pixel, palette, pixel_data

def add_border(width, height, bits_per_pixel, palette, pixel_data, border_width=15):
    # Новые размеры изображения
    new_width = width + 2 * border_width
    new_height = height + 2 * border_width

    # Если изображение 8-битное, преобразуем его в 24-битное (TrueColor)
    if bits_per_pixel == 8:
        new_bits_per_pixel = 24
        new_pixel_data = []

        # Преобразование 8-битных данных в 24-битные
        for y in range(height):
            row = bytearray()
            for x in range(width):
                color_index = pixel_data[y][x]
                r, g, b = palette[color_index * 4:color_index * 4 + 3]
                row.extend([b, g, r])  # BMP хранит цвета в порядке BGR
            # Выравнивание строки
            padding = (4 - (new_width * 3) % 4) % 4
            row.extend([0] * padding)
            new_pixel_data.append(row)
    else:
        new_bits_per_pixel = bits_per_pixel
        new_pixel_data = pixel_data

    # Создание нового массива данных с рамкой
    bordered_data = []

    # Заполнение верхней рамки
    for _ in range(border_width):
        row = bytearray()
        for _ in range(new_width):
            row.extend([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        # Выравнивание строки
        padding = (4 - (new_width * 3) % 4) % 4
        row.extend([0] * padding)
        bordered_data.append(row)

    # Заполнение основной части изображения с боковыми рамками
    for y in range(height):
        row = bytearray()
        # Левая рамка
        for _ in range(border_width):
            row.extend([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        # Основное изображение
        if new_bits_per_pixel == 24:
            row.extend(new_pixel_data[y][:width * 3])
        # Правая рамка
        for _ in range(border_width):
            row.extend([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        # Выравнивание строки
        padding = (4 - (new_width * 3) % 4) % 4
        row.extend([0] * padding)
        bordered_data.append(row)

    # Заполнение нижней рамки
    for _ in range(border_width):
        row = bytearray()
        for _ in range(new_width):
            row.extend([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])
        # Выравнивание строки
        padding = (4 - (new_width * 3) % 4) % 4
        row.extend([0] * padding)
        bordered_data.append(row)

    return new_width, new_height, new_bits_per_pixel, bordered_data

def write_bmp(filename, width, height, bits_per_pixel, pixel_data):
    with open(filename, 'wb') as f:
        # Запись заголовка файла
        f.write(b'BM')
        row_size = ((width * bits_per_pixel + 31) // 32) * 4
        file_size = 14 + 40 + (0 if bits_per_pixel == 24 else 1024) + row_size * height
        f.write(file_size.to_bytes(4, byteorder='little'))
        f.write((0).to_bytes(2, byteorder='little'))
        f.write((0).to_bytes(2, byteorder='little'))
        f.write((14 + 40 + (0 if bits_per_pixel == 24 else 1024)).to_bytes(4, byteorder='little'))

        # Запись заголовка изображения
        f.write((40).to_bytes(4, byteorder='little'))  # DIB header size
        f.write(width.to_bytes(4, byteorder='little'))
        f.write(height.to_bytes(4, byteorder='little'))
        f.write((1).to_bytes(2, byteorder='little'))  # Planes
        f.write((bits_per_pixel).to_bytes(2, byteorder='little'))  # Bit depth
        f.write((0).to_bytes(4, byteorder='little'))  # Compression
        f.write((0).to_bytes(4, byteorder='little'))  # Image size
        f.write((0).to_bytes(4, byteorder='little'))  # Horizontal resolution
        f.write((0).to_bytes(4, byteorder='little'))  # Vertical resolution
        f.write((0).to_bytes(4, byteorder='little'))  # Colors in palette
        f.write((0).to_bytes(4, byteorder='little'))  # Important colors

        # Запись данных пикселей
        for row in pixel_data:
            f.write(row)

if __name__ == "__main__":
    input_bmp_file = "_сarib_TC.bmp"
    output_bmp_file = "carib_bordered.bmp"
    try:
        width, height, bits_per_pixel, palette, pixel_data = read_bmp(input_bmp_file)
        new_width, new_height, new_bits_per_pixel, bordered_data = add_border(width, height, bits_per_pixel, palette, pixel_data)
        write_bmp(output_bmp_file, new_width, new_height, new_bits_per_pixel, bordered_data)
        print("Border added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")