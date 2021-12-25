from pathlib import Path
from itertools import product


def parse_input(file=__file__, suffix=None):
    p = Path(file)
    with open(p.parent.joinpath('input').joinpath(p.stem + ('' if suffix is None else '-' + suffix) + '.txt')) as f:
        enhance = [1 if c == '#' else 0 for c in f.readline().strip()]
        image = []
        for r in f.readlines() + ['']:
            if r.strip() == '':
                continue
            image.append([1 if c == '#' else 0 for c in r.strip()])
        return image, enhance


def pad_image(image, boundary):
    res = []
    res.append([boundary] * (len(image) + 4))
    res.append([boundary] * (len(image) + 4))
    for r in image:
        res.append([boundary, boundary] + r[:] + [boundary, boundary])
    res.append([boundary] * (len(image) + 4))
    res.append([boundary] * (len(image) + 4))
    return res


def shifts(i, j):
    return product(range(i - 1, i + 2), range(j - 1, j + 2))


def decode(pimage, enhance, i, j):
    x = ''
    for jj, ii in shifts(j, i):
        x += str(pimage[jj][ii])
    x = int(x, 2)
    return enhance[x]


def iterate(image, enhance, boundary=None):
    if boundary is None:
        boundary = image[0][0]
    pimage = pad_image(image, boundary)
    res = pad_image(image, enhance[0] if boundary == 0 else enhance[511])
    for i in range(1, len(pimage[0])-1):
        for j in range(1, len(pimage)-1):
            res[j][i] = decode(pimage, enhance, i, j)
    return res


def solve(values, enhance, count):
    image = values
    for i in range(count):
        image = iterate(image, enhance, boundary=(0 if i==0 else None))
    res = 0
    for r in image:
        res += sum(r)
    return res


if __name__ == "__main__":
    input_values, enhance = parse_input()

    print("Part 1:", solve(input_values, enhance, 2))
    print("Part 2:", solve(input_values, enhance, 50))
