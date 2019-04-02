#!/usr/bin/python3

# Importing Modules

# DATA analysis modules
import numpy as np
from scipy.optimize import curve_fit
from uncertainties import ufloat as uf
from uncertainties import unumpy as unp

# Custom functions
from timescan_plot import timescanplot

# Felion Modules
from FELion_definitions import ShowInfo, ErrorInfo, FELion_Toplevel

# Tkinter modules
from tkinter import Toplevel

# Matplotlib Modules
from matplotlib.widgets import Slider
from matplotlib.gridspec import GridSpec as grid

# Built-In modules
import os

def depletionPlot(files, location, power_n, dpi, parent):

    ####################################### Initialisation #######################################

    try:
        power_n = np.asarray(power_n.split(','), dtype = np.float)
        power_values, n = power_n[:-1], power_n[-1]
    except Exception:
        return ErrorInfo("Error", 'Please enter the Power_on, power_off and n_shots value.')

    np.seterr(all='ignore')
    os.chdir(location)

    ####################################### END Initialisation #######################################

    ####################################### Tkinter figure 1 #######################################

    ## Embedding figure to tkinter Toplevel
    title_name1 = 'Timescan'
    root1 = Toplevel(parent)
    tk_widget1 = FELion_Toplevel(root1, title_name1, location)

    fig1, canvas1 = tk_widget1.figure(dpi, figsize=(15,5))
    axs0 = fig1.add_subplot(111)

    ####################################### PLOTTING DETAILS Timescan #######################################

    lg_fontsize = 15
    title_fontsize = 15
    lb_size = 15
    
    counts, stde = [], []
    for f in files:        
        mass, iterations, t_res, t_b0, mean, error, time = timescanplot(f, location, dpi, parent, depletion = True)
        print('\nReturned.\n')
        axs0.errorbar(time, mean[0], yerr = error[0], label = '{}; {}:[{}], B0:{}ms, Res:{}'.format(f, mass[0], iterations[0], t_b0, t_res))
        
        time = time[1:]/1000
        mean = mean[0][1:]
        stde.append(error[0][1:])
        counts.append(mean)
        
    counts, stde = np.array(counts), np.array(stde)
    
    axs0.set_title('Timescan', fontsize=title_fontsize)
    axs0.set_xlabel('time (s)', fontsize= lb_size)
    axs0.set_ylabel('Counts', fontsize= lb_size)
    axs0.grid(True)
    axs0.legend()

    ####################################### END Plotting details #######################################

    canvas1.draw() # drawing in the tkinter canvas: canvas drawing board
    
    ####################################### END Tkinter figure 1 #######################################

    ####################################### Tkinter figure 2 #######################################

    ## Embedding figure to tkinter Toplevel
    title_name2 = 'Depletion Scan'
    root2 = Toplevel(parent)
    tk_widget2 = FELion_Toplevel(root2, title_name2, location)

    fig2, canvas2 = tk_widget2.figure(70, figsize=(25, 10))

    spec = grid(ncols=2, nrows=1, figure=fig2)

    axs = fig2.add_subplot(spec[0, 0])
    depletion_plot = fig2.add_subplot(spec[0, 1])

    ####################################### PLOTTING DETAILS Depletion Scan #######################################

    on_off = []
    for i in counts:
        on_off.append(i.min())
    on_off = np.array(on_off)
    
    K_OFF, N = [], []
    K_OFF_err, N_err = [], []
    
    K_ON, Na0, Nn0 = [], [], []
    K_ON_err, Na0_err, Nn0_err = [], [], []
    
    for i in range(0, len(counts), 2):
        
        on = np.argmin(on_off)
        off = np.argmax(on_off)
        
        # making the error '0' value as very close to '0' 
        #since div by it makes it easier while fitting parameters
        stde[on][stde[on]==0]=10e-10
        stde[off][stde[off]==0]=10e-10
        
        #depletion values; y-axis
        depletion_on, depletion_on_err = counts[on], stde[on]
        depletion_off, depletion_off_err = counts[off], stde[off]

        # power values; x-axis
        power_on = (power_values[i]*n*time)/1000. # divide by 1000 for mJ to J conversion 
        power_off = (power_values[i+1]*n*time)/1000.
        power_max = power_values.max()*n*time.max()/1000.
        x = np.linspace(0, power_max, num=len(time))
        
        axs.errorbar(power_off, depletion_off, yerr = depletion_off_err, fmt='ok')
        axs.errorbar(power_on, depletion_on, yerr = depletion_on_err, fmt='ok')
        
        ### finding parameters for fitting
        
        # depletion off
        def N_OFF(x, K_OFF, N):
            return (N)*np.exp(-K_OFF*x)
        
        K_OFF_init, N_init = 0, depletion_off.max()
        
        N_increase_bound_by = 1000
        N_upper_bound = N_init + N_increase_bound_by
        
        pop_off, popc_off = curve_fit(
            N_OFF, power_off, depletion_off,
            sigma = stde[off],
            absolute_sigma = True,
            p0 = [K_OFF_init, N_init],
            bounds = [(-np.inf, 0), (np.inf, N_upper_bound)]
            )
        
        perr_off = np.sqrt(np.diag(popc_off))
        
        # off fitting variables         
        K_OFF.append(pop_off[0])
        N.append(pop_off[1])
        
        K_OFF_err.append(perr_off[0])
        N_err.append(perr_off[1])

        # depletion on
        def N_ON(X, Na0, Nn0, K_ON):
            x, K_OFF = X
            return Na0*np.exp(-K_ON*x)*np.exp(-K_OFF*x) + Nn0*np.exp(-K_OFF*x)

        #K_ON_init, Na0_init, Nn0_init = ()
        X = (power_on, pop_off[0])
        pop_on, popc_on = curve_fit(
            N_ON, X, depletion_on,
            sigma = stde[on],
            absolute_sigma = True,
            #p0 = [Na0_init, Nn0_init, K_ON_init]
            bounds = ([0,0,-np.inf], [pop_off[1], pop_off[1], np.inf])
        )
        perr_on = np.sqrt(np.diag(popc_on))
        
        #on fitting variables
        Na0.append(pop_on[0])
        Nn0.append(pop_on[1])
        K_ON.append(pop_on[2])
        
        Na0_err.append(perr_on[0])
        Nn0_err.append(perr_on[1])
        K_ON_err.append(perr_on[2])
    
    uK_OFF, uN = unp.uarray(K_OFF, K_OFF_err), unp.uarray(N, N_err)
    uK_ON, uNa0, uNn0 = unp.uarray(K_ON, K_ON_err), unp.uarray(Na0, Na0_err) , unp.uarray(Nn0, Nn0_err)
    
    
    def Depletion(X, A):
        x, K_ON = X
        return A*(1-np.exp(-K_ON*x))
    
    uy_OFF = lambda x, uN, uK_OFF: uN*unp.exp(-uK_OFF*x)
    uy_ON = lambda x, uNa0, uNn0, uK_OFF, uK_ON : uNa0*unp.exp(-uK_ON*x)*unp.exp(-uK_OFF*x) + uNn0*unp.exp(-uK_OFF*x)
    
    A, A_err = [], []
    
    for i in range(len(N)):
        
        udepletion = 1 - uy_ON(x, uNa0[i], uNn0[i], uK_OFF[i], uK_ON[i])/uy_OFF(x, uN[i], uK_OFF[i])
        depletion, depletion_error = unp.nominal_values(udepletion), unp.std_devs(udepletion)
        
        #fitting for depletion
        X = (x, K_ON[i])
        pop_depletion, poc_depletion = curve_fit(
            Depletion, X, depletion, 
            sigma = depletion_error,
            absolute_sigma = True
        )
        
        A.append(pop_depletion[0])
        perr_A = np.sqrt(np.diag(poc_depletion))
        A_err.append(perr_A[0])

    uA = unp.uarray(A, A_err)

    def plot(i, l):
        # off plotting
        y_off0 = N_OFF(x, K_OFF[i], N[i])
        g_off0, = axs.plot(x, y_off0, label = 'N_OFF: [{:.2f}mJ], K_OFF={:.2fP}/J, N={:.2fP}'.format(power_values[i+1], uK_OFF[i], uN[i]))

        # on plotting
        y_on0 = N_ON((x, K_OFF[i]), Na0[i], Nn0[i], K_ON[i])
        g_on0, = axs.plot(x, y_on0, label = 'N_ON: [{:.2f}mJ], K_ON={:.2fP}/J, N={:.2fP}, Na0={:.2fP}, Nn0={:.2fP}'.format(power_values[i], uK_ON[i], uNa0[i]+uNn0[i], uNa0[i], uNn0[i]))
        
        # deletion plot
        udepletion_new = 1 - uy_ON(x, uNa0[i], uNn0[i], uK_OFF[i], uK_ON[i])/uy_OFF(x, uN[i], uK_OFF[i])
        depletion_new, depletion_error_new = unp.nominal_values(udepletion_new), unp.std_devs(udepletion_new)

        depletion0, = depletion_plot.plot(x, depletion_new, '--')
        
        depletion_fitted = Depletion(X, A[i])
        depletion1, = depletion_plot.plot(x, depletion_fitted,
                                        label = 'A = {:.2fP}, K_ON = {:.2fP}/J'.format(uA[i], uK_ON[i])
                                        )
        
        # controlling fitting parameters
        axcolor = 'lightgoldenrodyellow'
        
        koff_g = fig2.add_axes([l, 0.12, 0.2, 0.015], facecolor=axcolor) #[left, bottom, width, height]
        n_g = fig2.add_axes([l, 0.10, 0.2, 0.015], facecolor=axcolor)
        kon_g = fig2.add_axes([l, 0.08, 0.2, 0.015], facecolor=axcolor)
        na_g = fig2.add_axes([l, 0.06, 0.2, 0.015], facecolor=axcolor)
        nn_g = fig2.add_axes([l, 0.04, 0.2, 0.015], facecolor=axcolor)
        
        # inc = 0.2

        # b0 = 0.12
        # b1 = b0 - inc
        # b2 = b1 - inc
        # b3 = b2 - inc
        # b4 = b3 - inc

        # w, h = 0.2, 0.015
        
        # koff_g = fig2.add_axes([l, b0, w, h], facecolor=axcolor) #[left, bottom, width, height]
        # n_g = fig2.add_axes([l, b1, w, h], facecolor=axcolor)

        # kon_g = fig2.add_axes([l, b2, w, h], facecolor=axcolor)
        # na_g = fig2.add_axes([l, b3, w, h], facecolor=axcolor)
        # nn_g = fig2.add_axes([l, b4, w, h], facecolor=axcolor)

        koff_slider = Slider(koff_g, '$K_{OFF}$', 0, K_OFF[i]+10, valinit = K_OFF[i])
        n_slider = Slider(n_g, 'N', 0, N[i]+(N[i]/2), valinit = N[i])

        kon_slider = Slider(kon_g, '$K_{ON}$', 0, K_ON[i]+10, valinit = K_ON[i])
        na_slider = Slider(na_g, '$Na_0$', 0, Na0[i]+(Na0[i]/2), valinit = Na0[i])
        nn_slider = Slider(nn_g, '$Nn_0$', 0, Nn0[i]+(Nn0[i]/2), valinit = Nn0[i])
                
        def update(val):
            
            koff = koff_slider.val
            ukoff = uf(koff, K_OFF_err[i])

            n = n_slider.val
            un = uf(n, N_err[i])

            kon = kon_slider.val
            ukon = uf(kon, K_ON_err[i])

            na = na_slider.val
            una = uf(na, Na0_err[i])

            nn = nn_slider.val
            unn = uf(nn, Nn0_err[i])

            yoff = N_OFF(x, koff, n)
            g_off0.set_ydata(yoff)

            yon = N_ON((x, koff), na, nn, kon)
            g_on0.set_ydata(yon)
            
            # depletion
            udepletion_new1 = 1 - uy_ON(x, una, unn, ukoff, ukon)/uy_OFF(x, un, ukoff)
            depletion_new1, depletion_error_new1 = unp.nominal_values(udepletion_new1), unp.std_devs(udepletion_new1)
            depletion0.set_ydata(depletion_new1)
            
            X = (x, kon)
            pop_depletion, poc_depletion = curve_fit(
                    Depletion, X , depletion_new1, 
                    sigma = depletion_error_new1, 
                    absolute_sigma = True
                )
            
            A_new1 = pop_depletion[0]
            perr = np.sqrt(np.diag(poc_depletion))[0]
            uA_new1 = uf(A_new1 , perr)
    
            depletion_fitted_new = Depletion(X, A_new1)
            depletion1.set_ydata(depletion_fitted_new)

            # k = i*2
            # legend.get_texts()[k].set_text('N_OFF: [{:.2f}mJ], K_OFF={:.2fP}/J, N={:.2fP}'.format(power_values[i+1], ukoff, un))
            # legend.get_texts()[k+1].set_text('N_ON: [{:.2f}mJ], K_ON={:.2fP}/J, N={:.2fP}, Na0={:.2fP}, Nn0={:.2fP}'.format(power_values[i], ukon, una+unn, una, unn))
            # depletion_legend.get_texts()[i].set_text('A = {:.2fP}, K_ON = {:.2fP}/J'.format(uA_new1, ukon))

            canvas2.draw_idle()
            
            return fig2

        koff_slider.on_changed(update)
        n_slider.on_changed(update)

        kon_slider.on_changed(update)
        na_slider.on_changed(update)
        nn_slider.on_changed(update)
    
        return koff_slider, n_slider, kon_slider, na_slider, nn_slider, koff_g, n_g, kon_g, na_g, nn_g, fig2

    widget_position = l = 0.05
    for i in range(len(N)):
        koff_slider, n_slider, kon_slider, na_slider, nn_slider, koff_g, n_g, kon_g, na_g, nn_g, fig2 = plot(i, l)
        l += 0.25

    ### setting labels
    # title_depletion1 = '$N_{ON}(ntE)=N_{a0}e^{-k_{on}ntE}e^{-k_{off}ntE} + N_{n0}e^{-k_{off}ntE}$ ;\t$N_{OFF}(ntE)=(N)e^{-k_{off}ntE}$ ; $N = N_{a0}+ N_{n0}$'
    # axs.set_title(title_depletion1, fontsize=title_fontsize)
    axs.set_xlabel('$n * t * E (Joule)$', fontsize= lb_size)
    axs.set_ylabel('Counts', fontsize= lb_size)

    axs.grid(True)
    # box = axs.get_position()
    # axs.set_position([box.x0, box.y0, box.width*0.6, box.height])
    # legend = axs.legend(loc='center left', bbox_to_anchor=(1, 0.95), title=files, fontsize=lg_fontsize-2)
    # legend.get_title().set_fontsize(lg_fontsize)
    legend = axs.legend(loc = 'upper right')
    
    depletion_plot.grid(True)
    depletion_legend = depletion_plot.legend(loc = 'lower right', fontsize=lg_fontsize)
    depletion_plot.set_xlabel('$n * t * E (Joule)$', fontsize= lb_size)
    depletion_plot.set_ylabel('Relative abundance of active isomer', fontsize= lb_size)
    # depletion_plot.set_title('$D(ntE) = 1-N_{ON}/N_{OFF}$ fitted with $D(ntE) = A(1-e^{K_{ON}*ntE})$', fontsize = title_fontsize)
    
    ####################################### END Plotting details #######################################

    canvas2.draw_idle() # drawing in the tkinter canvas: canvas drawing board
    
    ####################################### END Tkinter figure 2 #######################################


    # except Exception as e:
    #     ErrorInfo("ERROR", e)