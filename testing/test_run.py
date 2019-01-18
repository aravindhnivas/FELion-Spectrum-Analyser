
    print("\nLocation: I am here in mainloop", location)

    try:
        move = lambda x: shutil.move(my_path + "/{}".format(x), my_path + "/DATA/{}".format(x))
        
        folders = ['DATA', 'EXPORT', 'OUT']
        print("\nLocation: I am inside now", location)

        def run(folders):

            if set(folders).issubset(os.listdir(os.path.dirname(os.getcwd()))):
                print("\n##############\nYeah I am here: \n##############\n")
                loc = os.path.dirname(location)
            else: loc = location
            
            return loc

        loc = run(folders)

        os.chdir(loc)
        my_path = os.getcwd()    
        
        if(fname.find('felix')>=0): fname = fname.split('.')[0]

        back_dir = os.path.dirname(my_path)

        for i in folders:
            if not set(folders).issubset(os.listdir(back_dir)):
                if not os.path.isdir(i): os.mkdir(i)

        filename = fname + ".felix"
        powerfile = fname+".pow"
        basefile = fname+".base"

        if not os.path.isfile('DATA/%s'%filename): move(filename)
        if not os.path.isfile('DATA/%s'%basefile): move(basefile)

        #Powerfile check
        if os.path.isfile(powerfile): move(powerfile)

        data = felix_read_file(fname)

        #Check wether the baslien file exists
        if not os.path.isfile('DATA/'+basefile):
            print("Guessing baseline from .felix file!")
            xs, ys = GuessBaseLine(data)
        else:
            print("Reading baseline from .base file!")
            xs, ys, *rest = ReadBase(fname)

        fig, ax = plt.subplots()

        p = InteractivePoints(fig, ax, xs, ys)
        ax.plot(data[0], data[1], ls='', marker='o', ms=5, markeredgecolor='r', c='r')

        print("\nUSAGE:\nBlue baseline points are dragable...\
            \nKeys:\n\
        'a' - adds a point at current cursor position\n\
        'd' - delets a point at current cursor position\n\
        'w' - moves the point to the 'average' value at given x position\n\
        'q' - stores baseline in .base file and quits!\n")

        ax.set_title('BASELINE points are drag-able!')
        ax.set_xlim((data[0][0]-70, data[0][-1]+70))
        ax.set_xlabel("wavenumber (cm-1)")
        ax.set_ylabel("Counts")
        plt.show()

        print("\n{}.base Baseline Saved.".format(fname))
        if baseline != None:
            SaveBase(fname, baseline)
    
    except Exception as e:
        print("Error: ", e)
        filenotfound("ERROR: ", e)