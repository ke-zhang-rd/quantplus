import math


def alive_nodes(S, S_upper=None, S_lower=None, every_step=False):
  """Return alive[i][j]: True if node (i, j) survives the thresholds.

  Terminal nodes are alive when S_lower <= S <= S_upper.
  every_step=False: an earlier node is alive if it can still reach an alive
                    terminal node (thresholds apply to the last step only).
  every_step=True : an earlier node must ALSO itself lie inside the band, so a
                    path that leaves the band at any step is cut.
  """
  N = len(S) - 1
  hi = math.inf if S_upper is None else S_upper
  lo = -math.inf if S_lower is None else S_lower
  alive = [[False] * (i + 1) for i in range(N + 1)]
  for j in range(N + 1):
    alive[N][j] = lo <= S[N][j] <= hi
  for i in range(N - 1, -1, -1):
    for j in range(i + 1):
      reach = alive[i + 1][j] or alive[i + 1][j + 1]
      alive[i][j] = reach and (lo <= S[i][j] <= hi if every_step else True)
  return alive


def crr(S0, K, r, sigma, T, N, S_upper=None, S_lower=None, every_step=False, verbose=True):
  """American call on a CRR tree.

  S_upper / S_lower: stock-price thresholds. Nodes outside [S_lower, S_upper]
  are treated as having zero probability and are pruned from the tree.
  None means no threshold on that side.

  every_step=False: thresholds apply to the terminal (expiry) nodes only.
  every_step=True : thresholds apply at every time step.
  """
  dt = T/N

  u = math.exp(sigma * math.sqrt(dt))
  d = 1 / u
  p = (math.exp(r * dt) - d) / (u - d) 
  q = 1 - p
  D = math.exp(-r * dt)

  if verbose:
    print("dt: ", dt)
    print("u: ", u)
    print("d: ", d)
    print("p: ", p)
    print("q: ", q)
    print("D: ", D)

  rows, cols = N+1, N+1
  S = [[0 for _ in range(cols)] for _ in range(rows)]
  payoff = [[0 for _ in range(cols)] for _ in range(rows)]

  for i in range(0, N+1):
    for j in range(0, i+1):
      S[i][j] = S0 * u**(i-j) * d**j
      payoff[i][j] = max(S[i][j] - K, 0.0)
      # payoff is init to exercise payoff

  alive = alive_nodes(S, S_upper, S_lower, every_step)
  if not alive[0][0]:
    raise ValueError("No path survives inside [S_lower, S_upper]")

  if verbose:
    print("S:")
    print(S)

    print("payoff: ")
    print(payoff)

  for i in range(N-1, -1, -1):
    for j in range(i+1):
      if not alive[i][j]:
        payoff[i][j] = 0.0  # pruned node
        continue
      up_ok, dn_ok = alive[i+1][j], alive[i+1][j+1]
      if up_ok and dn_ok:
        from_forward_payoff = D * (p * payoff[i+1][j] + q * payoff[i+1][j+1])
      elif up_ok:
        # down child pruned: all remaining probability goes to up child
        from_forward_payoff = D * payoff[i+1][j]
      elif dn_ok:
        # up child pruned: all remaining probability goes to down child
        from_forward_payoff = D * payoff[i+1][j+1]
      else:
        payoff[i][j] = 0.0  # pruned node
        continue
      payoff[i][j] = max(payoff[i][j], from_forward_payoff)

  if verbose:
    print("payoff: ")
    print(payoff)
    print("payoff[0][0]: ")
    print(payoff[0][0])
  return payoff[0][0]


if __name__ == "__main__":
  r = 0.0425
  sigma = 0.35
  T = 55/365
  S0 = 225
  K = 240
  N = 100

  print("no bounds     :", crr(S0, K, r, sigma, T, N, verbose=False))
  print("last step only:", crr(S0, K, r, sigma, T, N, S_upper=300, S_lower=170, verbose=False))
  print("every step    :", crr(S0, K, r, sigma, T, N, S_upper=300, S_lower=170, every_step=True, verbose=False))
