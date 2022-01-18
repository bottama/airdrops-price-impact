def airdrop_price_impact(coin, start_date, end_date, current_folder='deliverables'):

    # import modules
    import pandas as pd
    import json
    import requests
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import seaborn as sns
    import os

    # plot settings
    plt.style.use('seaborn')
    sns.set_style("white")
    sns.set_theme(style="ticks")
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False

    # markets
    spot = coin + '/USD'
    perp = coin + '-PERP'

    # spot market
    request = requests.get('https://ftx.com/api//markets/' + spot +
                           '/candles?resolution=3600&start_time=' + str(start_date) + '&end_time=' + str(end_date))
    request = json.loads(request.text)
    df_spot = pd.json_normalize(request['result'])

    # perpetual
    request = requests.get('https://ftx.com/api//markets/' + perp +
                           '/candles?resolution=3600&start_time=' + str(start_date) +
                           '&end_time=' + str(end_date))
    request = json.loads(request.text)
    df_perp = pd.json_normalize(request['result'])

    # funding rates
    request = requests.get('https://ftx.com/api/funding_rates?&future=' + perp +
                           '&start_time=' + str(start_date) + '&end_time=' + str(end_date))
    request = json.loads(request.text)
    df_funding = pd.json_normalize(request['result'])

    print(coin + ' data collected')

    # set index
    df_spot.set_index('startTime', inplace=True)
    df_spot.index = pd.to_datetime(df_spot.index)
    df_spot = df_spot.sort_index()
    df_perp.set_index('startTime', inplace=True)
    df_perp.index = pd.to_datetime(df_perp.index)
    df_perp = df_perp.sort_index()
    df_funding.set_index('time', inplace=True)
    df_funding.index = pd.to_datetime(df_funding.index)
    df_funding = df_funding.sort_index()

    # long-only spot
    n_spot = 1
    spot_pnl = (df_spot['close'] - df_spot['close'][0]) * n_spot
    cum_ret_spot = spot_pnl / df_spot['close'][0] * 100
    print('Long-only $' + coin + ': ' + str(round(cum_ret_spot[-1], 2)) + "%")

    # Long Spot and Short Perpetual
    n_spot = 1
    n_perp = df_spot['close'][0] / df_perp['close'][0]
    spot_pnl = (df_spot['close'] - df_spot['close'][0]) * n_spot
    perp_pnl = (df_perp['close'][0] - df_perp['close']) * n_perp
    funding_pnl = df_funding['rate'] * df_perp['close'] * n_perp
    pnl = spot_pnl + perp_pnl + funding_pnl.cumsum()
    cum_ret_long_short = pnl / (df_spot['close'][0] + 1/20 * df_perp['close'][0]) * 100
    print('Long $' + coin + ' and Shot ' + perp + ': ' + str(round(cum_ret_long_short[-1], 2)) + "%")

    # long-only perpetual
    n_perp = 1
    perp_pnl = (df_perp['close'] - df_perp['close'][0]) * n_perp
    funding_pnl = - df_funding['rate'] * df_perp['close'] * n_perp
    pnl = perp_pnl + funding_pnl.cumsum()
    cum_ret_perp = pnl / (df_perp['close'][0]) * 100
    print('Long ' + perp + ' fully funded: ' + str(round(cum_ret_perp[-1], 2)) + "%")

    # plot
    fig, ax = plt.subplots(3, 1, figsize=(14., 14), gridspec_kw={'height_ratios': [2, 1, 3]})
    fig.text(s='$' + coin + ' vs ' + coin + '-PERP before and after AirDrop \n',
             x=0.375, y=0.95, fontsize=20, ha='center', va='center')
    ax[0].plot(df_spot['close'])
    ax[0].plot(df_perp['close'])
    plt.setp(ax[0], ylabel='USD Value')
    ax[0].margins(x=0)
    ax[1].plot(df_funding['rate'] * 24 * 365 * 100, color='grey')
    ax[1].plot((df_funding['rate'] * 24 * 365 * 100).rolling(24).mean(), color='red')
    ax[1].hlines(y=0, xmin=cum_ret_perp.index[0], xmax=cum_ret_perp.index[-1], linestyles='--',
                 linewidth=.25, colors='black')
    ax[1].margins(x=0)
    ax[2].plot(cum_ret_spot)
    ax[2].plot(cum_ret_long_short)
    ax[2].plot(cum_ret_perp)
    ax[2].margins(x=0)
    ax[2].hlines(y=0, xmin=cum_ret_perp.index[0], xmax=cum_ret_perp.index[-1], linestyles='--',
                 linewidth=.25, colors='black')
    plt.setp(ax[2], ylabel='Performance [%]')
    plt.setp(ax[1], ylabel='Annualized \n Funding Rate [%]')
    if coin == 'OMG':
        ax[0].legend(['$' + coin, coin + '-PERP'], bbox_to_anchor=(.87, 0.9), loc="upper right",
                     bbox_transform=fig.transFigure, ncol=1, frameon=False)
        ax[1].legend(['Annualized Funding Rate [%]', 'MA(1D)'], bbox_to_anchor=(.8, 0.5), loc="lower center",
                     bbox_transform=fig.transFigure, ncol=1,
                     frameon=False)
        ax[2].legend(['Long-only $' + coin + ': ' + str(round(cum_ret_spot[-1], 2)) + "%",
                      'Long $' + coin + ' and Short ' + perp + ': ' + str(round(cum_ret_long_short[-1], 2)) + "%",
                      'Long-only ' + perp + ' fully funded: ' + str(round(cum_ret_perp[-1], 2)) + "%"],
                     bbox_to_anchor=(.77, 0.38), loc="lower center",
                     bbox_transform=fig.transFigure, ncol=1, frameon=False)
    else:
        ax[0].legend(['$' + coin, coin + '-PERP'], bbox_to_anchor=(.15, 0.88), loc="upper left",
                     bbox_transform=fig.transFigure, ncol=1,
                     frameon=False)
        ax[1].legend(['Annualized Funding Rate [%]', 'MA(1D)'], bbox_to_anchor=(.15, 0.54), loc="upper left",
                     bbox_transform=fig.transFigure, ncol=1,
                     frameon=False)
        ax[2].legend(['Long-only $' + coin + ': ' + str(round(cum_ret_spot[-1], 2)) + "%",
                      'Long $' + coin + ' and Short ' + perp + ': ' + str(round(cum_ret_long_short[-1], 2)) + "%",
                      'Long-only ' + perp + ' fully funded: ' + str(round(cum_ret_perp[-1], 2)) + "%"],
                     bbox_to_anchor=(.15, 0.45), loc="upper left",
                     bbox_transform=fig.transFigure, ncol=1,
                     frameon=False)

    # save fig
    cwd = os.getcwd()
    final_wd = cwd.replace(current_folder, '/reports/' + coin + '_case_study.png')
    plt.savefig(final_wd, dpi=180)
    plt.close()

    return print(coin + ' airdrop analysis done')
