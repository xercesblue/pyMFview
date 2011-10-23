#Author: Francisco De La Cruz <dlcs.frank@gmail.com>
# Date: October 19, 2011

# libdect result viewer.
# This viewer has only been tested with the MF detector.
# Other detectors should work, mainly RX and RX adaptive
# 

import struct
from PIL import Image
import ImageEnhance
import sys
import getopt
# Parameters

def usage():
    print "libdect result viewer usage"
    print "-o <output file>"
    print "-i <input file>"
    print "-m <mean file>"
    print "-t <threshold>"
    print "-s <date dimensions> i.e. -s 200, 200"


def viewer(argv):
 
    try:
        optlist, args = getopt.getopt(argv, "t:m:i:o:s:",["threshold", "mean=","input=","output=","size="])
        if not optlist:
            usage()
            sys.exit(2)
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)
    
    im = None
    output = None
    input = None
    size = None
    mean_file = None
    threshold = 0.5
    for o, a in optlist:
   #    print o, a
    
        if o in ("-i", "--input") and a:
             input = a
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-s", "--size"):
            try:
                w, h =a.split(',')
                size = (int(w), int(h))
            except ValueError:
                print "Invalid dimensions"
                usage()
                sys.exit(2)
        elif o in ("-m", "mean"):
            if a:
                mean_file = a
                print "Using mean file", mean_file
        elif o in ("-t", "threshold"): 
             if a:
                try:
                     threshold = float(a)
                except ValueError:
                    print "Invalid threshold"
                    usage()
                    sys.exit(2)
        # General error
        else:
           usage()
           sys.exit(2)

    if size:
        im = Image.new("RGB", size)
    else:
       usage()
       sys.exit(2)
   
    print "Input: ", input
    print "Output:", output
    if mean_file:
        print "Mean File: ", mean_file
    else:
        print "Threshold: ", threshold
    # Load image
    pixels = im.load()
    data_values = []
    target_epsi = 0.01
    mean_adjust = 0.009
    mean_values = []
    tmean = threshold
 
    # Check command line arguments
    # Read Target Mean
  
    if mean_file:
        try:
            with open(mean_file, "rb") as t:
                byte = t.read(4)
                while byte != "":
                    # Do stuff with byte.
                    try:
                        readb = t.read(4)
                        if len(readb) == 0:
                            print "End of mean data"
                            break
                        meanval ,  = struct.unpack('<f', readb)
                        mean_values.append(meanval)
                    except EOFError:
                        print "End of mean data"

                #target mean
                print "Read %s mean values " % len(mean_values)
                tmean = sum(mean_values)/len(mean_values)

                print "Target mean calculated at %s" % tmean
                threshold =  tmean-mean_adjust
           
        except IOError:
            print "File not found", mean_file
            sys.exit(2)

    print "Threshold set at ", threshold
 
        # Read Results
    try:

        with open(input, "rb") as f:
            byte = f.read(4)
            while byte != "":
                # Do stuff with byte.
                try:
                    b = f.read(4)
                    if len(b) == 0:
                        print "Done reading data set"
                        break
                    meanval ,  = struct.unpack('<f', b)
                    data_values.append(meanval)
                except EOFError:
                    print "Done reading data"
    except IOError:
        print "File not found", input
        sys.exit(2)

    print "Read %s data values " % len(data_values)
    mean = sum(data_values)/len(data_values)
    print "Data mean %s" % mean

    for i in range(im.size[0]):    # for every pixel:
        for j in range(im.size[1]):
            fval = data_values.pop()

            if fval > threshold:
                pixels[i,j] = 255, 255, 255
            elif abs(fval-mean) > target_epsi:
                pixels[i,j] = 200, 128, 17
            else:
                pixels[i,j] = 90, 90, 90


    im.show()
    im.save(output, format="PNG")	

if __name__ == "__main__":
    viewer(sys.argv[1:])




