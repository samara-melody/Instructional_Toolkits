import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from disba import EigenFunction
import inspect


def plot_synthetic_model(velocity_model, depths):
    fig, ax = plt.subplots(1, 3, figsize=(6, 4), sharey=True)

    ax[0].plot(velocity_model[:, 1], depths, 'k', lw=2)
    ax[0].set_xlabel('Vp')
    ax[0].set_ylabel('Depth (m)')
    ax[0].grid()
    ax[0].invert_yaxis()
    
    ax[1].plot(velocity_model[:, 2], depths, 'k', lw=2)
    ax[1].set_xlabel('Vs')
    ax[1].grid()

    ax[2].plot(velocity_model[:, 3], depths, 'k', lw=2)
    ax[2].set_xlabel('Rho')
    ax[2].grid()
    
    fig.suptitle('Synthetic Model', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig, ax


def plot_observed_data(f_obs, d_obs, f_true=None, d_true=None):
    fig, ax = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [2, 1]})
    
    cmap = plt.get_cmap('autumn')
    colors = cmap(np.linspace(0, 1, len(f_obs)))
    
    ax[0].scatter(f_obs, d_obs, c=colors, edgecolors='black', zorder=3, label='Observed Data')
    ax[0].set_xlabel('Frequency [Hz]')
    ax[0].set_ylabel('Phase velocity [km/s]')
    ax[0].grid()


    ax[1].scatter(d_obs, d_obs / f_obs, c=colors, edgecolors='black', zorder=3, label='Observed Data')
    ax[1].set_ylabel('Wavelength [km]')
    ax[1].set_xlabel('Phase velocity [km/s]')
    ax[1].grid()
    ax[1].set_ylim([max(d_obs / f_obs) + 0.05, 0])

    if f_true is not None and d_true is not None:
        ax[0].plot(f_true, d_true, 'k--', label='True Data', lw=0.5)
        ax[1].plot(d_true, d_true / f_true, 'k--', label='True Data', lw=0.5)
        
    handles, labels = ax[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(.98, 0.5), frameon=False)

    fig.suptitle('Observed Data versus True Synthetic Data', fontsize=14, fontweight='bold')
    plt.tight_layout(w_pad=2)

    return fig, ax


