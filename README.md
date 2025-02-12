<H2>Созхдание рамки для BMP изоражений</H2>

<h3>Задание: </h3>

Преобразовать BMP файл, создав вокруг него рамку из пикселей рандомных
цветов. Ширина рамки - 15 пикселей. Количество цветов – 256 и TrueColor.
Изменить соответствующие поля в заголовке и сохранить файл под новым
именем. Длина строки BMP файла выравнивается по 32-битовой границе,
(4-м байт), при необходимости к каждой строке в файле добавляются
выравнивающие байты!

-----

<h3>Основные участки кода: </h3>

Как и [Convert_BMP](https://github.com/sinedfq/Convert_BMP/tree/main), данный участок кода выполняет считывание BMP изображения

```python
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
```
----------

Основная функция создание рамки у BMP изображения ```add_border```

```python
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
```

Вначале исполнения метода мы узнаём новые размеры (```new_hight``` и ```new_width```) изображения <br>
Далее если изображение 8-битное, то мы преоразуем его в 24-битное для корректной работы  <br>
   • Для каждой строки (y) мы создаем новый bytearray для хранения преобразованных пикселей.  <br>
   • Для каждого пикселя (x) мы получаем индекс цвета из палитры и извлекаем соответствующие значения RGB.  <br>
   • Мы добавляем эти значения в строку в порядке BGR (так как формат BMP использует именно этот порядок).  <br>
   • Затем мы добавляем необходимое количество нулей для выравнивания строки до кратности 4 байтам и добавляем строку в новый массив пикселей.  <br>  <br>

Далее мы создаём саму нашу рамку:  <br>
1. Создаём массив ```border_data```, в котором у нас будут храниться данные  <br>
2. Далее в цикле мы заполняем данный массив случайными цветами и добавляем выравнивание   <br>
3. Далее мы заполняем основное изображние с боковыми рамками  <br>
4. И в конце заполняем нижнию рамку

-----

Оставшиеся функции ```write_bmp``` и ```main``` можно увидеть [тут](https://github.com/sinedfq/Convert_BMP/tree/main) 
 
-----

<H3>Результат работы:</H3>

![image](https://github.com/user-attachments/assets/c2b41379-31f6-44e7-800a-d417841091b0)
