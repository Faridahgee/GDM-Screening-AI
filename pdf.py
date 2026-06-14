import qrcode

# Your GitHub URL
url = "https://github.com/Faridahgee/GDM-Screening-AI"

# Generate QR code
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)
qr.add_data(url)
qr.make(fit=True)

# Create image
img = qr.make_image(fill_color="black", back_color="white")
img.save("github_qr_code.png")

print("✅ QR code saved as github_qr_code.png")