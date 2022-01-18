# Airdrops and Price Discovery
## $OMG and $CREAM case studies

### Author: Matteo Bottacini, [matteo.bottacini@cryptofinance.ch](mailto:matteo.bottacini@cryptofinance.ch) 
### Last update: January 18th, 2022

## Project description
In this project is investigated the price formation in the Crypto Markets when an Airdrop is announced.

Folder structure:
~~~~
airdrops-price-impact/
    deliverables/
        run-analysis.py
    src/
        utils.py
    reports/
        CREAM_case_study.png
        ONG_case_study.ong
    README.md
~~~~

## Table of contents
1. [Deliverables](#deliverables)
2. [Src](#src)
3. [Report](#report)

## Deliverables
In this folder is contained the only script that you need to run to perform the analysis: [run_analysis.py](/deliverables/run_analysis.py).
The script produces to plots that are stored in [/reports](/reports):
1. [OMG case study](/reports/OMG_case_study)
2. [CREAM case study](/reports/CREAM_case_study)

## Src
In this folder is the script with the set of functions that perform the analysis: [utils.py](/src/utils.py) 

## Report

According to the [Binance Academy Glossary](https://academy.binance.com/en/glossary/airdrop), the term airdrop refers to "the distribution of digital assets to the public, either by virtue of holding a certain other token or simply by virtue of being an active wallet address on a particular blockchain."

In practice, a user must, for the most part, hold a certain amount of a predefined asset in a public wallet at the time of the snapshot, and after that they will receive the new coins for "free" in their wallet.

Let us take a closer look at the case of $OMG.

The BOBA Network announced that the OMG Foundation would launch a token to support the network (BOBA) as a governance token.
Users holding OMG tokens on L1 or L2 on November 12, 2021 at 00:00 received a BOBA token for each OMG token they held in their wallets ([Link to full story](https://boba.network/token/)).

This sounds great: free tokens!

But, as you might surmise, behind every airdrop is a great deal of marketing hype trying to create project awareness to boost the price.

In the first subplot on the below chart, you can see the price dynamics of $OMG (blue line) and OMG-PERP (orange line) ten days before and after the airdrop (data provided by [FTX.com](https://docs.ftx.com/#overview).

![](/reports/OMG_case_study)

Before the snapshot, the spot price increased from $15 to $20 (approx. 33%), while the future perpetual price went from $15 to around $16 (approx. 6%), creating a strong backwardation.

After the snapshot, both prices plummeted and converged at around $13.5, and then continued to fall for the next few days that followed.

The airdrop event created a strong demand and inflow into the spot market, but the Futures Market, which was not eligible for the airdrop, discounted the price more and more.

Futures by nature always try to "anticipate" future events. The Trading team and I always like to remind ourselves that "there is always a reason when a future looks 'cheap' (backwardation) and when a future looks 'expensive' (contango)". 
Well, this time things were pretty clear.

In the second subplot, we can see the Hourly Funding Rates Annualised (grey line) and the one-day Moving Average of the funding rates (red line).

Funding rates represent the "cost of capital" of entering a position in the perpetual futures market. 

When funding rates are greater (lower) than 0, the market is in contango (backwardation).
Also, when funding rates are positive (negative), the holder of a long position (short position) will pay the funding rate every hour to the holder of a short position (long position).
Therefore, it is important to account for them when studying the PnL of a hedging strategy.

Let us say we wanted the BOBA token, but we did not want to run the price risk. We would need to hedge our position by taking a short position in the futures market. Given the pronounced backwardation, every hour we would have to pay the funding, thus making this strategy really expensive.

In the third subplot, we see the performance of a long only strategy on $OMG (blue line), and the performance of a hedged strategy consisting of buying $OMG and shorting at time 0 OMG-PERP for the same notional amount (orange line). 
Both performed poorly: long-only: -37.6%, and the hedged one: -30.62%.

Finally, one should play the game in these three cases:
a. One believes in a new project (BOBA, in this case) really strongly and wants to obtain the airdrop no matter the price of $OMG.
b. One is fast enough to get out before it is too late.
c. One is a risk-lover and is trying to speculate by entering a leverged long position in the perpetual, gaining the negative funding rates and any price increase.And today, almost the same thing is happening with $CREAM.

After the announcement of the new airdrop, the spot price started climbing: from $40 to roughly $90 (120% approx. in just two days), and the perpetual price followed slightly below this number. 

In my view, whether $CREAM was really in high water, investors front ran the announcement too soon and too quickly.

Assuming funding rates to be on average (optimistically) -100% annualised, shorting the perp and paying the funding for ten days will cost approx 2.8% too much. 

In the plot below, we can see the price dynamics (first subplot), the funding rates (second subplot), and the strategies performance (third subplot) as of today.

(plot: CREAM_case_study.pdf)

At the time of writing, $CREAM is trading at $61. 

Looking at the charts and at some key indicators (RSI, MAs, etc.), I expect prices to drop a bit more before a nice rally occurs prior the snapshot.

Given the current market capitalisation of $38 million, a 100% price increase would not be out of the ordinary in the crypto space, but please do not forget to pay attention to the airdrop's snapshot.

Happy trading!
