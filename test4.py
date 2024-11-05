from PIL import Image

# Membaca gambar
images = [
    Image.open('static/images/img_0_0.png'),
    Image.open('static/images/img_0_1.png'),
    Image.open('static/images/img_0_2.png')
]

# Mengatur ukuran canvas berdasarkan gambar pertama
width, height = images[0].size
canvas = Image.new('RGBA', (width, height))

# Mengubah ukuran dan mode gambar lainnya agar sesuai dengan gambar pertama
for i in range(len(images)):
    images[i] = images[i].resize((width, height)).convert('RGBA')

# Menggabungkan gambar
for img in images:
    canvas = Image.alpha_composite(canvas, img)

# Menyimpan gambar hasil gabungan
canvas.save('gabungan.png')
