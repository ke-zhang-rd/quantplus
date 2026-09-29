==========================================
Finance and CRR(Cox-Ross-Rubinstein) model
==========================================

This page explains the pricing model used by ``quantplus`` and the assumptions
behind it. The package implements the Cox-Ross-Rubinstein (CRR) binomial tree
model for option pricing, along with the closed-form Black-Scholes benchmark.

Option pricing problem
----------------------

An option is a derivative whose value depends on the future behavior of an
underlying asset. At a high level, the task is to estimate the present value of
a future payoff under a model for the underlying price process.

For a European option, the value at maturity is known from the payoff function:

- call payoff: max(S_T - K, 0)
- put payoff: max(K - S_T, 0)

where:

- ``S_T`` is the underlying price at maturity
- ``K`` is the strike price

The CRR model provides a discrete-time approximation to the risky asset dynamics.

CRR binomial tree model
-----------------------

The Cox-Ross-Rubinstein framework assumes that the underlying price moves through
a recombining binomial tree over discrete time steps. At each step, the price can
move up or down by multiplicative factors:

- ``u``: up factor
- ``d``: down factor

For a standard CRR construction:

- ``u = exp(sigma * sqrt(dt))``
- ``d = 1 / u``

where ``dt = T / N`` and ``N`` is the number of time steps.

The risk-neutral up probability is:

.. math::

    p = \frac{e^{(r-q)dt} - d}{u - d}

where:

- ``r`` is the risk-free rate
- ``q`` is the dividend yield or carry adjustment
- ``sigma`` is the volatility

This probability is chosen so that the expected discounted stock return matches
the risk-free rate under the risk-neutral measure.

.. plot::
   :caption: A four-step CRR stock-price lattice. Different paths recombine at shared nodes.

   from math import exp, sqrt

   import matplotlib.pyplot as plt

   initial_price = 100.0
   volatility = 0.25
   expiry = 1.0
   steps = 4
   up = exp(volatility * sqrt(expiry / steps))
   down = 1.0 / up

   fig, ax = plt.subplots(figsize=(9, 4.5))
   for level in range(steps):
       for up_moves in range(level + 1):
           x = level
           y = 2 * up_moves - level
           for next_up_moves in (up_moves, up_moves + 1):
               next_x = level + 1
               next_y = 2 * next_up_moves - next_x
               ax.plot([x, next_x], [y, next_y], color="#91a4ad", linewidth=1.2, zorder=1)

   for level in range(steps + 1):
       for up_moves in range(level + 1):
           y = 2 * up_moves - level
           stock_price = initial_price * up**up_moves * down ** (level - up_moves)
           ax.scatter(level, y, s=90, color="#147d78", edgecolor="white", zorder=2)
           ax.annotate(f"{stock_price:.0f}", (level, y), xytext=(0, 10),
                       textcoords="offset points", ha="center", fontsize=8)

   ax.set_xticks(range(steps + 1), [f"Step {step}" for step in range(steps + 1)])
   ax.set_ylabel("Up/down state")
   ax.set_title("Recombining CRR stock-price lattice")
   ax.set_ylim(-steps - 0.8, steps + 0.8)
   ax.grid(axis="x", alpha=0.2)
   ax.spines[["top", "right", "left"]].set_visible(False)
   ax.tick_params(axis="y", left=False, labelleft=False)
   fig.tight_layout()

Backward induction
------------------

The option value is computed recursively from maturity back to the present. At the
terminal nodes, the value is the payoff:

- call: ``max(S - K, 0)``
- put: ``max(K - S, 0)``

Then at each earlier node, the continuation value is computed as the discounted
expected value under the risk-neutral probabilities:

.. math::

    V_{i,j} = e^{-r dt} \left( p V_{i+1,j+1} + (1-p) V_{i+1,j} \right)

For American options, the holder may exercise early, so the value is compared
against the immediate exercise payoff and the larger of the two is chosen:

.. math::

    V_{i,j} = \max\left(V_{i,j}^{continuation}, V_{i,j}^{exercise}\right)

This is exactly the logic implemented in the C++ core of the package.

Threshold pruning
-----------------

``crr_price`` can apply inclusive lower and upper bounds to the stock-price
states. By default, only terminal nodes outside ``[S_lower, S_upper]`` are
removed. Earlier nodes remain eligible only if at least one child can reach an
allowed terminal node. With ``every_step=True``, each intermediate node must
also lie inside the band.

