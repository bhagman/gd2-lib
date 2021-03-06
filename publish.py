#!/usr/bin/python
#
# This program assembles the distribution file Gameduino2.zip
# from the source .ino files, and the asset files in
# converted-assets.
#

inventory = {
    '1.Basics'      : "helloworld fizz blobs simon jpeg",
    '2.Graphics'    : "logo walk tiled mono slotgag reflection",
    '3.Peripherals' : "sketch tilt noisy song",
    '4.Utilities'   : "viewer radarchart selftest",
    '5.Demos'       : "cobra jnr kenney sprites widgets",
    '6.Games'       : "nightstrike chess invaders frogger",
}

import zipfile

def clean(src):
    vis = 1
    dst = []
    for l in src:
        assert not chr(9) in l, "Tab found in source"
        if "//'" in l:
            l = l[:l.index("//'")]
        if vis and not "JCB" in l:
            dst.append(l.rstrip() + "\n")
        else:
            if "JCB{" in l:
                vis = 0
            if "}JCB" in l:
                vis = 1
    return "".join(dst)

z = zipfile.ZipFile("Gameduino2.zip", "w", zipfile.ZIP_DEFLATED)

for f in "keywords.txt GD2.cpp GD2.h transports/wiring.h".split():
    z.write(f, "Gameduino2/%s" % f)

for d,projs in inventory.items():
    dir = "Gameduino2" + "/" + d
    for p in projs.split():
        pd = dir + "/" + p
        z.writestr("%s/%s.ino" % (pd, p), clean(open("%s.ino" % p)))
        for l in open("%s.ino" % p):
            if '#include "' in l:
                hdr = l[10:l.rindex('"')]
                z.write("converted-assets/%s" % hdr, "%s/%s" % (pd, hdr))

z.close()

# print ["./mkino %s" % s for s in " ".join(inventory.values()).split()]
