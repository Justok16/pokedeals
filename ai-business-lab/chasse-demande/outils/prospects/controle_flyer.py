# Contrôle au pixel du flyer exporté (QR décodé et centré dans son cadre, pastille du haut). Lancer depuis supports/.
import cv2
import numpy as np
from PIL import Image

f = "flyer-dig-a5-v4.png"
im = cv2.imread(f)
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
v, pts, _ = cv2.QRCodeDetector().detectAndDecode(im)
pts = pts[0]
print("QR ->", v)
qx0, qx1 = pts[:, 0].min(), pts[:, 0].max()
qy0, qy1 = pts[:, 1].min(), pts[:, 1].max()
cy = int((qy0 + qy1) / 2)
cx = int((qx0 + qx1) / 2)
row = g[cy]
col = g[:, cx]
l = int(qx0)
while row[l - 1] > 200:
    l -= 1
r = int(qx1)
while row[r + 1] > 200:
    r += 1
t = int(qy0)
while col[t - 1] > 200:
    t -= 1
b = int(qy1)
while col[b + 1] > 200:
    b += 1
print("QR marges px: G", qx0 - l, "D", r - qx1, "H", qy0 - t, "B", b - qy1)
a = np.array(Image.open(f).convert("RGB")).astype(int)
x0, y0 = 1150, 40
rr = a[y0:230, x0:1720]
white = rr.min(2) > 200
ty, tx = np.where(white)
green = (rr[:, :, 1] > 150) & (rr[:, :, 0] < 120)
gy, gx = np.where(green)
print(
    "pastille: bord 53-505 / 51-135 ; texte",
    tx.min(),
    ty.min(),
    tx.max(),
    ty.max(),
    "point",
    gx.min(),
    gy.min(),
    gx.max(),
    gy.max(),
)