Backward induction follows the surviving branches. If both children survive,
the usual risk-neutral expectation is used. If only one child survives, the
remaining transition probability is assigned to it before discounting; a node
with no surviving child has zero value. This is a thresholded lattice valuation
and differs from an unfiltered CRR price. If the root cannot reach any allowed
terminal node, ``crr_price`` raises ``ValueError``.

.. code-block:: python

    bounded_price = qp.crr_price(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=200,
        q=0.01,
        is_call=True,
        american=True,
        S_lower=80.0,
        S_upper=120.0,
        every_step=True,
    )

Assumptions of the CRR model
----------------------------

The CRR model is based on a set of simplifying assumptions:

- the underlying follows a discrete binomial process over time
- time is divided into a finite number of steps
- volatility is constant over the option life
- the risk-free rate is constant
- the dividend yield or carry rate is constant
- there are no arbitrage opportunities in the risk-neutral pricing setup
- the tree is recombining, so the number of states remains manageable

These assumptions are standard in introductory option-pricing models and are
well suited for educational and benchmark applications.

European vs American options
----------------------------

The package distinguishes between:

- European options: exercise only at maturity
- American options: exercise at any earlier node

In the pricing function, this is controlled by the ``american`` flag:

.. code-block:: python

    price = qp.crr_price(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=200,
        q=0.01,
        is_call=True,
        american=False,
    )

For a European option, the code follows the standard backward-induction valuation
without early exercise checks. For an American option, it compares continuation
value against exercise value at each time step.

Black-Scholes benchmark
-----------------------

The package also exposes ``black_scholes_price``, which gives the closed-form
solution to the same problem under the continuous-time geometric Brownian motion
model. This is valuable for two reasons:

- it provides a familiar benchmark
- it shows how the binomial model approaches continuous-time pricing as ``N`` grows

The CRR tree becomes more accurate as the number of steps increases because the
lattice approximates the continuous diffusion more finely.

.. plot::
   :caption: European call prices from the CRR tree approach the Black-Scholes benchmark as the number of steps increases.

   import matplotlib.pyplot as plt
   import quantplus as qp

   spot = 100.0
   strike = 100.0
   rate = 0.05
   volatility = 0.20
   expiry = 1.0
   dividend_yield = 0.01
   step_counts = [5, 10, 20, 40, 80, 160, 320]
   crr_prices = [
       qp.crr_price(spot, strike, rate, volatility, expiry, count,
                    q=dividend_yield, is_call=True)
       for count in step_counts
   ]
   benchmark = qp.black_scholes_price(
       spot, strike, rate, volatility, expiry, q=dividend_yield, is_call=True
   )

   fig, ax = plt.subplots(figsize=(8, 4.5))
   ax.plot(step_counts, crr_prices, marker="o", color="#147d78", label="CRR")
   ax.axhline(benchmark, color="#c05a36", linestyle="--", label="Black-Scholes")
   ax.set_xscale("log", base=2)
   ax.set_xticks(step_counts, [str(count) for count in step_counts])
   ax.set_xlabel("Number of CRR steps")
   ax.set_ylabel("European call price")
   ax.set_title("CRR convergence to Black-Scholes")
   ax.grid(alpha=0.25)
   ax.legend(frameon=False)
   fig.tight_layout()

How the code implements this
----------------------------

In the C++ core, the process is implemented as a nested loop over time steps and
stock states. The numerical sequence is:

1. compute the terminal payoffs
2. iterate backwards through time
3. compute continuation values using risk-neutral probabilities
4. compare with early exercise when required
5. return the root node value

In the Python layer, the function only validates user input and then calls the
compiled native implementation. This keeps the public interface simple while
preserving efficient numerical execution.

This means the model logic is not hidden in Python loops; the expensive
calculation runs inside the compiled C++ implementation, while user code remains
clean and readable.

Practical interpretation
------------------------

The CRR model is especially useful for:

- teaching option-pricing mechanics
- benchmarking numerical methods
- approximating option values when closed-form formulas are not available
- exploring early-exercise behavior for American options

It is not a complete market model for all exotic derivatives, but it is a clean,
transparent framework for vanilla options and for understanding how discrete-time
pricing works in practice.

