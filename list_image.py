from PIL import Image, ImageFont, ImageDraw


def underlined_text(ctx, pos, text, font, **kw_args):
    """creates underlined text without having to calculate the position manually"""
    text_width, text_height = ctx.textsize(text, font=font)
    line_x, line_y = pos[0], pos[1] + text_height + 1
    ctx.text(pos, text, font=font, **kw_args)
    ctx.line((line_x, line_y, line_x + text_width, line_y), **kw_args)


def create_image(user, width, height, bg_colour, text_colour, alt_text_colour, songs, margin):
    """creates the image given all of the parameters"""
    # set up image
    img = Image.new(mode='RGB', size=(width, height), color=bg_colour)
    draw = ImageDraw.Draw(img)

    # title
    title_font = ImageFont.truetype('Fonts/NotoSansJP-Regular.otf', 32)
    title = f"{user}'s song list!"
    title_width, title_height = draw.textsize(title, font=title_font)
    title_height += 11
    underlined_text(draw, ((width / 2) - (title_width / 2), 10), title, font=title_font, fill=alt_text_colour)  # (width/2)-(title_width/2) centers the text

    # border
    draw.rounded_rectangle((margin, title_height + margin, width - margin, height - margin), fill=bg_colour, outline=alt_text_colour, width=2, radius=margin)

    # songs
    pad = 10
    song_font = ImageFont.truetype('Fonts/NotoSansJP-Regular.otf', 14)
    song_width = pad + margin
    song_spacing = 3
    song_min_height = title_height + pad + (1.5 * margin)
    song_text_height = draw.textsize("A1", font=song_font)[1]
    for i in range(len(songs)):
        draw.text((song_width, ((i - 1) * song_spacing) + song_min_height + (song_text_height * i)), f"{i + 1}. {songs[i]}", color=text_colour, font=song_font)

    # save image
    img.save(f"Exports/{user}'s exported list.png")


def calculate_songs_height(songs, margin):
    """calculates the height of the songs text portion of the image"""
    temp = Image.new(mode='RGB', size=(0, 0), color="#FFFFFF")
    calc = ImageDraw.Draw(temp)
    return (((calc.textsize("A1", font=(ImageFont.truetype('Fonts/NotoSansJP-Regular.otf', 14)))[1]) + 3) * len(songs)) + margin


def export_image(user, bg_colour, text_colour, alt_text_colour, songs):
    """creates an image of the users list"""
    margin = 25
    songs_height = calculate_songs_height(songs, margin)
    create_image(user, 525, 124 + songs_height, bg_colour, text_colour, alt_text_colour, songs, margin)


# ↓ debug ↓
if __name__ == '__main__':
    songs = ["Halcyon", "Mirage garden", "Happy end of the world", "Ascension to heaven", "Freedom dive", "レイニブーツ", "ひみつの小学生", "Lag train", "Loop spinner", "Secret music"]
    export_image("Fuyumi", "#002b4a", "#c3c3c3", "#defffe", songs)
