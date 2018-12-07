import numpy as np
import matplotlib.pyplot as plt
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some mass spec data.')
    parser.add_argument('date', metavar='D', type=str, help='name file')
    parser.add_argument('-a', '--amount', type=int, help='amount of scans')

    args = parser.parse_args()


def main(date):
    """  """
    if args.amount:
        for scans in range(args.amount):
            date = input('scan number or filename: ')
            if len(date) <2:
                date= args.date[0:9] + date +'.mass'
            else:
                date= date + '.mass'
            with open(date) as f:
                data = f.read()

            data = data.split('\n')

            x = -np.ones(len(data))
            y = -np.ones(len(data))

            for index, a in enumerate(data):

                if '#' in a or len(a) < 1:
                    if '# m03_ao09_width' in a:
                        a = a.split('\t\t#')
                        b0 = "%.0f" % (int(a[3]) / 1000)
                else:
                    a = a.split('\t')
                    x[index] = float(a[0])
                    y[index] = float(a[1])

            name = f.name[:8].replace('_', '-')

            plt.semilogy(x, y, label= input('legenda input: '))
            plt.legend()

        compound_name = input("What is your compounds name? ")
        compound_structure = input('The structure? ')
        Temp = input('Temperature? ')
        ion = input('Electron energy? ')

        plt.suptitle('Mass spectrum ion source from {} ({}) \n {}, T={}K, B0 opening {} ms, Ee={}V'.format(compound_name, compound_structure, name, Temp, b0, ion))

        plt.xlabel('mass [u]')
        plt.ylabel('ion counts /{} ms'.format(b0))
        plt.grid(True)
        plt.ylim(1)

        plt.show()

    else:
        date= date + '.mass'
        with open(date) as f:
            data = f.read()

        data = data.split('\n')

        x = -np.ones(len(data))
        y = -np.ones(len(data))

        for index, a in enumerate(data):

            if '#' in a or len(a) < 1:
                if '# m03_ao09_width' in a:
                    a = a.split('\t\t#')
                    b0 = "%.0f" % (int(a[3])/1000)
            else:
                a = a.split('\t')
                x[index] = float(a[0])
                y[index] = float(a[1])

        name = f.name[:8].replace('_', '-')

        plt.semilogy(x, y)
        if args.amount:
            plt.title('{}, T={}K, B0 opening {} ms, Ee={}V'.format(name,Temp, b0, ion))
            plt.suptitle('Mass spectrum ion source from {} ({})'.format(compound_name,compound_structure))
        plt.xlabel('mass [u]')
        plt.ylabel('ion counts /{} ms'.format(b0))
        plt.grid(True)
        plt.ylim(1)

        plt.show()

main(args.date)

