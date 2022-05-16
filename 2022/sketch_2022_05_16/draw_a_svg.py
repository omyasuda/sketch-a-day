from random import randint, choice
from pyodide import create_proxy


svgNS = 'http://www.w3.org/2000/svg'
svgelement = document.createElementNS(svgNS, 'svg')
svgelement.setAttributeNS(None, 'width', '800px')
svgelement.setAttributeNS(None, 'height', '800px')

def circle(x, y, d, stroke='black', fill='white'):
    c = document.createElementNS(svgNS, 'circle')
    c.setAttributeNS(None, 'cx', x)
    c.setAttributeNS(None, 'cy', y)
    c.setAttributeNS(None, 'r', d / 2)
    c.setAttributeNS(None, 'fill', fill)
    c.setAttributeNS(None, 'stroke', stroke)
    svgelement.appendChild(c)
    return c

def rect(x, y, w, h, stroke='black', fill='white'):
    r = document.createElementNS(svgNS, 'rect')
    r.setAttributeNS(None, 'x', x)
    r.setAttributeNS(None, 'y', y)
    r.setAttributeNS(None, 'width', w)
    r.setAttributeNS(None, 'height', h)
    r.setAttributeNS(None, 'fill', fill)
    r.setAttributeNS(None, 'stroke', stroke)
    svgelement.appendChild(r)
    return r

def text(x, y, text, size=5, fill='black'):
    t = document.createElementNS(svgNS, 'text')
    t.setAttributeNS(None, 'x', x)
    t.setAttributeNS(None, 'y', y)
    t.style.fill = fill
    t.style.fontSize = str(size)
    t.style.fontFamily = 'monospace'
    t.style.textAnchor = 'middle'
    t.innerHTML = text
    svgelement.appendChild(t)
    return t


def draw_records(xo, yo, wo, ho, records, **kwargs):
    margin = kwargs.pop('margin', 5)
    x, y = xo + margin, yo + margin,
    w, h = wo - 2 * margin, ho - 2 * margin
    total_area = sum(map(lambda r: r[1], records))
    rx = ry = 0
    for i, (name, area, sub) in enumerate(records):
        hue = remap(area, 0, total_area / 4, 60, 300)
        bri = remap(area, 0, total_area / 4, 100, 50)
        if w > h:
            rw, rh = remap(area, 0, total_area, 0, w), h
        else:
            rw, rh = w, remap(area, 0, total_area, 0, h)
        rect(x + rx, y + ry, abs(rw), abs(rh), fill=f"hsl({hue},80%,{bri}%)")
        if sub:
            if rw * rh > 20000 and rh >= margin * 3 and rw >= margin * 3:
                next_sub = choice((1, 0))
            else:
                next_sub = 0
            next_records = generate_records(name, next_sub)
            draw_records(x + rx, y + ry, rw, rh, next_records)
        else:
            ts = 5
            while len(name) * ts < rw and ts < rh / 3:
                ts += 1
            if ts != 5:
                text(x + rx + rw / 2,
                     y + ry + rh / 2 + ts / 2,
                     name, ts, fill='black')
            else:
                circle(x + rx + rw / 2, y + ry + rh / 2, min(rh, rw) / 10, fill='black')
        if w > h:
            rx += rw
        else:
            ry += rh


def generate_records(name, next_sub=True):
    if name:
        name += '.'
    return [
        (name + next_name, randint(1, 5), next_sub) for next_name in '012345'
    ]


def remap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

records = generate_records('')
draw_records(0, 0, 800, 800, records, margin=0)
# write into DIV
document.getElementById('ContainerBox').append(svgelement)

def mouse_pressed(e):
    if e.button == 0: #left mouse button
#         circle(e.offsetX,e.offsetY, randint(40, 70))
#     else:
        svgelement.innerHTML = ''
        records = generate_records('')
        draw_records(0, 0, 800, 800, records, margin=0)
        #c = circle(e.offsetX,e.offsetY, randint(40, 70))

on_click = create_proxy(mouse_pressed)
svgelement.addEventListener("mousedown", on_click)
