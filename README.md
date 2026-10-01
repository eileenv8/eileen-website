# eileen-website

Personal site for Eileen Margaret Vert Jubilee — plain HTML, CSS, and one p5.js
sketch. No framework, no build step, no CMS.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole page. All copy lives here. |
| `styles.css` | All styling. Colors and spacing are CSS variables at the top, in `:root`. |
| `sketch.js` | The p5.js animation behind the hero: a mycelial network that grows, fuses into nodes, and pulses. |
| `vercel.json` | Tells Vercel this is a static site, not a Next.js app. |
| `clothesline/index.html` | Clothesline SF, the styling business with Ashley. Served at `/clothesline`. Self-contained: its CSS and JS live in the one file. |
| `portraits/` | Ten illustrated portraits of Eileen and the code that draws them. See `portraits/README.md`. |

## Editing it

Open `index.html` in a text editor and change the words. That's it — there is
nothing to install, compile, or rebuild. To see your changes locally, open the
file in a browser, or run a small server so relative paths behave:

```
python3 -m http.server 8000    # then visit http://localhost:8000
```

To change colors or spacing, edit the variables at the top of `styles.css`.

To change the About image, put your picture in the `images` folder, then in
`index.html` find the comment that says `ABOUT IMAGE` and change the `src` on
the line below it to your file's name (for example `images/my-picture.jpg`),
and set `width` and `height` to the picture's size in pixels.
Keep files under about 500KB so the page stays fast; a JPG around 1200px tall
is plenty.

To add a writing entry, uncomment the `<ul class="entries">` block in the
Writing section of `index.html` and duplicate one `<li>`.

## Deploying

Vercel builds from the `main` branch. Push to `main` and it redeploys.

## History

This repo previously held a Next.js 15 + Tailwind + Sanity CMS scaffold. That
code is still in git history (see commits before the static rewrite) if the
photostream and blog are ever revived.