def plot_rayleigh_eigenfunctions(velocity_model, thick, freq):
    eigf = EigenFunction(*velocity_model.T)

    fig, ax = plt.subplots(1, 2, figsize=(10, 6),gridspec_kw={'width_ratios': [1, 1]},sharey=True, sharex=True)

    for d in np.cumsum(thick):
        ax[0].hlines(y=d / 1000, xmin=-1.3, xmax=1.3, colors='k', linestyles=':')
        ax[1].hlines(y=d / 1000, xmin=-1.3, xmax=1.3, colors='k', linestyles=':')

    cmap = plt.cm.viridis

    for e, f in enumerate(freq):
        eigr = eigf(1 / f, mode=0, wave="rayleigh")
        color = cmap(e / (len(freq) - 1))

        ax[0].plot(eigr.uz, eigr.depth, linestyle="-", linewidth=2, label=f'{f:.2f} Hz', color=color)
        ax[1].plot(-eigr.ur, eigr.depth, linestyle="-", linewidth=2, label=f'{f:.2f} Hz', color=color)

    ax[0].axvline(0, color='dimgrey', linewidth=1)
    ax[0].set_title('Uz Depth Sensitivity')
    ax[0].set_xlabel('Normalized Eigenfunction')
    ax[0].set_ylabel('Depth (km)')
    ax[0].grid()
    ax[0].set_xlim(-1.3, 1.3)
    ax[0].invert_yaxis()

    ax[1].axvline(0, color='dimgrey', linewidth=1)
    ax[1].set_title('Ur Depth Sensitivity')
    ax[1].set_xlabel('Normalized Eigenfunction')
    ax[1].grid()
    
    handles, labels = ax[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(.98, 0.5), frameon=False)
    
    fig.suptitle('Normalized Eigenfunction Kernels', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig, ax




def plot_parameters(forward_vp, forward_rho,
    vmin, vmax, perturb_std, std_min, std_max, std_perturb_std,
    n_dimensions, n_dimensions_min, n_dimensions_max,
    vs_min, vs_max, vs_position, vs_perturb_std, vp_vs,
    n_chains, n_iterations, burnin_iterations, save_every,
    vmin_prior, vmax_prior, depth_prior, Voronoi1D, velocity_model=None, depths=None):
    
    fig, ax = plt.subplots(1, 4, figsize=(15, 6), gridspec_kw={'width_ratios': [1, 1, 1, 1.5]})
    for a in ax[0:3]:
        a.sharey(ax[0])
  
    vp_code = inspect.getsource(forward_vp).strip()
    rho_code = inspect.getsource(forward_rho).strip()

    textstr = (
        r"$\bf{VORONOI\ POSITIONS\ (DEPTH-CONTROL)}$" + f"""
        vmin = {vmin}
        vmax = {vmax}
        perturb_std = {perturb_std} \n\n""" +

        r"$\bf{NOISE\ PARAMETERIZATION}$" + f"""
        std_min = {std_min}
        std_max = {std_max}
        std_perturb_std = {std_perturb_std} \n\n""" +

        r"$\bf{TD\ PARAMETERIZATION}$" + f"""
        n_dimensions = {n_dimensions}
        n_dimensions_min = {n_dimensions_min}
        n_dimensions_max = {n_dimensions_max} \n\n""" +

        r"$\bf{VS\ PARAMETERIZATION}$" + f"""
        vs_min = {vs_min}
        vs_max = {vs_max}
        vs_position = {vs_position}
        vs_perturb_std = {vs_perturb_std} \n\n""" +

        r"$\bf{VP\ and\ RHO\ RELATIONSHIPS\ to\ VS}$" + f"""
        vp_vs = {vp_vs}
        {vp_code}
        {rho_code} \n\n""" +

        r"$\bf{MCMC\ PARAMTERIZATION}$" + f"""
        n_chains = {n_chains}
        n_iterations = {n_iterations}
        burnin_iterations = {burnin_iterations}
        save_every = {save_every} \n\n"""
        )

    if velocity_model is not None and depths is not None:
        Voronoi1D.plot_tessellation(velocity_model[:, 0], velocity_model[:, 2],label='True Vs', ax=ax[0], color='k', lw=2, input_type='extents')
        ax[0].set_ylim(np.cumsum(velocity_model[:, 0])[-1] + max(velocity_model[:, 0]), 0)
    else:
        ax[0].invert_yaxis()
    
    ax[0].set_xlabel('Vs [km/s]')
    ax[0].set_ylabel('Depth [km]')
    ax[0].grid()

    ax[0].fill_betweenx(depth_prior, vmin_prior, vmax_prior, alpha=0.2, label='Prior')
    ax[0].plot(vs_min, vs_position, '.b')
    ax[0].plot(vs_max, vs_position, '.b')
    
    if velocity_model is not None and depths is not None:
        ax[1].plot(velocity_model[:, 1], depths, 'k', lw=2)
        ax[1].plot(forward_vp(velocity_model[:, 2]), depths, '--r', label='True Vp')
        ax[1].set_ylim(np.cumsum(velocity_model[:, 0])[-1] + max(velocity_model[:, 0]), 0)
    ax[1].set_xlabel('Vp [km/s]')
    ax[1].grid()
    
    if velocity_model is not None and depths is not None:
        ax[2].plot(velocity_model[:, 3], depths, 'k', lw=2)
        ax[2].plot(forward_rho(velocity_model[:, 2]), depths, '--r', label='True Rho')
        ax[2].set_ylim(np.cumsum(velocity_model[:, 0])[-1] + max(velocity_model[:, 0]), 0)
    ax[2].set_xlabel('Rho [gcc]')
    ax[2].grid()

  
    ax[3].text(0.5, 0.5, textstr, fontsize=10, va='center', ha='center', 
               bbox=dict(boxstyle='round,pad=.5', facecolor='whitesmoke', edgecolor='gray'))
    ax[3].axis("off")
    
    return fig, ax




def plot_vs_depth_posteriors(depth_prior, vmax, vmin_prior, vmax_prior, vs_min, vs_max, vs_position, n_dimensions_min, n_dimensions_max,
    sampled_thickness, sampled_vs, statistics_vs, interp_depths, sampled_voronoi_nuclei, Voronoi1D, scale_vs=2, interf_bins=50, velocity_model=None):
    
    ncols = 4 + n_dimensions_max - n_dimensions_min
    width_ratios = [5] + [1] * (ncols - 1)

    fig, ax = plt.subplots(1, ncols,figsize=(12, 8), gridspec_kw={'width_ratios': width_ratios})
    
    ax[0].fill_betweenx(depth_prior, vmin_prior, vmax_prior, alpha=0.1, label='Prior');
    ax[0].plot(vs_min, vs_position, '--b.', lw=0.5, alpha=0.5);
    ax[0].plot(vs_max, vs_position, '--b.', lw=0.5, alpha=0.5);

    ax[0], cbar = Voronoi1D.plot_tessellation_density(sampled_thickness, sampled_vs,
        input_type='extents', ax=ax[0],cmap='GnBu',norm=LogNorm(vmin=0.1, vmax=vmax*scale_vs))
    
    if velocity_model is not None:
        Voronoi1D.plot_tessellation(velocity_model[:, 0], velocity_model[:, 2], ax=ax[0],color='k', lw=2, label='True Vs', input_type='extents');
    

    ax[0].plot(statistics_vs['mean'], interp_depths, ':r', lw=2, label='Vs Ensemble Mean');
    ax[0].plot(statistics_vs['median'], interp_depths, '--r', lw=2, label='Vs Ensemble Median');
    ax[0].plot(statistics_vs['percentiles'][0], interp_depths, '--m', lw=1, label='10th percentile');
    ax[0].plot(statistics_vs['percentiles'][1], interp_depths, ':m', lw=1, label='90th percentile');
    
    ax[0].set_xlabel("Vs [km/s]")
    ax[0].set_ylabel("Depth [km]")
    ax[0].legend().set_visible(False)
    ax[0].set_ylim(vmax, 0)
    ax[0].set_xlim(vs_min.min(), vs_max.max())
    ax[0].grid()


    ax[1].plot(statistics_vs['std'], interp_depths, 'k', lw=1, label='std');
    ax[1].tick_params(labelleft=False)
    ax[1].set_ylabel('')
    ax[1].set_ylim(*ax[0].get_ylim())
    ax[1].set_xlabel("Vs STD")
    ax[1].grid()
    
    Voronoi1D.plot_interface_hist(sampled_voronoi_nuclei, bins=interf_bins, color='b', alpha=0.5, ec='w', ax=ax[2]);
    ax[2].set_ylim(*ax[0].get_ylim())
    ax[2].set_xlim(0,25)

    # Calculate interface histograms based on no. of dimensions per solution
    for e, i in enumerate(range(n_dimensions_min,n_dimensions_max+1),start=3):
        filtered = [a for a in sampled_voronoi_nuclei if len(a) == i]
        Voronoi1D.plot_interface_hist(filtered, bins=interf_bins, color='b', alpha=0.5, ec='w', ax=ax[e]);
        ax[e].set_xlabel(f"Posterior for\n{i}-interface\nsolutions")
        ax[e].grid()
        ax[e].tick_params(labelleft=False)
        ax[e].set_ylabel('')
        ax[e].set_ylim(*ax[0].get_ylim())
        ax[e].set_xlim(0,25)
  
    plt.tight_layout()

    return fig, ax




def plot_data_noise_posterior(f_obs, d_obs, n_dimensions_min, n_dimensions_max,
                              percentiles, results, target, noise_bins=20, noise_std_true=None, f_true=None, d_true=None):
    
    cmap = plt.get_cmap('autumn')
    colors = cmap(np.linspace(0, 1, len(f_obs)))

    fig, ax = plt.subplots(1, 3, figsize=(10, 4))

    if f_true is not None and d_true is not None:
        ax[0].plot(f_true, d_true, 'k--', label='Exact Data')
    ax[0].scatter(f_obs, d_obs, c=colors, edgecolors='black', zorder=3, label='Observed Data')
    ax[0].fill_between(f_obs, percentiles[0], percentiles[1], color='b', alpha=0.5, label='Calc Data\n(10th-90th perc)', zorder=100)
    ax[0].set_xlabel('Frequency [Hz]')
    ax[0].set_ylabel('Phase velocity [km/s]')
    ax[0].grid()
    ax[0].legend().set_visible(False)

    if noise_std_true is not None:
        ax[1].axvline(x=noise_std_true, color='k', lw=2, alpha=1, label='True data noise')
    
    pdf, bins, _ = ax[1].hist(results['rayleigh.std'], color='b', alpha=0.5, density=True, bins=noise_bins, ec='w', zorder=100, label='Posterior')
    ax[1].fill_between([target.std_min, target.std_max], 1 / (target.std_max - target.std_min), alpha=0.2, label='Prior')
    ax[1].set_xlabel('Noise standard deviation')
    ax[1].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    ax[1].legend(framealpha=0.9)

    bins = np.arange(n_dimensions_min-.5, n_dimensions_max+.6, 1)
    pdf, bins, _ = ax[2].hist(results['voronoi.n_dimensions'], color='b', alpha=0.5, density=True, bins=bins, ec='w', zorder=100, label='Posterior')
    ax[2].fill_between([n_dimensions_min-.5, n_dimensions_max+.5], 1 / (1 + n_dimensions_max - n_dimensions_min), alpha=0.2, label='Prior')
    ax[2].set_xlabel('No. of Dimensions')
    ax[2].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    ax[2].legend(framealpha=0.9)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    ax[2].set_xticks(bin_centers)

    plt.tight_layout()

    return fig, ax




def get_subplot_layout(n_subplots):
    rows = int(np.sqrt(n_subplots))
    cols = int(np.ceil(n_subplots / rows))
    return rows, cols

def plot_chains(inversion, Voronoi1D, interp_depths, vmin, vmax, vs_min, vs_max, velocity_model=None):
    n_chains = len(inversion.chains)
    rows, cols = get_subplot_layout(n_chains)
    fig, axes = plt.subplots(rows, cols, figsize=(10, 15), sharey=True)

    # Flatten axes array for easy iteration even if 1D or 2D
    axes_flat = np.ravel(axes)

    for ipanel, (ax, chain) in enumerate(zip(axes_flat, inversion.chains)):
        saved_states = chain.saved_states
        saved_nuclei = saved_states["voronoi.discretization"]
        saved_vs = saved_states['voronoi.vs']

        Voronoi1D.plot_tessellations(saved_nuclei,saved_vs,
                                     ax=ax,linewidth=0.1,color="k",bounds=(vmin, vmax))
        
        if velocity_model is not None:
            Voronoi1D.plot_tessellation(velocity_model[:, 0],velocity_model[:, 2],
                                    color='k',lw=2,ax=ax,input_type='extents')
            
        Voronoi1D.plot_tessellation_statistics(saved_nuclei, saved_vs, interp_depths, ax=ax)

        ax.set_title(f'Chain {chain.id}')
        ax.tick_params(direction='in', labelleft=False, labelbottom=False)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_ylim(vmax, vmin)
        ax.set_xlim(vs_min, vs_max)
        ax.legend().set_visible(False)

        if not ipanel % cols:
            ax.set_ylabel('Depth [km]')
            ax.tick_params(labelleft=True)
        if ipanel >= (rows - 1) * cols:
            ax.set_xlabel('Vs [km/s]')
            ax.tick_params(labelbottom=True)

    # Hide any unused axes if total axes > chains
    for ax in axes_flat[n_chains:]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

    return fig, axes

