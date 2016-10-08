from PIL import Image, ImageDraw, ImageFont, ImageFilter

import requests
import io

# http://stackoverflow.com/questions/24247932/send-multiple-stringio-from-pil-image-in-post-requests-with-python

def blur(original):
    # Load an image from the hard drive
    #original = Image.open("popple.jpg")

    # Blur the image
    blurred = original.filter(ImageFilter.BLUR)

    # Display both images
    #original.show()
    #blurred.show()

    # save the new image
    #blurred.save("output.png")
    return blurred


def convert():
    for infile in sys.argv[1:]:
        f, e = os.path.splitext(infile)
        outfile = f + ".jpg"
        if infile != outfile:
            try:
                Image.open(infile).save(outfile)
            except IOError:
                print("cannot convert", infile)


def roll(image, delta):
    "Roll an image sideways"

    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize-delta, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))

    return image


def text(base):
    base = base.convert('RGBA')
    # get an image
    #base = Image.open('popple.jpg').convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype('FreeMono.ttf', 40)
    # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity
    d.text((10,10), "Hello", font=fnt, fill=(255,255,255,128))
    # draw text, full opacity
    d.text((10,60), "World", font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(base, txt)
    #out.save('output.png')
    #out.show()
    return out


def composite(overlay):
    # get an image
    overlay = overlay.convert('RGBA')
    base = Image.open('popple.jpg').convert('RGBA')
    #out = Image.alpha_composite(base, overlay)
    base.paste(overlay, (40,40), overlay)
    base.paste(overlay, (240,40), overlay)
    base.paste(overlay, (40,240), overlay)
    base.paste(overlay, (240,240), overlay)
    return base


def save(i):
    i.save('output.jpg')


def test_gen(url = None):
    if url is None:
      print("Ooops, empty URL")
      return

    r = requests.get(url)
    if r.status_code != requests.codes.ok:
      print("Ooops, status code not OK: " + str(r.status_code))
      return
#'https://scontent.xx.fbcdn.net/v/t1.0-1/c0.12.457.457/s160x160/12994355_10154089814361407_1270883076140821763_n.jpg?oh=6f3c9e328749f4fff210a22ce3c12ad9&oe=57E7BB87')
    #print(r.status_code) # requests.codes.ok
    #print(len(r.text))

    i = Image.open(io.BytesIO(r.content))
    i = blur(i)
    i = text(i)
    i = composite(i)
    save(i)
