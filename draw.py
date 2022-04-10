from svg.path import parse_path
import argparse
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy
import os
import xml.etree.ElementTree as ET


def parse_svg_file(file):
    tree = ET.parse(file)
    root = tree.getroot()
    width = int(float(root.attrib['viewBox'].split()[2]))
    height = int(float(root.attrib['viewBox'].split()[3]))
    path_string = ''
    for p in root.findall('.//{http://www.w3.org/2000/svg}path'):
        path_string += p.attrib['d']
    path = parse_path(path_string)
    return width, height, path


def get_render_func_svg(width, height, path, period):
    def render_func_svg(t):
        return path.point(t / period) + (width + height * 1j)
    return render_func_svg


def render_func_circle(t):
    return math.cos(t) + 1j * math.sin(t)


def render_func_line(t):
    return math.cos(t)


def compute_exp(n, period, t):
    return math.cos(2 * math.pi * n / period * t) + 1j * math.sin(2 * math.pi * n / period * t)


def compute_c_n(f, n, period, steps):
    total = 0 + 0j
    resolution = period / steps
    for step in range(steps):
        t = step * resolution
        total += f(t) * compute_exp(-n, period, t)
    c_n = total / steps
    return c_n


def compute_c_ns(f, period, total_n, steps):
    c_ns = []
    for n in range(total_n):
        c_ns.append(compute_c_n(f, n, period, steps))
    return c_ns


def compute_term(c_n, n, period, t):
    return c_n * compute_exp(n, period, t)


def compute_f_x_t(c_ns, period, total_n, steps):
    resolution = period / steps
    f_x_t = []
    for step in range(steps):
        t = step * resolution
        f_x = []
        for n in range(total_n):
            c_n = c_ns[n]
            f_x.append(compute_term(c_n, n, period, t))
        f_x_t.append(f_x)
    return f_x_t


def print_c_ns(c_ns):
    for c_n in c_ns:
        print('(%.2f + %.2fi)' % (c_n.real, c_n.imag))


def print_f_x_t(f_x_t):
    for f_x in f_x_t:
        line = []
        for term in f_x:
            line.append('(%.2f, %.2f)' % (term.real, term.imag))
        print(line)


def compute_cumsum(f_x):
    x = numpy.cumsum([0, ] + [term.real for term in f_x])
    y = numpy.cumsum([0, ] + [term.imag for term in f_x])
    return x, y


def get_animate(ax, f_x_t, steps):
    trace_x = []
    trace_y = []
    alphas = []
    trace, = ax.plot([], [], '-', lw=1)
    arrows, = ax.plot([], [], '.-', lw=1, alpha=0.5)

    def animate(i):
        cumsum = compute_cumsum(f_x_t[i % steps])
        trace_x.append(cumsum[0][-1])
        trace_y.append(cumsum[1][-1])
        trace.set_data(trace_x, trace_y)
        arrows.set_data(*cumsum)
        ax.relim()
        ax.autoscale_view()
        return trace, arrows
    return animate


def main(input_file_path, num_terms, steps, cycles, render=False, render_type='video'):
    period = 2 * math.pi

    width, height, path = parse_svg_file(input_file_path)
    render_func = get_render_func_svg(width, height, path, period)
    c_ns = compute_c_ns(render_func, period, num_terms, steps)
    f_x_t = compute_f_x_t(c_ns, period, num_terms, steps)

    fig = plt.figure()
    fig.canvas.manager.set_window_title(input_file_path)
    plt.axis('off')
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=True)
    animate = get_animate(ax, f_x_t, steps)
    ani = animation.FuncAnimation(fig, animate, frames=steps * cycles, interval=1000.0 / 60, blit=False)
    if render:
        base_name_without_extension = os.path.basename(input_file_path).rsplit('.')[0]
        if render_type == 'mp4':
            ani.save('output/%s.mp4' % base_name_without_extension, fps=60, extra_args=['-vcodec', 'libx264'])
        elif render_type == 'gif':
            ani.save('output/%s.gif' % base_name_without_extension, fps=60, writer='imagemagick')
    plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate Fourier Series for an SVG and optionally render a video.')
    parser.add_argument('-i', '--input-file-path', action='store', type=str, help='The path to the input svg', required=True)
    parser.add_argument('-n', '--num-terms', action='store', type=int, help='The number of Fourier coefficients terms to compute', default=1000)
    parser.add_argument('-s', '--steps', action='store', type=int, help='The number of steps to render', default=1000)
    parser.add_argument('-c', '--cycles', action='store', type=int, help='The number of cycles to render', default=1)
    parser.add_argument('-r', '--render', action='store_true', help='Whether to render to an output file or not')
    parser.add_argument('-t', '--render-type', action='store', type=str, help='Render to mp4 or gif', default='mp4')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    main(args.input_file_path, args.num_terms, args.steps, args.cycles, render=args.render, render_type=args.render_type)
