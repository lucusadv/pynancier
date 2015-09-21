import re


def reader(filename):
    with open(filename, "r") as f:
        x_keys =  re.split(',\s*', next(f).strip())
        for line in f:
            x_values = re.split(',\s*', line.strip())[1:]
            x_values = [float(v) for v in x_values]
            yield dict(zip(x_keys, x_values))



if __name__ == '__main__':
    a = reader('testfile.csv')
