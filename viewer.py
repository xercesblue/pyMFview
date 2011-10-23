
import struct
from PIL import Image
import ImageEnhance

im = Image.new("RGB", (719,1440))
pixels = im.load()
ff = []
threshold = 1
target_epsi = 0.01
tmean_adjust = 0.009
ff_target = []
# Read Target Mean
with open("mean.dat", "rb") as t:
    byte = t.read(4)
    while byte != "":
        # Do stuff with byte.
	try:
            tb = t.read(4)
            if len(tb) == 0:
                print "end of target data"
                break
            ftar ,  = struct.unpack('<f', tb)
            ff_target.append(ftar)
	except EOFError:
            print "done reading target data"


#target mean
print "Read %s target values " % len(ff)
tmean = sum(ff_target)/len(ff_target)

print "target %s" % tmean
print "setting threshold to %s"%tmean
threshold =  tmean-tmean_adjust

# Read Results
with open("MF_gpu.dat", "rb") as f:
    byte = f.read(4)
    while byte != "":
        # Do stuff with byte.
	try:
            b = f.read(4)
            if len(b) == 0:
                print "end of data"
                break
            flo ,  = struct.unpack('<f', b)
            ff.append(flo)
	except EOFError:
            print "done reading results"
print "Read %s res values " % len(ff)
mean = sum(ff)/len(ff)
print "mean %s" % mean

print "mean -> threshold delta %s" % (mean-threshold)
for i in range(im.size[0]):    # for every pixel:
    for j in range(im.size[1]):
	fval = ff.pop()
	
	if fval > threshold:
            pixels[i,j] = 255, 255, 255
	elif abs(fval-tmean) > target_epsi:
            #		pixels[i,j] = 83, 128, 17
            pixels[i,j] = 200, 128, 17
	else:
            pixels[i,j] = 90, 90, 90


im.show()

im.save("img.png", format="PNG")	






